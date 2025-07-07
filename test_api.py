#!/usr/bin/env python3
"""
Test script for the AI Code Plagiarism Detector API
"""

import requests
import json
import sys

def test_api():
    """Test the /check endpoint with sample code"""
    
    base_url = "http://localhost:5000"
    
    # Test data
    test_code1 = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")
"""

    test_code2 = """
def fib(num):
    if num <= 1:
        return num
    return fib(num-1) + fib(num-2)

for j in range(10):
    print(f"Fibonacci({j}) = {fib(j)}")
"""

    # Test health endpoint
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        print()
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Please start the server with: python main.py")
        return False

    # Test similarity check
    print("Testing similarity check...")
    try:
        response = requests.post(
            f"{base_url}/check",
            headers={"Content-Type": "application/json"},
            json={
                "code1": test_code1,
                "code2": test_code2
            }
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Similarity analysis completed!")
            print(json.dumps(result, indent=2))
            
            # Analyze results
            if 'FinalVerdict' in result:
                score = result['FinalVerdict']
                if score >= 80:
                    print(f"\n🔴 High similarity detected: {score}% - Potential plagiarism")
                elif score >= 60:
                    print(f"\n🟡 Moderate similarity: {score}% - Review recommended")
                elif score >= 40:
                    print(f"\n🔵 Low similarity: {score}% - Some common patterns")
                else:
                    print(f"\n🟢 Very low similarity: {score}% - Likely original")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("AI Code Plagiarism Detector - API Test")
    print("=" * 50)
    
    success = test_api()
    
    if success:
        print("\n✅ All tests passed!")
        print("\nYou can now:")
        print("1. Open http://localhost:5000 in your browser")
        print("2. Use the web interface to compare code")
        print("3. Make API calls to /check endpoint")
    else:
        print("\n❌ Tests failed!")
        print("\nMake sure:")
        print("1. The server is running: python main.py")
        print("2. API keys are configured in .env file")
        print("3. Dependencies are installed: pip install -r requirements.txt")
    
    sys.exit(0 if success else 1)
