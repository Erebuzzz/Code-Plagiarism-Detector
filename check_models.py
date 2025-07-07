import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('TOGETHER_API_KEY')

response = requests.get(
    'https://api.together.ai/models',
    headers={'Authorization': f'Bearer {api_key}'}
)

if response.status_code == 200:
    models = response.json()
    print("Available embedding models:")
    for model in models:
        if 'embed' in model.get('id', '').lower() or 'bge' in model.get('id', '').lower():
            print(f"- {model.get('id')}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
