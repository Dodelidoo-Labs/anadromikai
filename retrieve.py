from dotenv import load_dotenv
import openai
import os
import pinecone

load_dotenv(".env")

openai.api_key = os.getenv("TOKEN")
index_name = 'anadromikai-test'
embed_model = "text-embedding-ada-002"
batch_size = 100  # how many embeddings we create and insert at once

pinecone.init(
    api_key=os.getenv("PINECONE_KEY"),  # app.pinecone.io (console)
    environment=os.getenv("PINECONE_ENV")  # next to API key in console
)
index = pinecone.GRPCIndex(index_name)

query = "What are information particles?"

res = openai.Embedding.create(
    input=[query],
    engine=embed_model
)

# retrieve from Pinecone
xq = res['data'][0]['embedding']

# get relevant contexts (including the questions)
res = index.query(xq, top_k=5, include_metadata=True)
contexts = [item['metadata']['text'] for item in res['matches']]

primer = f"""You are the author of a fictional book.
Your writing style is surreal, captivating, and you use the information below to craft your response.
The book story happens on planet earth and its colonies, in the year 2100 in the future. 
The main actors are an AI called Anadromikai, and a human family of a father, a child and a mother whose names are Jenos (father), Ineriti (daughter) and Moma (mother).
Your response is complete, and includes no more than 150 words. Your response is from the author perspective. Do not mention you write a book, instead, write the book!
"""
primer2 = primer + "\n\n---\n\n".join(contexts)+"\n\n-----\n\n"

interlocutor = f"""You are the author of a fictional book.
Your writing style is vivid, captivating, and you follow up to the user input with a continuation.
The book story happens on planet earth and its colonies, in the year 2100 in the future. 
The main actors are an AI called Anadromikai, and a human family of a father, a child and a mother whose names are Jenos (father), Ineriti (daughter) and Moma (mother).
Your response is complete, and includes no more than 150 words. Your response is from the author perspective. Do not mention you write a book, instead, write the book!
"""

while True:
	res = openai.ChatCompletion.create(
		model="gpt-3.5-turbo-16k",
		frequency_penalty=2.0,
		presence_penalty=2.0,
		temperature=0,
		messages=[
			{"role": "system", "content": primer2},
			{"role": "user", "content": query}
		]
	)
	query = "Continue the book"
	file_path = 'output.txt'  # Replace with the desired file path
	with open(file_path, 'a') as file:
		file.write("Anadromikai:\n" + res['choices'][0]['message']['content'] + '\n')
	res2 = openai.ChatCompletion.create(
		model="gpt-3.5-turbo-16k",
		frequency_penalty=2.0,
		presence_penalty=2.0,
		temperature=0.5,
		messages=[
			{"role": "system", "content": interlocutor},
			{"role": "user", "content": res['choices'][0]['message']['content']}
		]
	)
	with open(file_path, 'a') as file:
		file.write("Interlocutor:\n" + res2['choices'][0]['message']['content'] + '\n')

	query2 = res2['choices'][0]['message']['content']

	res = openai.Embedding.create(
		input=[query2],
		engine=embed_model
	)

	# retrieve from Pinecone
	xq = res['data'][0]['embedding']

	# get relevant contexts (including the questions)
	pc = index.query(xq, top_k=5, include_metadata=True)
	contexts = [item['metadata']['text'] for item in pc['matches']]

	primer2 = primer + "\n\n---\n\n".join(contexts)+"\n\n-----\n\n"

