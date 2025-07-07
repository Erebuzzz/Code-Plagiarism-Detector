#!/usr/bin/env python3
import requests
import json

code1 = '''def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)'''

code2 = '''def quick_sort(array):
    if len(array) <= 1:
        return array
    pivot_element = array[len(array) // 2]
    smaller = [item for item in array if item < pivot_element]
    equal = [item for item in array if item == pivot_element]
    larger = [item for item in array if item > pivot_element]
    return quick_sort(smaller) + equal + quick_sort(larger)'''

# Test detailed comparison
response = requests.post('http://localhost:8000/detailed-check', 
                        json={'code1': code1, 'code2': code2})

if response.status_code == 200:
    result = response.json()
    print('Structure Analysis:')
    print(f"Code 1 - Lines: {result['code1_analysis']['structure']['lines']}, Functions: {result['code1_analysis']['structure']['functions']}")
    print(f"Code 2 - Lines: {result['code2_analysis']['structure']['lines']}, Functions: {result['code2_analysis']['structure']['functions']}")
    print()
    print('Complexity Analysis:')
    print(f"Code 1 - Cyclomatic: {result['code1_analysis']['complexity']['cyclomatic']}")
    print(f"Code 2 - Cyclomatic: {result['code2_analysis']['complexity']['cyclomatic']}")
    print()
    print('Comparison Insights:')
    insights = result.get('comparison_insights', {})
    for category, insight_list in insights.items():
        print(f'{category}:')
        for insight in insight_list:
            print(f'  - {insight}')
else:
    print(f'Error: {response.status_code} - {response.text}')
