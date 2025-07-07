#!/usr/bin/env python3
import requests
import json

code = '''def factorial(n):
    """Calculate factorial of a number"""
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)

def main():
    print("Factorial of 5:", factorial(5))
    print("Factorial of 0:", factorial(0))

if __name__ == "__main__":
    main()'''

# Test single code analysis
response = requests.post('http://localhost:8000/analyze', 
                        json={'code': code})

if response.status_code == 200:
    result = response.json()
    print('Structure Analysis:')
    print(f"Lines: {result['structure']['lines']}")
    print(f"Functions: {result['structure']['functions']}")
    print(f"Classes: {result['structure']['classes']}")
    print(f"Comments: {result['structure']['comments']}")
    print()
    print('Complexity Analysis:')
    print(f"Cyclomatic: {result['complexity']['cyclomatic']}")
    print(f"Maintainability Index: {result['complexity']['maintainability_index']:.1f}")
    print()
    print('AI Detection:')
    print(f"AI Generated: {result['ai_detection']['is_ai_generated']}")
    print(f"Confidence: {result['ai_detection']['confidence']:.1f}%")
    print()
    print('Insights:')
    for insight in result.get('insights', []):
        print(f'  - {insight}')
else:
    print(f'Error: {response.status_code} - {response.text}')
