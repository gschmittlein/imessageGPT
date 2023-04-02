# imessageGPT

A python module for running a chatGPT question and answer layer on top imessage text data.

## Prerequisites:

- First, to run the script you must have Python installed. I recommend Python 3.9.0 or later download [here](https://www.python.org/downloads/). With earlier versions you may run into issues with package installation.
- You will also have to download the packages outlined in the requirements.txt file.
- Finally, you will have to run Tommy Praeger's [imessage_analysis](https://github.com/tommypraeger/imessage_analysis) repo to generate a csv file containing message data for the chat you would like to query.

## Setup:

Before running the script, you will also need to have an active OpenAI account with an API key (you can set up your account [here](https://platform.openai.com/account/api-keys)). You should also make sure that the message csv file is in the same directory as the messageGPT.py file. The message csv file should at least have three fields: **text** (the body text of the message), **sender** (the name of the person who sent the text) and **time** (the timestamp).

## Running:

To run the question and answer, simply open terminal and cd into the directory containing messageGPT.py. Once you are there, you should run the command `python3 messageGPT.py "OPENAI-KEY" "CSV-FILENAME" "QUERY"`

You should input your OpenAI key, csv filename, and desired query where indicated in the command. This is all the script needs to run. On a first run-through, it may take some additional time to complete - as it needs to create the FAISS vector database based on your dataset. But upon running once it will store the database as a FAISS index and simply re-read it in for all future runs.