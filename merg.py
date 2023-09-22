import csv

csv_file = '/path/to/csv.csv'  # Replace with the path to your CSV file
txt_file = 'new.txt'  # Replace with the desired path for the output text file

with open(csv_file, 'r') as file:
    reader = csv.reader(file)
    column_3_contents = [row[2] for row in reader]  # Extract column 3 contents

merged_contents = ' '.join(column_3_contents)  # Merge contents with spaces

with open(txt_file, 'w') as file:
    file.write(merged_contents)
