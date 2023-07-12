import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

with open('logs.json', 'r') as f:
    data = json.load(f)

doc = SimpleDocTemplate("comic.pdf", pagesize=letter)
story = []
table_data = []
styles = getSampleStyleSheet()

for i in range(0, len(data), 2):
    row_images = []
    row_texts = []
    for j in range(2):
        if i + j < len(data):
            item = data[i + j]
            # Load the image from the specified location
            img = Image(f"imgs/{(i + j)}-image.png", 200, 200)
            # Add the description from the JSON data
            para = Paragraph(item["content"], styles["BodyText"])
            # Add the image and description to the row
            row_images.append(img)
            row_texts.append(para)
    # Add the image and description to a row in the table data
    table_data.append(row_images)
    table_data.append(row_texts)

# Create a table with the data and add a border and some padding
table = Table(table_data)
table.setStyle(TableStyle([
    ('BOX', (0,0), (-1,-1), 1, colors.black),
    ('GRID', (0,0), (-1,-1), 1, colors.black),
    ('PAD', (0,0), (-1,-1), 10),
]))

story.append(table)
doc.build(story)
