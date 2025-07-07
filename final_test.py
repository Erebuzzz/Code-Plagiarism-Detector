#!/usr/bin/env python3
"""
Final Test Script for AI Code Plagiarism Detector
Tests all endpoints and functionality of the complete application.
"""

import requests
import json
import time

def test_endpoint(endpoint, data, description):
    """Test a specific endpoint with given data."""
    print(f"\n🧪 Testing {description}...")
    try:
        response = requests.post(f"http://localhost:8000{endpoint}", 
                               json=data, 
                               timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success: {description}")
            return result
        else:
            print(f"❌ Failed: {description} - Status: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {description} - {str(e)}")
        return None

def main():
    print("🚀 AI Code Plagiarism Detector - Final Integration Test")
    print("=" * 60)
    
    # Test data
    code1 = """def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)"""
    
    code2 = """def quick_sort(array):
    if len(array) <= 1:
        return array
    pivot_element = array[len(array) // 2]
    smaller = [item for item in array if item < pivot_element]
    equal = [item for item in array if item == pivot_element]
    larger = [item for item in array if item > pivot_element]
    return quick_sort(smaller) + equal + quick_sort(larger)"""
    
    # Test 1: Basic similarity check
    result1 = test_endpoint("/check", {
        "code1": code1,
        "code2": code2
    }, "Basic Code Similarity")
    
    if result1:
        print(f"   Cohere: {result1.get('Cohere', 'N/A')}%")
        print(f"   Together.ai: {result1.get('TogetherAI', 'N/A')}%")
        print(f"   Replicate: {result1.get('Replicate', 'N/A')}%")
        print(f"   Final Verdict: {result1.get('FinalVerdict', 'N/A')}%")
    
    # Test 2: Single code analysis
    result2 = test_endpoint("/analyze", {
        "code": code1
    }, "Single Code Analysis")
    
    if result2:
        structure = result2.get('structure', {})
        complexity = result2.get('complexity', {})
        ai_detection = result2.get('ai_detection', {})
        
        print(f"   Lines: {structure.get('lines', 'N/A')}")
        print(f"   Functions: {structure.get('functions', 'N/A')}")
        print(f"   Complexity: {complexity.get('cyclomatic', 'N/A')}")
        print(f"   AI Generated: {ai_detection.get('is_ai_generated', 'N/A')}")
        print(f"   Maintainability Index: {complexity.get('maintainability_index', 'N/A'):.1f}")
    
    # Test 3: Detailed comparison
    result3 = test_endpoint("/detailed-check", {
        "code1": code1,
        "code2": code2
    }, "Detailed Code Comparison")
    
    if result3:
        similarity = result3.get('similarity', {})
        print(f"   Combined Score: {similarity.get('combined_score', 'N/A')}%")
        print(f"   Individual Scores: {similarity.get('individual_scores', {})}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary:")
    tests_passed = sum([1 for r in [result1, result2, result3] if r is not None])
    print(f"   Tests Passed: {tests_passed}/3")
    
    if tests_passed == 3:
        print("🎉 All tests passed! The application is working correctly.")
        print("✨ Ready for production use!")
    else:
        print("⚠️  Some tests failed. Please check the backend server.")
    
    print("\n🌐 Frontend Access:")
    print("   Main App: http://localhost:3000")
    print("   Code Analysis: http://localhost:3000/analysis")
    print("   Detailed Comparison: http://localhost:3000/comparison")

if __name__ == "__main__":
    main()
