import os
import pandas as pd
from openai import OpenAI
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from dotenv import load_dotenv
import chardet

# Load environment variables
load_dotenv()
ELASTICSEARCH_ENDPOINT = os.getenv('elasticsearchendpoint')
ELASTIC_API_KEY = os.getenv('elasticapikey')

# Connect to Elasticsearch
es = Elasticsearch(ELASTICSEARCH_ENDPOINT, api_key=ELASTIC_API_KEY)
openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Columns to fetch from Elasticsearch
columns = ["Study Title", "Brief Summary", "Study Description"]

def detect_encoding(file_path):
    """Detect file encoding."""
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def fetch_data():
    """Fetch data from Elasticsearch."""
    search = Search(using=es, index="clinicaltrial").source(columns)
    results = search[0:7000].execute()
    data = [{field: hit[field] for field in columns if field in hit} for hit in results]
    return pd.DataFrame(data)

def summarize_text(prompt):
    """Summarize text using OpenAI."""
    task_prompt = f"Summarize the following text:\n{prompt}"
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": task_prompt}]
    )
    return response.choices[0].message.content.strip()

def translate_text(prompt, target_language="es"):
    """Translate text using OpenAI."""
    task_prompt = f"Translate the following text to {target_language}:\n{prompt}"
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": task_prompt}]
    )
    return response.choices[0].message.content.strip()

def generate_summary_dataset(data, checkpoint_file=r"C:\Users\nirmiti.deshmukh\Mindgram\finetune_data\summarization_dataset.csv"):
    """Create summarization dataset with checkpointing."""
    # Load checkpoint
    if os.path.exists(checkpoint_file):
        try:
            encoding = detect_encoding(checkpoint_file)
            completed_df = pd.read_csv(checkpoint_file, encoding=encoding)
            completed_indices = set(completed_df['Index'])
            print(f"Resuming from checkpoint. {len(completed_indices)} rows already processed.")
        except Exception as e:
            print(f"Error reading checkpoint file: {e}. Starting from scratch.")
            completed_df = pd.DataFrame(columns=['Index', 'Input', 'Output'])
            completed_indices = set()
    else:
        completed_df = pd.DataFrame(columns=['Index', 'Input', 'Output'])
        completed_indices = set()

    # Process data
    with open(checkpoint_file, mode='a', encoding='utf-8') as f:
        for i, row in data.iterrows():
            if i in completed_indices:  # Skip already processed rows
                continue

            try:
                input_text = f"{row.get('Study Title', '')}\n{row.get('Brief Summary', '')}\n{row.get('Study Description', '')}"
                summary = summarize_text(input_text)
                row_data = {'Index': i, 'Input': input_text, 'Summary': summary}
                pd.DataFrame([row_data]).to_csv(f, header=f.tell() == 0, index=False, encoding='utf-8')
                f.flush()
                print(f"[Summarization] Processed row {i + 1}/{len(data)}")
            except Exception as e:
                print(f"Error processing row {i}: {e}. Retrying...")
                break

    print("Summarization task completed.")

def generate_translation_dataset(data, checkpoint_file=r"C:\Users\nirmiti.deshmukh\Mindgram\finetune_data\translation_dataset.csv", target_language="es"):
    """Create translation dataset with checkpointing."""
    # Load checkpoint
    if os.path.exists(checkpoint_file):
        try:
            encoding = detect_encoding(checkpoint_file)
            completed_df = pd.read_csv(checkpoint_file, encoding=encoding)
            completed_indices = set(completed_df['Index'])
            print(f"Resuming from checkpoint. {len(completed_indices)} rows already processed.")
        except Exception as e:
            print(f"Error reading checkpoint file: {e}. Starting from scratch.")
            completed_df = pd.DataFrame(columns=['Index', 'Input', 'Output'])
            completed_indices = set()
    else:
        completed_df = pd.DataFrame(columns=['Index', 'Input', 'Output'])
        completed_indices = set()

    # Process data
    with open(checkpoint_file, mode='a', encoding='utf-8') as f:
        for i, row in data.iterrows():
            if i in completed_indices:  # Skip already processed rows
                continue

            try:
                input_text = f"{row.get('Study Title', '')}\n{row.get('Brief Summary', '')}\n{row.get('Study Description', '')}"
                translation = translate_text(input_text, target_language)
                row_data = {'Index': i, 'Input': input_text, 'Translation': translation}
                pd.DataFrame([row_data]).to_csv(f, header=f.tell() == 0, index=False, encoding='utf-8')
                f.flush()
                print(f"[Translation] Processed row {i + 1}/{len(data)}")
            except Exception as e:
                print(f"Error processing row {i}: {e}. Retrying...")
                break

    print("Translation task completed.")

def main():
    print("Fetching data from Elasticsearch...")
    data = fetch_data()
    if not data.empty:
        print(f"Processing {len(data)} rows...")
        # Task 1: Generate summarization dataset
        generate_summary_dataset(data)

        # Task 2: Generate translation dataset
        generate_translation_dataset(data, target_language="es")
    else:
        print("No data found in Elasticsearch.")

if __name__ == "__main__":
    main()

# elasticsearchendpoint=https://a25cbf64ca0d465a9d3eb5d9479121b6.eastus2.azure.elastic-cloud.com:443
# elasticapikey='OS1va2ZaSUJSVGZpcTdOYXFpX3A6YkJKRGp3TFdRT09aUkZqOGVQSWpEdw=='
