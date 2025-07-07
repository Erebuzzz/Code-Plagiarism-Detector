#!/usr/bin/env python3
"""
Demo script for AI Code Plagiarism Detector
Shows various similarity scenarios
"""

import requests
import json
import time

def demo_similarity_check(title, code1, code2, expected_similarity="Unknown"):
    """Demo a similarity check with explanation"""
    print(f"\n{'='*60}")
    print(f"🔍 DEMO: {title}")
    print(f"Expected Similarity: {expected_similarity}")
    print('='*60)
    
    print("\n📝 Code Snippet 1:")
    print("-" * 30)
    print(code1.strip())
    
    print("\n📝 Code Snippet 2:")
    print("-" * 30)
    print(code2.strip())
    
    print("\n⏳ Analyzing similarity...")
    
    try:
        response = requests.post(
            "http://localhost:5000/check",
            headers={"Content-Type": "application/json"},
            json={"code1": code1, "code2": code2},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print("\n📊 RESULTS:")
            print("-" * 20)
            
            for model, score in result.items():
                if model == 'FinalVerdict':
                    print(f"🎯 {model}: {score}%")
                else:
                    print(f"🤖 {model}: {score}%")
            
            # Interpretation
            final_score = result.get('FinalVerdict', 0)
            if final_score >= 80:
                print("\n🔴 HIGH SIMILARITY - Potential plagiarism detected!")
            elif final_score >= 60:
                print("\n🟡 MODERATE SIMILARITY - Review recommended")
            elif final_score >= 40:
                print("\n🔵 LOW SIMILARITY - Some common patterns found")
            else:
                print("\n🟢 VERY LOW SIMILARITY - Likely original code")
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Server not running. Start with: python main.py")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    input("\nPress Enter to continue...")

def run_demo():
    """Run the complete demo"""
    print("🎭 AI Code Plagiarism Detector - DEMO")
    print("=" * 50)
    print("This demo will show different similarity scenarios")
    print("Make sure the server is running: python main.py")
    input("\nPress Enter to start...")
    
    # Demo 1: Identical code
    demo_similarity_check(
        "Identical Code (Copy-Paste)",
        """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)

print(factorial(5))
        """,
        """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)

print(factorial(5))
        """,
        "Very High (90%+)"
    )
    
    # Demo 2: Renamed variables
    demo_similarity_check(
        "Renamed Variables (Minor Changes)",
        """
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

result = calculate_sum([1, 2, 3, 4, 5])
        """,
        """
def compute_total(values):
    sum_val = 0
    for value in values:
        sum_val += value
    return sum_val

answer = compute_total([1, 2, 3, 4, 5])
        """,
        "High (80-90%)"
    )
    
    # Demo 3: Different algorithms, same purpose
    demo_similarity_check(
        "Different Algorithms (Same Purpose)",
        """
def fibonacci_recursive(n):
    if n <= 1:
        return n
    return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)

for i in range(10):
    print(fibonacci_recursive(i))
        """,
        """
def fibonacci_iterative(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

for i in range(10):
    print(fibonacci_iterative(i))
        """,
        "Moderate (50-70%)"
    )
    
    # Demo 4: Completely different code
    demo_similarity_check(
        "Completely Different Code",
        """
class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    
    def start_engine(self):
        print(f"{self.brand} {self.model} engine started!")

my_car = Car("Toyota", "Camry")
my_car.start_engine()
        """,
        """
import math

def calculate_circle_area(radius):
    return math.pi * radius ** 2

def calculate_circumference(radius):
    return 2 * math.pi * radius

radius = 5
area = calculate_circle_area(radius)
circumference = calculate_circumference(radius)
        """,
        "Very Low (0-30%)"
    )
    
    # Demo 5: Refactored code
    demo_similarity_check(
        "Refactored Code (Structural Changes)",
        """
def process_data(data):
    if len(data) == 0:
        return None
    
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    
    return result

numbers = [1, -2, 3, -4, 5]
processed = process_data(numbers)
        """,
        """
def transform_positive_numbers(input_list):
    return [x * 2 for x in input_list if x > 0] if input_list else None

data = [1, -2, 3, -4, 5]
output = transform_positive_numbers(data)
        """,
        "Moderate to High (60-80%)"
    )
    
    print("\n🎉 Demo completed!")
    print("\nKey Takeaways:")
    print("- Identical code: 90%+ similarity")
    print("- Renamed variables: 80-90% similarity") 
    print("- Different algorithms: 50-70% similarity")
    print("- Completely different: 0-30% similarity")
    print("- Refactored code: 60-80% similarity")
    print("\nThreshold recommendations:")
    print("- 80%+ = Investigate for plagiarism")
    print("- 60-80% = Review recommended")
    print("- 40-60% = Minor similarities")
    print("- <40% = Likely original")

if __name__ == "__main__":
    run_demo()
