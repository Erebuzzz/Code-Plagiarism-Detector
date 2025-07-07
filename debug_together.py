#!/usr/bin/env python3
"""
Debug Together.ai API calls
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_together_api():
    """Test Together.ai API with detailed debugging"""
    
    api_key = os.getenv('TOGETHER_API_KEY')
    print(f"API Key (first 10 chars): {api_key[:10]}..." if api_key else "No API key found")
    
    if not api_key:
        print("❌ No Together.ai API key found in .env file")
        return
    
    # Test code sample
    test_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
    
    # Try different models and endpoints
    models_to_test = [
        'togethercomputer/m2-bert-80M-8k-retrieval',
        'sentence-transformers/all-MiniLM-L6-v2',
        'BAAI/bge-base-en-v1.5',
        'sentence-transformers/all-mpnet-base-v2'
    ]
    
    for model in models_to_test:
        print(f"\n🧪 Testing model: {model}")
        print("-" * 50)
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': model,
            'input': test_code
        }
        
        try:
            response = requests.post(
                'https://api.together.xyz/v1/embeddings',
                headers=headers,
                json=data,
                timeout=30
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success!")
                print(f"Response structure: {list(result.keys())}")
                
                if 'data' in result and len(result['data']) > 0:
                    embedding = result['data'][0]['embedding']
                    print(f"Embedding length: {len(embedding)}")
                    print(f"First 5 values: {embedding[:5]}")
                    print(f"Embedding type: {type(embedding)}")
                    return embedding
                else:
                    print(f"❌ Unexpected response structure: {result}")
            else:
                print(f"❌ Error {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"Error details: {json.dumps(error_detail, indent=2)}")
                except:
                    print(f"Error text: {response.text}")
                    
        except requests.exceptions.Timeout:
            print("❌ Request timeout")
        except requests.exceptions.ConnectionError:
            print("❌ Connection error")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
    
    # Test alternative endpoint
    print(f"\n🧪 Testing alternative endpoint...")
    print("-" * 50)
    
    try:
        # Try the inference endpoint instead
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'sentence-transformers/all-MiniLM-L6-v2',
            'input': test_code
        }
        
        response = requests.post(
            'https://api.together.xyz/inference',
            headers=headers,
            json=data,
            timeout=30
        )
        
        print(f"Alternative endpoint - Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Alternative endpoint result: {result}")
        else:
            print(f"Alternative endpoint error: {response.text}")
            
    except Exception as e:
        print(f"Alternative endpoint error: {e}")

if __name__ == "__main__":
    print("🔍 Together.ai API Debug Tool")
    print("=" * 50)
    test_together_api()
