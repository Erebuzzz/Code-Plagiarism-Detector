import requests
import json

# Test the similarity check with simple code
data = {
    "code1": "def hello():\n    print('Hello World')",
    "code2": "def greet():\n    print('Hello World')"
}

try:
    response = requests.post(
        'http://localhost:5003/check',
        headers={'Content-Type': 'application/json'},
        json=data
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
except Exception as e:
    print(f"Error: {e}")
