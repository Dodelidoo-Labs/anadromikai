import csv
import re
from datetime import datetime
import demoji

# Step 1: Read the text file
with open('/path/to/file.txt', 'r') as file:
    text_data = file.readlines()

# Step 2: Parse the data
chat_data = []
current_timestamp = None
current_sender = None
current_message = ""
current_emoji_desc = ""

for line in text_data:
    line = line.strip()
    if line:
        match = re.match(r'(\d{1,2}/\d{1,2}/\d{4}, \d{1,2}:\d{2}:\d{2} [APM]+): ([^:]+): (.*)', line)#re.match(r'(\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2} [APM]+) - ([^:]+): (.*)', line)
        if match:
            if current_timestamp and current_sender and current_message:
                chat_data.append({'timestamp': int(current_timestamp), 'sender': current_sender, 'message': current_message.strip(), 'emoji_desc': current_emoji_desc.strip()})
            #current_timestamp = datetime.strptime(match.group(1), "%m/%d/%y, %I:%M %p").timestamp()
            current_timestamp = datetime.strptime(match.group(1), "%d/%m/%Y, %I:%M:%S %p").timestamp()
            current_sender = match.group(2).lstrip('+').strip()
            current_message = demoji.replace(match.group(3), "")
            current_emoji_desc = " ".join(demoji.findall(match.group(3)).values())
        else:
            current_message += "\n" + demoji.replace(line)
            current_emoji_desc += " " + " ".join(demoji.findall(line).values())

# Add the last message to chat_data
if current_timestamp and current_sender and current_message:
    chat_data.append({'timestamp': int(current_timestamp), 'sender': current_sender, 'message': current_message.strip(), 'emoji_desc': current_emoji_desc.strip()})

# Step 3: Group messages
grouped_messages = {}
for data in chat_data:
    key = (data['timestamp'], data['sender'])
    if key in grouped_messages:
        grouped_messages[key].append({'message': data['message'], 'emoji_desc': data['emoji_desc']})
    else:
        grouped_messages[key] = [{'message': data['message'], 'emoji_desc': data['emoji_desc']}]

# Step 4: Convert to CSV
with open('chat_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['timestamp', 'sender', 'messages', 'emoji_desc'])
    for (timestamp, sender), messages in grouped_messages.items():
        writer.writerow([timestamp, sender, '\n'.join([msg['message'] for msg in messages]), '\n'.join([msg['emoji_desc'] for msg in messages])])
