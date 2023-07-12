import os
from dotenv import load_dotenv
import json
import openai

load_dotenv(".env")

options = ['comic', 'discussion', 'optimization']
print("Please select an option:")
for index, option in enumerate(options):
    print(f"{index+1}. {option}")
choice = int(input("Enter your choice (1-3): "))
while choice not in range(1, len(options)+1):
    print("Invalid choice. Please try again.")
    choice = int(input("Enter your choice (1-3): "))
selected_option = options[choice-1]

if selected_option == "comic":
    assistant = interlocutor = "You are a comic writer. You follow up to the previous comic panel scene with a new comic panel scene. Your response includes only visual descriptions of the comic panel scene itself. You use about 120 characters for the description. Your next comic panel scene is a direct continuation of this scene: "
elif selected_option == "discussion":
    assistant = input("Enter a description of the assistant: ")
    interlocutor = f"You are having a discussion with {assistant}. Respond in a colloquial tone, ask questions or challenge the response. Mention the discussion subject at least once. The response is: "
elif selected_option == "optimization":
    assistant = "You received some critique on your last statement. Follow up on the critique. Critique: "
    interlocutor = f"You are an advanced {type}. You are reviewing and suggest optimizations, corrections, better ways to achieve, point out eventual flaws or security issues to the context given you by {assistant}. Your response follows this format: Statement: (statement reviewed here) Critique: (critique here)"

prompt = input("Enter prompt:" )

base_url = os.getenv("BASE_URL")
model = os.getenv("MODEL")
max_tokens = int(os.getenv("MAX_TOKENS"))
temp = float(os.getenv("TEMPERATURE"))
freq = float(os.getenv("FREQ_PENALTY"))
pres = float(os.getenv("PRES_PENALTY"))
openai.api_key = os.getenv("TOKEN")
jsonpath = "logs.json"
fpath = "results.txt"
cpath = "comic.pdf"

def appendto(file, data):
    if os.path.isfile(file) and os.path.getsize(file) > 0:
        with open(file, 'r') as f:
            existing_data = json.load(f)
    else:
        # If file doesn't exist or is empty, initialize an empty list
        existing_data = []
    existing_data.append(data)
    with open(file, 'w') as f:
        json.dump(existing_data, f)

def make_image(result):
    image = openai.Image.create(
		prompt=result + ", Comic scene in the style of Alejandro Jodorowsky",
		n=1,
		size="512x512"
	)
    image_url = image['data'][0]['url']
    data = {
		"content": result,
		"url": image_url
	}
    appendto(jsonpath, data)

def make_discussion(result):
    if os.path.exists(fpath):  # Check if the file exists
        mode = "a"  # If file exists, open it in append mode
    else:
        mode = "w"  # If file doesn't exist, open it in write mode
    with open(fpath, mode) as u_file:
        u_file.write(result)

def get_legacy_response(prompt, n):
    try:
        response = openai.Completion.create(
			model=model,
			prompt=prompt,
			temperature=temp,
			max_tokens=max_tokens,
			frequency_penalty=freq,
			presence_penalty=pres,
            stop="###"
		)
        result = response['choices'][0]['text']

        if selected_option == "comic":
            make_image(result)
        elif selected_option == "discussion" or selected_option == "optimization":
            make_discussion(result)

        n += 1
        if n % 2 != 0:
            prompt = interlocutor + result
        else:
            prompt = assistant + result

        get_legacy_response(prompt, n)

        return result
    except Exception as e:
        result = f'Request failed with exception {e}'
        print( result )
        return False

def recur():
    get_legacy_response(prompt, 0)

recur()