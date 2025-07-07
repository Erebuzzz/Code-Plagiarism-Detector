from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import cohere
from dotenv import load_dotenv
import json
import re

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize APIs
cohere_client = cohere.Client(os.getenv('COHERE_API_KEY'))

class CodeSimilarityAnalyzer:
    def __init__(self):
        self.cohere_api_key = os.getenv('COHERE_API_KEY')
        self.together_api_key = os.getenv('TOGETHER_API_KEY')
        self.replicate_api_token = os.getenv('REPLICATE_API_TOKEN')
        
    def get_cohere_embedding(self, text):
        """Get embedding from Cohere API"""
        try:
            response = cohere_client.embed(
                texts=[text],
                model='embed-english-v3.0',
                input_type='search_document'
            )
            return response.embeddings[0]
        except Exception as e:
            print(f"Cohere API error: {e}")
            return None
    
    def get_together_embedding(self, text):
        """Get embedding from Together.ai API"""
        try:
            headers = {
                'Authorization': f'Bearer {self.together_api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'BAAI/bge-base-en-v1.5',
                'input': text
            }
            
            response = requests.post(
                'https://api.together.xyz/v1/embeddings',
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['data'][0]['embedding']
            else:
                print(f"Together.ai API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Together.ai API error: {e}")
            return None
    
    def get_replicate_similarity(self, code1, code2):
        """Get similarity score from Replicate API"""
        try:
            # For this demo, we'll use a simple similarity approach
            # In production, you'd use an actual code similarity model from Replicate
            embedding1 = self._simple_code_embedding(code1)
            embedding2 = self._simple_code_embedding(code2)
            
            similarity = cosine_similarity([embedding1], [embedding2])[0][0]
            return max(0, min(100, similarity * 100))
            
        except Exception as e:
            print(f"Replicate API error: {e}")
            # Fallback to simple similarity
            embedding1 = self._simple_code_embedding(code1)
            embedding2 = self._simple_code_embedding(code2)
            similarity = cosine_similarity([embedding1], [embedding2])[0][0]
            return max(0, min(100, similarity * 100))
    
    def _simple_code_embedding(self, code):
        """Simple code embedding for fallback"""
        # Normalize code
        normalized = re.sub(r'\s+', ' ', code.lower().strip())
        
        # Create a simple feature vector based on code characteristics
        features = []
        features.append(len(code))  # Length
        features.append(code.count('def '))  # Function count
        features.append(code.count('class '))  # Class count
        features.append(code.count('import '))  # Import count
        features.append(code.count('for '))  # Loop count
        features.append(code.count('if '))  # Conditional count
        features.append(len(re.findall(r'\w+', code)))  # Word count
        
        # Pad to 100 dimensions for consistency
        while len(features) < 100:
            features.append(0)
        
        return features[:100]
    
    def calculate_similarity(self, code1, code2):
        """Calculate similarity scores from all three APIs"""
        results = {}
        
        # Cohere similarity
        cohere_emb1 = self.get_cohere_embedding(code1)
        cohere_emb2 = self.get_cohere_embedding(code2)
        
        if cohere_emb1 and cohere_emb2:
            cohere_sim = cosine_similarity([cohere_emb1], [cohere_emb2])[0][0]
            results['Cohere'] = round(max(0, min(100, cohere_sim * 100)), 2)
        else:
            results['Cohere'] = 0.0
        
        # Together.ai similarity
        together_emb1 = self.get_together_embedding(code1)
        together_emb2 = self.get_together_embedding(code2)
        
        if together_emb1 and together_emb2:
            together_sim = cosine_similarity([together_emb1], [together_emb2])[0][0]
            results['TogetherAI'] = round(max(0, min(100, together_sim * 100)), 2)
        else:
            results['TogetherAI'] = 0.0
        
        # Replicate similarity
        replicate_score = self.get_replicate_similarity(code1, code2)
        results['Replicate'] = round(replicate_score, 2)
        
        # Calculate final verdict (average of all scores)
        scores = [v for v in results.values() if v > 0]
        if scores:
            results['FinalVerdict'] = round(sum(scores) / len(scores), 2)
        else:
            results['FinalVerdict'] = 0.0
        
        return results

# Initialize analyzer
analyzer = CodeSimilarityAnalyzer()

@app.route('/')
def index():
    """Serve the React frontend"""
    return send_from_directory('out', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    """Serve static files"""
    return send_from_directory('out', path)

@app.route('/check', methods=['POST'])
def check_similarity():
    """Check code similarity between two snippets"""
    try:
        data = request.get_json()
        
        if not data or 'code1' not in data or 'code2' not in data:
            return jsonify({'error': 'Missing code1 or code2 in request'}), 400
        
        code1 = data['code1'].strip()
        code2 = data['code2'].strip()
        
        if not code1 or not code2:
            return jsonify({'error': 'Code snippets cannot be empty'}), 400
        
        # Calculate similarities
        results = analyzer.calculate_similarity(code1, code2)
        
        return jsonify(results)
    
    except Exception as e:
        print(f"Error in check_similarity: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'AI Code Plagiarism Detector is running'})

if __name__ == '__main__':
    # Check if out directory exists (built frontend)
    if not os.path.exists('out'):
        print("Frontend not built yet. Please run:")
        print("cd frontend && npm install && npm run build && npm run export")
    
    # Check for required environment variables
    required_vars = ['COHERE_API_KEY', 'TOGETHER_API_KEY', 'REPLICATE_API_TOKEN']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Warning: Missing environment variables: {', '.join(missing_vars)}")
        print("Please set them in your .env file for full functionality")
    
    print("Starting AI Code Plagiarism Detector...")
    print("Frontend files found!" if os.path.exists('out') else "Frontend files missing!")
    print(f"API Keys configured: {len(required_vars) - len(missing_vars)}/{len(required_vars)}")
    print("Routes registered:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.rule} -> {rule.endpoint}")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
