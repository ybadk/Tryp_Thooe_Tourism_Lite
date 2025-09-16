import os
import re


def remove_special_characters(text):
    # Define the pattern to keep only letters, numbers, and spaces
    pattern = r'[^a-zA-Z0-9\s]'
    text = re.sub(pattern, '', text)
    return text


# Path to the South Africa folder
folder_path = 'text_training_data/Tshwane'

# Iterate over the files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        # Read the file
        with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
            text = file.read()

        # Remove special characters
        text = remove_special_characters(text)

        # Write the modified text back to the file
        with open(os.path.join(folder_path, filename), 'w', encoding='utf-8') as file:
            file.write(text)
