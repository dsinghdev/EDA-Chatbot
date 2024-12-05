import json
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv(override=True)

hf_token = os.getenv("HUGGINGFACE_API_KEY")
if not hf_token:
    raise ValueError("Hugging Face API token not found. Please set the HF_TOKEN environment variable.")
client = InferenceClient(api_key=hf_token)

def load_eda_insights(insights_path):
    with open(insights_path, "r") as file:
        return json.load(file)

def chatbot_query(eda_insights, user_query):

    prompt = f"""
You are a data insights assistant. Your task is to answer user questions about a dataset 
based on the provided context. Be precise, and use only the context to formulate your response.
    
Context:
Dataset Overview:
- Rows: {eda_insights['shape']['rows']}
- Columns: {eda_insights['shape']['columns']}
- Missing Values: {eda_insights['missing_values']}
- Summary Statistics: {eda_insights['summary_stats']}
    
Question:
{user_query}

Answer:
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    try:
        response = client.chat.completions.create(
        model="Qwen/Qwen2.5-72B-Instruct", 
        messages=messages, 
        temperature=0,
        max_tokens=500,
    )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"An error occurred: {e}"

