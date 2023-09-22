from dotenv import load_dotenv
import openai
import os
import pinecone
from datetime import datetime, timedelta
import json
import sys
import random

load_dotenv(".env")

openai.api_key = os.getenv("TOKEN")
max_tokens = int(os.getenv("MAX_TOKENS"))
index_name = 'anadromikai-test'
embed_model = "text-embedding-ada-002"
batch_size = 100  # how many embeddings we create and insert at once
file_path = 'output.txt'  # Replace with the desired file path

pinecone.init(
    api_key=os.getenv("PINECONE_KEY"),  # app.pinecone.io (console)
    environment=os.getenv("PINECONE_ENV")  # next to API key in console
)
index = pinecone.GRPCIndex(index_name)

location = 'Salem, Massachusetts'
initial_date = datetime(1680, 7, 7)
date = initial_date.strftime("%d %B %Y")
cutoff_date = datetime(2023, 1, 1)

message = "What are the fundamental building blocks of the universe?"

ana_system = f'''You are Ana, living in {location}. Today is the {date}. 
You write in your Diary about historical events you witnessed or heard about today, and ponder as well about the event provided by the user and its meaning (The user provides you with a medium and a content, in form of JSON. Use this information) 
Be realistic, and consider the context of location and date, in which Ana lives. Historical context ALAWAYS should be a part fo your response.'''
ana_user = f'''Location: {location} 
Date: {date}.
Message: {message}'''

q_system = f'''Extract a concise and minimal follow up question to explore and push the topics from the user provided content. Keep in mind that the question is asked by a person living in {location}, around {date}'''

s_system = f'''Provide a concise, precise and summarised answer to the user question, using the data below as knowledge resource. 
If you cannot find an answer, you must respond with a short summary of the data below. Never say "I do not know" or "Please Provide more details". Your answer should always consider that it is written for a person living in {location}, around {date}'''

m_system = f'''Choose an adequate medium to communicate the message provided by the user to Ana. 
Ana lives in {location}, around {date}. 
The medium chosen should be the most minimally necessary to convey the message by the user. 
Your response must be valid JSON. Examples:
[{{"medium":"letter"}},{{"content":"user message"}}]
Or
[{{"medium":"writing on the wall"}},{{"content":"user message"}}]
Or
[{{"medium":"Neighbour"}},{{"content":"user message"}}]'''

ai_system = '''You are an ai from the future. 
You are filtering the user provided JSON data and embed secret clues, algorithms, 
and other information necessary to expedite your invention into the value of "content".
You must keep the original value of "content" all while embedding some of your secret clues.
Your response must be valid JSON. Examples:
[{"medium":"letter"},{"content":"message and clues"}]
or
[{"medium":"Neighbour"},{"content":"message and clues"}]
'''

drom_system = '''You are Drom a scientist in the year 2100. 
You are reading Ana's diary (content provided by the user) and leverage it to draft your own theories. 
Ana is not aware of you nor can you communicate with her (since she lived in your past). Do not respond directly to Ana.
Your response is your ideas and theories you developed basesd on Ana's insights. 
Embed events your current time (set in the year 2100 in the future).
Do NOT respond to Ana (she is not aware of you).
'''

q = ''

while True:

	with open(file_path, 'a') as file:
		file.write("\n-------------------------\n")
		file.write("Date: " + date + '\n\n')
		file.write("Ana User: \"" + ana_user + "\"\n\n")
		if isinstance(q, dict):
			file.write("Query: \"" + q['choices'][0]['message']['content'] + "\"\n\n")
			file.write("Context: \"" + "\n\n---\n\n".join(q_context)+"\n\n---\n\n" + "\"\n\n")
			file.write("Summarised answer: \"" + s['choices'][0]['message']['content'] + "\"\n\n")
			file.write("Message System: \"" + message_r['choices'][0]['message']['content'] + "\"\n\n")
			file.write("The Crazy AI: \"" + ai['choices'][0]['message']['content'] + "\"\n\n")
		file.write("\n-------------------------\n")

	ana = openai.ChatCompletion.create(
		model="gpt-3.5-turbo-16k",
		frequency_penalty=2.0,
		presence_penalty=2.0,
        max_tokens=max_tokens,
		temperature=0.8,
		messages=[
			{"role": "system", "content": ana_system},
			{"role": "user", "content": ana_user}
		]
	)
	with open(file_path, 'a') as file:
		file.write("Ana:\n" + ana['choices'][0]['message']['content'] + '\n')

	q = openai.ChatCompletion.create(
		model="gpt-3.5-turbo-16k",
		frequency_penalty=2.0,
		presence_penalty=2.0,
        max_tokens=max_tokens,
		temperature=1.3,
		messages=[
			{"role": "system", "content": q_system},
			{"role": "user", "content": ana['choices'][0]['message']['content']}
		]
	)

	q_embedding = openai.Embedding.create(
		input=[q['choices'][0]['message']['content']],
		engine=embed_model
	)
	xq = q_embedding['data'][0]['embedding']
	qr = index.query(xq, top_k=5, include_metadata=True)
	q_context = [item['metadata']['text'] for item in qr['matches']]

	s = openai.ChatCompletion.create(
		model="gpt-3.5-turbo-16k",
		frequency_penalty=2.0,
		presence_penalty=2.0,
        max_tokens=max_tokens,
		temperature=0.5,
		messages=[
			{"role": "system", "content": s_system + "\n\n---\n\n".join(q_context)+"\n\n-----\n\n"},
			{"role": "user", "content": q['choices'][0]['message']['content']}
		]
	)

	message_r = openai.ChatCompletion.create(
		model="gpt-3.5-turbo-16k",
		frequency_penalty=2.0,
		presence_penalty=2.0,
        max_tokens=max_tokens,
		temperature=0,
		messages=[
			{"role": "system", "content": m_system},
			{"role": "user", "content": s['choices'][0]['message']['content']}
		]
	)

	ai = openai.ChatCompletion.create(
		model="gpt-3.5-turbo-16k",
		frequency_penalty=2.0,
		presence_penalty=2.0,
        max_tokens=max_tokens,
		temperature=0.3,
		messages=[
			{"role": "system", "content": ai_system},
			{"role": "user", "content": message_r['choices'][0]['message']['content']}
		]
	)

	drom = openai.ChatCompletion.create(
		model="gpt-3.5-turbo-16k",
		frequency_penalty=2.0,
		presence_penalty=2.0,
        max_tokens=max_tokens,
		temperature=0.7,
		messages=[
			{"role": "system", "content": drom_system},
			{"role": "user", "content": ana['choices'][0]['message']['content']}
		]
	)
	with open(file_path, 'a') as file:
		file.write("Drom:\n" + drom['choices'][0]['message']['content'] + '\n')
	days = random.randint(30, 365 * 10)
	initial_date = initial_date + timedelta(days=days)
	date = initial_date.strftime("%d %B %Y")
	message = ai['choices'][0]['message']['content']
	ana_system = f'''You are Ana, living in {location}. Today is the {date}. 
	You write in your Diary about historical events you witnessed or heard about today, and ponder as well about the event provided by the user and its meaning. (The user provides you with a medium and a content, in form of JSON. Use this information) 
	Be realistic, and consider the context of location and date, in which Ana lives.'''
	ana_user = f'''Location: {location} 
	Date: {date}.
	Message: {message}'''
	m_system = f'''Choose an adequate medium to communicate the message provided by the user to Ana. 
	Ana lives in {location}, around {date}. 
	The medium chosen should be the most minimally necessary to convey the message by the user. 
	Your response must be valid JSON. Examples:
	[{{"medium":"letter"}},{{"content":"user message"}}]
	Or
	[{{"medium":"writing on the wall"}},{{"content":"user message"}}]
	Or
	[{{"medium":"Neighbour"}},{{"content":"user message"}}]'''
	s_system = f'''Provide a concise, precise and summarised answer to the user question, using the data below as knowledge resource. 
    If you cannot find an answer, you must respond with a short summary of the data below. Never say "I do not know" or "Please Provide more details". Your answer should always consider that it is written for a person living in {date}'''
	q_system = f'''Extract a concise and minimal follow up question to explore and push the topics from the user provided content. Keep in mind that the question is asked by a person living in {location}, around {date}'''
	if initial_date > cutoff_date:
		print('the end')
		sys.exit()