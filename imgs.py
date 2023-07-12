import os
import requests
import json

def download_image(url, file_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Image downloaded: {file_path}")
    else:
        print(f"Failed to download image: {url}")

# Example JSON array with image URLs
json_array = [{}]

# Specify the folder where the images should be saved
save_folder = "imgs"  # Relative path to a folder named "images"

# Create the folder if it doesn't exist
os.makedirs(save_folder, exist_ok=True)
n = 0
# Download images from URLs in the JSON array
for item in json_array:
    image_url = item['url']
    file_name = str(n) + "-image.png"  # Extract file name from the URL
    file_path = os.path.join(save_folder, file_name)  # Create the file path
    download_image(image_url, file_path)
    n += 1
