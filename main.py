import os
from dotenv import load_dotenv
import json
import openai

load_dotenv(".env")

options = ['discussion', 'optimization']
print("Please select an option:")
for index, option in enumerate(options):
    print(f"{index+1}. {option}")
choice = int(input("Enter your choice (1-2): "))
while choice not in range(1, len(options)+1):
    print("Invalid choice. Please try again.")
    choice = int(input("Enter your choice (1-2): "))
selected_option = options[choice-1]

if selected_option == "discussion":
    role = input("Enter the role of the assistant: ")
    assistant = f"You are {role}, one of the participants in a discussion. Conversationally reply to: "
    interlocutor = f"You are having having a discussion with {role}. Challenge the statements of {role}: "
elif selected_option == "optimization":
    role = input("Define the role of the interlocutor: ")
    assistant = f"You are an advanced {role}. You find flaws, issues, or possible optimization opportunities in the provided code. You return only the rewritten code, you do not wrap your code, you do not add backticks, you do not explain your code. The code: "
    interlocutor = f"You are an advanced {role}. You find flaws, issues, or possible optimization opportunities in the provided code. You return only the rewritten code, you do not wrap your code, you do not add backticks, you do not explain your code. The code: "

prompt = input("Enter prompt:" )

base_url = os.getenv("BASE_URL")
model = os.getenv("MODEL")
max_tokens = int(os.getenv("MAX_TOKENS"))
temp = float(os.getenv("TEMPERATURE"))
freq = float(os.getenv("FREQ_PENALTY"))
pres = float(os.getenv("PRES_PENALTY"))
openai.api_key = os.getenv("TOKEN")
fpath = "results.txt"


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

def make_discussion(result, response):
    if os.path.exists(fpath):  # Check if the file exists
        mode = "a"  # If file exists, open it in append mode
    else:
        mode = "w"  # If file doesn't exist, open it in write mode
    with open(fpath, mode) as u_file:
        u_file.write("=========\n" + json.dumps(response['usage']) + "\n=========\n" + result + "\n=========\n")

def get_legacy_response(prompt, n):
    if n == 0:
        prompt = interlocutor + prompt
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
        if 'usage' in response and 'completion_tokens' in response['usage']:
            completion_tokens = response['usage']['completion_tokens']
        if not completion_tokens or completion_tokens == 0:
            get_legacy_response(prompt, n)

        make_discussion(result, response)

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