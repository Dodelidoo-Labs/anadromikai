from dotenv import load_dotenv
from langchain.document_loaders import UnstructuredFileLoader
from langchain.document_loaders import csv_loader
import openai
import os
import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter
from uuid import uuid4
from tqdm.auto import tqdm
import openai
import pinecone
from tqdm.auto import tqdm
import datetime
from time import sleep
import sys
import re

tokenizer = tiktoken.get_encoding('p50k_base')

load_dotenv(".env")
file_loader_path = input("The File path (example: /Users/username/Desktop/docs/d.rtf)")
openai.api_key = os.getenv("TOKEN")
index_name = 'anadromikai-test'
embed_model = "text-embedding-ada-002"
batch_size = 100  # how many embeddings we create and insert at once
pinecone.init(
    api_key=os.getenv("PINECONE_KEY"),  # app.pinecone.io (console)
    environment=os.getenv("PINECONE_ENV")  # next to API key in console
)

if index_name not in pinecone.list_indexes():
    # if does not exist, create index
    pinecone.create_index(
        index_name,
        dimension=1536,
        metric='cosine'
    )

loader = UnstructuredFileLoader(file_loader_path)
docs = loader.load()
data = []
for doc in docs:
    # timestamp_match = re.search(r"timestamp: (\d+)", doc.page_content)
    # sender_match = re.search(r"sender: (.+)", doc.page_content)
    # messages_match = re.search(r"messages: (.+)", doc.page_content)
    # emoji_desc_match = re.search(r"emoji_desc: (.+)", doc.page_content)

    # timestamp = timestamp_match.group(1) if timestamp_match else 'None'
    # sender = sender_match.group(1) if sender_match else 'None'
    # messages = messages_match.group(1) if messages_match else 'None'
    # emoji_desc = emoji_desc_match.group(1) if emoji_desc_match else 'None'

    data.append({
        # 'timestamp': timestamp,
        # 'sender': sender,
        'text': doc.page_content,
        # 'emotion': emoji_desc
    })

def tiktoken_len(text):
    tokens = tokenizer.encode(
        text,
        disallowed_special=()
    )
    return len(tokens)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=20,
    length_function=tiktoken_len,
    separators=["\n\n", "\n", " ", ""]
)

chunks = []

for idx, record in enumerate(tqdm(data)):
    texts = text_splitter.split_text(record['text'])
    chunks.extend([{
        'id': str(uuid4()),
        'text': texts[i],
        # 'timestamp': record['timestamp'],
        # 'sender': record['sender'],
        # 'emotion': record['emotion'],
        'chunk': i,
    } for i in range(len(texts))])

# initialize connection to pinecone

# connect to index
index = pinecone.GRPCIndex(index_name)

for i in tqdm(range(0, len(chunks), batch_size)):
    # find end of batch
    i_end = min(len(chunks), i+batch_size)
    meta_batch = chunks[i:i_end]
    # get ids
    ids_batch = [x['id'] for x in meta_batch]
    # get texts to encode
    texts = [x['text'] for x in meta_batch]
    # create embeddings (try-except added to avoid RateLimitError)
    try:
        res = openai.Embedding.create(input=texts, engine=embed_model)
    except:
        done = False
        while not done:
            sleep(5)
            try:
                res = openai.Embedding.create(input=texts, engine=embed_model)
                done = True
            except:
                pass
    embeds = [record['embedding'] for record in res['data']]
    # cleanup metadata
    meta_batch = [{
        'text': x['text'],
        'chunk': x['chunk'],
        # 'timestamp': x['timestamp'],
        # 'sender': x['sender'],
        # 'emotion': x['emotion']
    } for x in meta_batch]
    to_upsert = list(zip(ids_batch, embeds, meta_batch))
    # upsert to Pinecone
    index.upsert(vectors=to_upsert)