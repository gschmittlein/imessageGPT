#!/usr/bin/env python
# coding: utf-8

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import ElasticVectorSearch
from langchain.vectorstores import FAISS
import pandas as pd
import openai
from time import time,sleep
import re
import sentence_transformers
import sys
import os
from os import path

os.environ["TOKENIZERS_PARALLELISM"] = "false"

embeddings = HuggingFaceEmbeddings()

# TODO: input openai api key here
openai.api_key = sys.argv[1]

# # Set up FAISS Vector DB with Messages
if path.exists("faiss_index") == False:
    print("creating faiss index, this may take a minute (or two)")
    # TODO: read in your csv file here
    df = pd.read_csv(sys.argv[2])
    # data transformations on csv file
    df['fulltext'] = df['sender'] + ": " + df['text']
    df['fulltext'] = df['fulltext'].apply(lambda x: x.replace("\\n", ""))
    fulltext = "\n".join(df['fulltext'])
    embeddings = HuggingFaceEmbeddings()
    text_splitter = CharacterTextSplitter(separator=" ", chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_text(fulltext)
    db = FAISS.from_texts(texts, embeddings)
    # write to faiss index file
    db.save_local("faiss_index")
else:
    print("reading in faiss index")
    # read in from faiss index file
    db = FAISS.load_local("faiss_index", embeddings)

# # Run Embedding Search
# TODO: write your own query here
query = sys.argv[3]
print("running embedding search based on query")
docs = db.similarity_search(query, k = 10)

# get context
context_list = []
for i in range(0, len(docs)):
    context_list.append(docs[i].page_content)
# pull together context
context = "\n###\n".join(context_list)

# function to submit a prompt to openai api
def gpt3_completion(prompt, model='gpt-3.5-turbo', temp=0.7, top_p=1.0, tokens=500, freq_pen=0, pres_pen=0.0, stop=['<<END>>']):
    max_retry = 3
    retry = 0
    while True:
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages = [
                    {"role": "system", "content": "You are a helpful assistant designed to scan text messages and provide the correct answer based on the context provided. Feel free to make inferences or stretches based on the context provided."},
                    {"role": "user", "content": prompt},
                            ],
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response["choices"][0]["message"]["content"].strip()
            text = re.sub('\s+', ' ', text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)

# defining prompt
prompt = f"Based on the records of text messages below, answer the following question: {query}.\n\nText messages:\n{context}"

# running gpt3 completion
print("running openai completion")
gpt3_result = gpt3_completion(prompt, temp = 1, tokens = 500)

# print query + response
print("\n###\nuser query: " + query + "\n###\n" + "chatgpt response: " + gpt3_result + "\n###")
