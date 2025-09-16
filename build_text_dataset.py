import os
import csv
import json
import glob
import html
from bs4 import BeautifulSoup
from pathlib import Path
import pdfplumber

DATASET_PATH = 'unified_text_dataset.jsonl'

# Folders to scan
FOLDERS = [
    'all-rag-techniques-main',
    'system-prompts-and-models-of-ai-tools-main',
    'processed_places_data',
    'processed_data',
    'crawled_data',
    'tshwane_crawled_data',
    'tshwane_website_clone',
]

EXTENSIONS = ['.csv', '.json', '.html', '.htm', '.txt', '.md', '.pdf']

def extract_csv(file_path):
    rows = []
    with open(file_path, encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        for row in reader:
            content = ', '.join([f"{h}: {v}" for h, v in zip(headers, row)]) if headers else ', '.join(row)
            rows.append(content)
    return rows

def extract_json(file_path):
    with open(file_path, encoding='utf-8', errors='ignore') as f:
        data = json.load(f)
    if isinstance(data, list):
        return [json.dumps(item, ensure_ascii=False) for item in data]
    elif isinstance(data, dict):
        return [json.dumps(data, ensure_ascii=False)]
    return []

def extract_html(file_path):
    with open(file_path, encoding='utf-8', errors='ignore') as f:
        soup = BeautifulSoup(f, 'html.parser')
        # Remove scripts/styles
        for tag in soup(['script', 'style']):
            tag.decompose()
        text = soup.get_text(separator=' ', strip=True)
    return [text]

def extract_txt(file_path):
    with open(file_path, encoding='utf-8', errors='ignore') as f:
        return [f.read()]

def extract_pdf(file_path):
    texts = []
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                texts.append(page.extract_text() or '')
    except Exception as e:
        print(f"PDF extraction failed for {file_path}: {e}")
    return texts

def extract_file(file_path):
    ext = Path(file_path).suffix.lower()
    if ext == '.csv':
        return extract_csv(file_path)
    elif ext == '.json':
        return extract_json(file_path)
    elif ext in ['.html', '.htm']:
        return extract_html(file_path)
    elif ext in ['.txt', '.md']:
        return extract_txt(file_path)
    elif ext == '.pdf':
        return extract_pdf(file_path)
    return []

def main():
    dataset = []
    for folder in FOLDERS:
        for root, dirs, files in os.walk(folder):
            for file in files:
                ext = Path(file).suffix.lower()
                if ext in EXTENSIONS:
                    file_path = os.path.join(root, file)
                    print(f"Extracting from {file_path}")
                    try:
                        contents = extract_file(file_path)
                        for content in contents:
                            dataset.append({
                                'source': file_path,
                                'type': ext.lstrip('.'),
                                'content': content.strip(),
                            })
                    except Exception as e:
                        print(f"Failed to extract {file_path}: {e}")
    # Write to JSONL
    with open(DATASET_PATH, 'w', encoding='utf-8') as f:
        for item in dataset:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    print(f"Dataset written to {DATASET_PATH} with {len(dataset)} entries.")

if __name__ == '__main__':
    main() 