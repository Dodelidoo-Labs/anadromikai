import openai
from sentence_transformers import SentenceTransformer
from transformers import BartForConditionalGeneration, BartTokenizer
import os
from dotenv import load_dotenv

print("Loading Environment...")
# Load environment variables
load_dotenv(".env")
print("Loading OpenAI...")
openai.api_key = os.getenv("TOKEN")
print("Loading SenteceTransformer...")
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
print("Loading BART...")
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
summarizer = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
print("Define Helper Methods...")
def generate_content(prompt, tokens=1000):
    response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=[
            {"role": "system", "content": "You are a book author and write a Book which is set in the future. The Book is about a family: Ana (the mother), Drom (the father), Ikai (the daughter), and Anadromikai (an Artificial Intelligence). The user is providing you a summary of what was written so far, a last sentence, and you will follow up to that, with a continuation of the Book. Th writing style is slow paced, detailed, a mix of conversation and scene/action descriptions. The book is written from the perspective of a fourth entity, which will reveal itself to the reader only by reading between the lines, and you will never explicitly mention there is a fourth entity."},
            {"role": "user", "content": prompt}
        ],
      max_tokens=tokens
    )
    return response.choices[0].message['content'].strip()
def embed_text(text):
    return model.encode([text])[0]
def chunk_content(content, chunk_size=800):
    """Split the content into chunks of a specified size."""
    return [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
def summarize_chunks(content, chunk_size=800):
    """Summarize content by chunking and then combining the summaries."""
    chunks = chunk_content(content, chunk_size)
    summaries = [generate_summary(chunk) for chunk in chunks]
    return ' '.join(summaries)
def generate_summary(text):
    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = summarizer.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)
print("Define Variables...")
file_name = "generated_book.txt"
initial_summary = input("Enter the summary of what happened so far (primer): ")
initial_sentence = input("Enter the last sentence (from which the book will start): ")
primer_prompt = f"Summary: '{initial_summary}', Last Sentence: '{initial_sentence}'."
print("Generating Book Opening Sentences...")
book_content = generate_content(primer_prompt)
with open(file_name, 'w') as file:
    file.write(book_content + "\n\n" + "Next")
while True:
    book_summary = summarize_chunks(book_content)
    print("Summary of existing book created...")
    last_sentence = book_content.split('.')[-2] + '.'
    continuation_prompt = f"Summary: '{book_summary}', Last sentence: '{last_sentence}'"
    new_content = generate_content(continuation_prompt)
    print("Follow up content generated...")
    if new_content in book_content:
        print("Detected repetition. Stopping generation.")
        break

    book_content += "\n\n" + new_content
    with open(file_name, 'a') as file:
        file.write("\n\n" + new_content + "\n\n" + "Next")
    user_input = input("Press Enter to continue or type 'stop' to end: ").strip().lower()
    if user_input == 'stop':
        break

print("Book generation completed!")
