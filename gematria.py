import math
import requests
import json
import re
import csv

def compute_gematria(word):
    gematria_dict = {
    'א': 1,
    'ב': 2,
    'ג': 3,
    'ד': 4,
    'ה': 5,
    'ו': 6,
    'ז': 7,
    'ח': 8,
    'ט': 9,
    'י': 10,
    'כ': 20,
    'ל': 30,
    'מ': 40,
    'נ': 50,
    'ס': 60,
    'ע': 70,
    'פ': 80,
    'צ': 90,
    'ק': 100,
    'ר': 200,
    'ש': 300,
    'ת': 400,
    'ך': 20,  # Final form of 'כ'
    'ם': 40,  # Final form of 'מ'
    'ן': 50,  # Final form of 'נ'
    'ף': 80,  # Final form of 'פ'
    'ץ': 90,  # Final form of 'צ'
}

    total = 0
    for letter in word:
        if letter in gematria_dict:
            total += gematria_dict[letter]

    return total



def process_paragraph(paragraph):
    paragraph = paragraph.split('׃')[0]
    paragraph = paragraph.replace('[', '').replace(']', '').replace('(', '').replace(')', '')

    # Split the paragraph into words using regular expression
    words = re.split(r'\s+|־', paragraph)

    # Compute gematria for each word
    gematria_per_word = [(word, compute_gematria(word)) for word in words]

    # Compute gematria for the entire paragraph
    total_gematria = sum(gematria for word, gematria in gematria_per_word)

    return paragraph, total_gematria

# def smallest_non_trivial_divisor(num):
#     # Special case for 2
#     if num % 2 == 0:
#         return 2

#     # Loop to check divisors starting from 3 up to the square root of the number
#     for divisor in range(3, int(math.sqrt(num)) + 1, 2):
#         if num % divisor == 0:
#             return divisor

#     # If no divisor is found, the number is prime
#     return None

def create_csv_file(filename, data):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Phrase', 'Total Gematria Value'])
        writer.writerows(data)

all_data = []
for book_num in range(1, 40):
    for chapter_num in range(1, 100):  # Use a sufficiently large range for chapter numbers
        url = f'https://bolls.life/get-text/WLCC/{book_num}/{chapter_num}/'
        chapter_response = requests.get(url)
        if chapter_response.status_code == 200:
            chapter = json.loads(chapter_response.text)
            for verse in chapter:
                verse_text = verse['text']
                phrase, total_gematria = process_paragraph(verse_text)
                all_data.append([phrase, total_gematria])

# Write the data to a CSV file
create_csv_file('gematria_data.csv', all_data)

# # Fetch the list of available translations
# chapter_response = requests.get('https://bolls.life/get-text/WLCC/36/1/')
# chapter = json.loads(chapter_response.text)

# for verse in chapter:
#     process_paragraph(verse['text'])

# numbers_set = set(numbers)  # Convert list to set for faster lookup
# res = 0
# for num in numbers:
#     res += num
#     print(str(num) + ': ', str(smallest_non_trivial_divisor(num)) + '(' + str(res) + ')')
# # Check for sums and products
# for i in range(len(numbers)):
#     for j in range(i+1, len(numbers)):  # Avoid checking a pair twice
#         sum_ij = numbers[i] + numbers[j]
#         if sum_ij in numbers_set:
#             print(f"{numbers[i]} + {numbers[j]} = {sum_ij}")
        
#         product_ij = numbers[i] * numbers[j]
#         if product_ij in numbers_set:
#             print(f"{numbers[i]} * {numbers[j]} = {product_ij}")

# # Check for differences
# for i in range(len(numbers)):
#     for j in range(len(numbers)):
#         if i != j:  # Avoid checking the same number
#             diff_ij = abs(numbers[i] - numbers[j])
#             if diff_ij in numbers_set:
#                 print(f"{numbers[i]} - {numbers[j]} = {diff_ij}")

# # Check for divisions
# for i in range(len(numbers)):
#     for j in range(len(numbers)):
#         if i != j and numbers[j] != 0:  # Avoid division by zero and checking the same number
#             division_ij = numbers[i] / numbers[j]
#             if division_ij in numbers_set:
#                 print(f"{numbers[i]} / {numbers[j]} = {division_ij}")