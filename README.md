# imessageGPT

A python module for running a chatGPT question and answer layer on top imessage text data. Designed to be used with Tommy Praeger's repo imessage_analysis.

## Prerequisites:

To run the script you must have Python installed. I recommend Python 3.9.0 or later. You will also have to download the packages outlined in the requirements.txt file. Finally, you will have to run Tommy Praeger's imessage_analysis repo to generate a csv file containing message data for the chat you would like to query.

## Setup:

Before running the script, you should make sure that the message csv file is in the same directory as the messageGPT.py file. You will also need to have an active OpenAI account (free account works) with an API key.

## Running:

To run the question and answer, simply open terminal and cd into the directory containing messageGPT.py. Once you are there, you should run the command **python3 messageGPT.py "OPENAI-KEY" "CSV-FILENAME" "QUERY"**

You should input your OpenAI key, csv filename, and desired query where indicated in the command. This is all the script needs to run. On a first run-through, it may take some time to complete - as it needs to create the FAISS vector database. But upon running once it will store the database and simply read it in for all future runs.