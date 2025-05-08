import os
import json
import pandas as pd
from datasets import Dataset
from huggingface_hub import login
from dotenv import load_dotenv
load_dotenv()
def read_json_files(folder_path):
    """Read JSON files from a folder and return a list of data."""
    json_files_data = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    json_files_data.append((filename, data))
            except json.JSONDecodeError:
                print(f"Error decoding JSON from {file_path}")
    
    return json_files_data

def extract_plain_text(json_obj):
    if isinstance(json_obj, str):
        return json_obj
    elif isinstance(json_obj, (int, float, bool)):
        return str(json_obj)
    elif isinstance(json_obj, dict):
        parts = []
        for k, v in json_obj.items():
            text = extract_plain_text(v).strip()
            if text:
                parts.append(f"{k}\n{text}")
        return "\n\n".join(parts)
    elif isinstance(json_obj, list):
        parts = []
        for item in json_obj:
            t = extract_plain_text(item).strip()
            if t:
                parts.append(f"- {t}")
        return "\n".join(parts)
    elif json_obj is None:
        return ""
    else:
        return str(json_obj)



def create_dataframe(json_files_data):
    data = { 'desease':[], 'content':[], 'content_json':[], 'type_desease':[] }
    for filename, json_obj in json_files_data:
        type_disease = filename.replace('.json','')
        # Chuẩn hoá thành list of dict
        if isinstance(json_obj, dict):
            records = []
            for key, value in json_obj.items():
                if isinstance(value, dict):
                    record = {'Bệnh': key, **value}
                else:
                    record = {'Bệnh': key, 'Nội dung': value}
                records.append(record)
        elif isinstance(json_obj, list):
            records = json_obj
        else:
            continue

        for disease_data in records:
            disease = disease_data.get('Bệnh','')
            if disease == "TÀI LIỆU THAM KHẢO":
                continue
            content_text = extract_plain_text(disease_data)
            content_json = json.dumps(disease_data, ensure_ascii=False)
            data['desease'].append(disease)
            data['content'].append(content_text)
            data['content_json'].append(content_json)
            data['type_desease'].append(type_disease)
    return pd.DataFrame(data)


def push_to_huggingface(df, repo_id, token=None):
    """Push the DataFrame to Hugging Face."""
    if token:
        login(token)
    
    dataset = Dataset.from_pandas(df)
    dataset.push_to_hub(repo_id)
    print(f"Successfully pushed dataset to {repo_id}")

def main():
    # Get parameters
    json_folder_path = "data/json"
    hf_repo_id = "codin-research/benh-hoc-corpus-raw"
    hf_token = os.getenv("HF_TOKEN")
    
    # Read JSON files
    print("Reading JSON files...")
    json_files_data = read_json_files(json_folder_path)
    print(f"Found {len(json_files_data)} JSON files.")
    
    if not json_files_data:
        print("No JSON data found. Exiting.")
        return
    
    # Create DataFrame
    print("Processing JSON data...")
    df = create_dataframe(json_files_data)
    print(f"Created DataFrame with {len(df)} records.")
    
    df.to_json(
        "push_data/data_merge_v1.json",
        orient="records",
        force_ascii=False,
        indent=2
    )    # Display sample
    confirm = input("\nDo you want to push this data to Hugging Face? (y/n): ")

    print("\nSample of the DataFrame:")
    pd.set_option('display.max_colwidth', 50)
    print(df.head())

    df = pd.read_json("push_data/data_merge_v1.json")
    
    # Confirm before pushing
    if confirm.lower() == 'y':
        try:
            print("Pushing to Hugging Face...")
            push_to_huggingface(df, hf_repo_id, hf_token)
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Operation cancelled.")

if __name__ == "__main__":
    main()