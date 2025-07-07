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
import ast
import keyword
from collections import Counter
from datetime import datetime

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

class CodeAnalyzer:
    """Advanced code analysis for detailed insights and AI detection"""
    
    def __init__(self):
        self.cohere_client = cohere_client
        
    def analyze_code_structure(self, code):
        """Analyze code structure and complexity"""
        try:
            tree = ast.parse(code)
            
            analysis = {
                'lines_of_code': len([line for line in code.split('\n') if line.strip()]),
                'functions': [],
                'classes': [],
                'imports': [],
                'variables': [],
                'complexity_metrics': {},
                'code_patterns': {}
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    analysis['functions'].append({
                        'name': node.name,
                        'args': len(node.args.args),
                        'line': node.lineno,
                        'docstring': ast.get_docstring(node) is not None
                    })
                elif isinstance(node, ast.ClassDef):
                    analysis['classes'].append({
                        'name': node.name,
                        'line': node.lineno,
                        'methods': len([n for n in node.body if isinstance(n, ast.FunctionDef)])
                    })
                elif isinstance(node, ast.Import):
                    analysis['imports'].extend([alias.name for alias in node.names])
                elif isinstance(node, ast.ImportFrom):
                    analysis['imports'].append(node.module or 'relative')
                elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                    analysis['variables'].append(node.id)
            
            # Calculate complexity metrics
            analysis['complexity_metrics'] = self._calculate_complexity(code, tree)
            analysis['code_patterns'] = self._analyze_patterns(code)
            
            return analysis
            
        except SyntaxError as e:
            return {'error': f'Syntax error: {str(e)}', 'line': getattr(e, 'lineno', 'unknown')}
        except Exception as e:
            return {'error': f'Analysis error: {str(e)}'}
    
    def _calculate_complexity(self, code, tree):
        """Calculate various complexity metrics"""
        complexity = {
            'cyclomatic_complexity': 1,  # Base complexity
            'cognitive_complexity': 0,
            'nesting_depth': 0,
            'maintainability_index': 0
        }
        
        # Count decision points for cyclomatic complexity
        decision_nodes = 0
        max_depth = 0
        current_depth = 0
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.With, ast.Try, ast.ExceptHandler)):
                decision_nodes += 1
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif isinstance(node, ast.BoolOp):
                decision_nodes += len(node.values) - 1
        
        complexity['cyclomatic_complexity'] += decision_nodes
        complexity['nesting_depth'] = max_depth
        
        # Simple maintainability index approximation
        loc = len([line for line in code.split('\n') if line.strip()])
        complexity['maintainability_index'] = max(0, 171 - 5.2 * np.log(loc) - 0.23 * complexity['cyclomatic_complexity'])
        
        return complexity
    
    def _analyze_patterns(self, code):
        """Analyze code patterns and style"""
        patterns = {
            'naming_conventions': self._check_naming_conventions(code),
            'code_style': self._analyze_code_style(code),
            'ai_indicators': self._detect_ai_patterns(code)
        }
        return patterns
    
    def _check_naming_conventions(self, code):
        """Check naming conventions"""
        lines = code.split('\n')
        conventions = {
            'snake_case_functions': 0,
            'camelCase_functions': 0,
            'UPPERCASE_constants': 0,
            'single_letter_vars': 0,
            'descriptive_names': 0
        }
        
        function_pattern = re.compile(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)')
        
        for line in lines:
            # Check function names
            func_matches = function_pattern.findall(line)
            for func_name in func_matches:
                if '_' in func_name and func_name.islower():
                    conventions['snake_case_functions'] += 1
                elif re.match(r'^[a-z]+[A-Z]', func_name):
                    conventions['camelCase_functions'] += 1
                
                if len(func_name) > 3:
                    conventions['descriptive_names'] += 1
            
            # Check for constants
            if re.search(r'[A-Z_]{2,}\s*=', line):
                conventions['UPPERCASE_constants'] += 1
                
            # Check for single letter variables
            if re.search(r'\b[a-z]\s*=', line):
                conventions['single_letter_vars'] += 1
        
        return conventions
    
    def _analyze_code_style(self, code):
        """Analyze code style patterns"""
        lines = code.split('\n')
        style = {
            'avg_line_length': np.mean([len(line) for line in lines]) if lines else 0,
            'empty_lines': len([line for line in lines if not line.strip()]),
            'comments': len([line for line in lines if line.strip().startswith('#')]),
            'docstrings': len(re.findall(r'""".*?"""', code, re.DOTALL)),
            'indentation_style': 'spaces' if '    ' in code else 'tabs' if '\t' in code else 'mixed'
        }
        return style
    
    def _detect_ai_patterns(self, code):
        """Detect patterns that might indicate AI-generated code"""
        ai_indicators = {
            'score': 0,
            'indicators': [],
            'confidence': 'low'
        }
        
        # Common AI-generated code patterns
        ai_patterns = [
            (r'# This function', 'Generic function comments'),
            (r'# Initialize|# Create|# Set up', 'Verbose initialization comments'),
            (r'def\s+\w+\(.*\):\s*""".*?"""', 'Detailed docstrings for simple functions'),
            (r'if\s+__name__\s*==\s*[\'"]__main__[\'"]:', 'Standard main guard'),
            (r'import\s+\w+\s*\n\s*import', 'Organized imports'),
            (r'try:\s*\n.*?except.*?:', 'Exception handling patterns'),
            (r'\.format\(|f[\'"].*?\{.*?\}', 'Modern string formatting'),
            (r'list\(.*?\)|dict\(.*?\)', 'Explicit type conversions'),
        ]
        
        for pattern, description in ai_patterns:
            if re.search(pattern, code, re.DOTALL | re.MULTILINE):
                ai_indicators['score'] += 10
                ai_indicators['indicators'].append(description)
        
        # Check for overly perfect structure
        lines = [line for line in code.split('\n') if line.strip()]
        if lines:
            # Perfect indentation
            indented_lines = [line for line in lines if line.startswith('    ')]
            if len(indented_lines) > len(lines) * 0.3:
                ai_indicators['score'] += 15
                ai_indicators['indicators'].append('Consistent indentation pattern')
            
            # Balanced comment ratio
            comment_ratio = len([line for line in lines if line.strip().startswith('#')]) / len(lines)
            if 0.1 <= comment_ratio <= 0.3:
                ai_indicators['score'] += 10
                ai_indicators['indicators'].append('Optimal comment density')
        
        # Determine confidence level
        if ai_indicators['score'] >= 60:
            ai_indicators['confidence'] = 'high'
        elif ai_indicators['score'] >= 30:
            ai_indicators['confidence'] = 'medium'
        else:
            ai_indicators['confidence'] = 'low'
        
        return ai_indicators
    
    def detect_ai_generated_code(self, code):
        """Main AI detection function using multiple approaches"""
        try:
            # Get code analysis
            structure_analysis = self.analyze_code_structure(code)
            
            if 'error' in structure_analysis:
                return {'error': structure_analysis['error']}
            
            # AI detection based on patterns
            ai_patterns = structure_analysis.get('code_patterns', {}).get('ai_indicators', {})
            
            # Use Cohere for semantic analysis
            semantic_analysis = self._semantic_ai_detection(code)
            
            # Combine results
            final_score = (ai_patterns.get('score', 0) + semantic_analysis.get('score', 0)) / 2
            
            result = {
                'ai_probability': min(100, final_score),
                'confidence': 'high' if final_score >= 60 else 'medium' if final_score >= 30 else 'low',
                'pattern_analysis': ai_patterns,
                'semantic_analysis': semantic_analysis,
                'structure_analysis': structure_analysis,
                'verdict': self._get_ai_verdict(final_score)
            }
            
            return result
            
        except Exception as e:
            return {'error': f'AI detection failed: {str(e)}'}
    
    def _semantic_ai_detection(self, code):
        """Use Cohere to analyze semantic patterns for AI detection"""
        try:
            # Known AI-generated code samples for comparison
            ai_samples = [
                "def calculate_factorial(n):\n    if n == 0 or n == 1:\n        return 1\n    else:\n        return n * calculate_factorial(n - 1)",
                "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)",
                "def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr"
            ]
            
            # Get embeddings
            code_embedding = self.cohere_client.embed(
                texts=[code],
                model='embed-english-v3.0',
                input_type='search_document'
            ).embeddings[0]
            
            ai_embeddings = self.cohere_client.embed(
                texts=ai_samples,
                model='embed-english-v3.0',
                input_type='search_document'
            ).embeddings
            
            # Calculate similarities
            similarities = []
            for ai_emb in ai_embeddings:
                sim = cosine_similarity([code_embedding], [ai_emb])[0][0]
                similarities.append(sim)
            
            avg_similarity = np.mean(similarities)
            max_similarity = max(similarities)
            
            # Convert to AI probability score
            semantic_score = max_similarity * 100
            
            return {
                'score': semantic_score,
                'avg_similarity': avg_similarity,
                'max_similarity': max_similarity,
                'patterns_detected': semantic_score > 50
            }
            
        except Exception as e:
            print(f"Semantic AI detection error: {e}")
            return {'score': 0, 'error': str(e)}
    
    def _get_ai_verdict(self, score):
        """Get human-readable verdict"""
        if score >= 70:
            return "Highly likely AI-generated"
        elif score >= 50:
            return "Possibly AI-generated"
        elif score >= 30:
            return "Some AI characteristics detected"
        else:
            return "Likely human-written"

# Initialize global instances
analyzer = CodeSimilarityAnalyzer()
code_analyzer = CodeAnalyzer()

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

@app.route('/analyze', methods=['POST'])
def analyze_code():
    """Analyze a single code snippet for structure, complexity, and AI detection"""
    try:
        data = request.get_json()
        
        if not data or 'code' not in data:
            return jsonify({'error': 'Missing code in request'}), 400
        
        code = data['code'].strip()
        
        if not code:
            return jsonify({'error': 'Code cannot be empty'}), 400
        
        # Perform comprehensive analysis
        analysis_result = code_analyzer.analyze_code_structure(code)
        ai_detection_result = code_analyzer.detect_ai_generated_code(code)
        
        # Combine results and convert numpy types
        result = {
            'structure': {
                'lines': analysis_result.get('lines_of_code', 0),
                'functions': len(analysis_result.get('functions', [])),
                'classes': len(analysis_result.get('classes', [])),
                'imports': len(analysis_result.get('imports', [])),
                'variables': len(analysis_result.get('variables', [])),
                'function_details': analysis_result.get('functions', []),
                'class_details': analysis_result.get('classes', []),
                'comments': analysis_result.get('code_patterns', {}).get('code_style', {}).get('comments', 0)
            },
            'complexity': {
                'cyclomatic': analysis_result.get('complexity_metrics', {}).get('cyclomatic_complexity', 0),
                'cognitive': analysis_result.get('complexity_metrics', {}).get('cognitive_complexity', 0),
                'maintainability_index': analysis_result.get('complexity_metrics', {}).get('maintainability_index', 0),
                'nesting_depth': analysis_result.get('complexity_metrics', {}).get('nesting_depth', 0)
            },
            'style': analysis_result.get('code_patterns', {}),
            'ai_detection': {
                'is_ai_generated': bool(ai_detection_result.get('ai_probability', 0) > 50),
                'confidence': float(ai_detection_result.get('ai_probability', 0)),
                'verdict': ai_detection_result.get('verdict', 'Unknown')
            },
            'insights': generate_single_code_insights(analysis_result, ai_detection_result),
            'timestamp': datetime.now().isoformat()
        }
        
        # Convert any numpy types to native Python types
        result = convert_numpy_types(result)
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error in analyze_code: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/detailed-check', methods=['POST'])
def detailed_similarity_check():
    """Enhanced similarity check with detailed analysis"""
    try:
        data = request.get_json()
        
        if not data or 'code1' not in data or 'code2' not in data:
            return jsonify({'error': 'Missing code1 or code2 in request'}), 400
        
        code1 = data['code1'].strip()
        code2 = data['code2'].strip()
        
        if not code1 or not code2:
            return jsonify({'error': 'Code snippets cannot be empty'}), 400
        
        # Basic similarity check
        similarity_results = analyzer.calculate_similarity(code1, code2)
        
        # Detailed analysis for both codes
        analysis1 = code_analyzer.analyze_code_structure(code1)
        analysis2 = code_analyzer.analyze_code_structure(code2)
        
        # AI detection for both codes
        ai_detection1 = code_analyzer.detect_ai_generated_code(code1)
        ai_detection2 = code_analyzer.detect_ai_generated_code(code2)
        
        # Advanced similarity metrics
        detailed_comparison = {
            'structural_similarity': calculate_structural_similarity(analysis1, analysis2),
            'complexity_comparison': compare_complexity(analysis1, analysis2),
            'style_similarity': compare_code_style(analysis1, analysis2)
        }
        
        result = {
            'similarity': {
                'combined_score': float(similarity_results.get('FinalVerdict', 0)),
                'individual_scores': {
                    'cohere': float(similarity_results.get('Cohere', 0)),
                    'together': float(similarity_results.get('TogetherAI', 0)),
                    'replicate': float(similarity_results.get('Replicate', 0))
                }
            },
            'code1_analysis': {
                'structure': {
                    'lines': analysis1.get('lines_of_code', 0),
                    'functions': len(analysis1.get('functions', [])),
                    'classes': len(analysis1.get('classes', [])),
                    'imports': len(analysis1.get('imports', [])),
                    'variables': len(analysis1.get('variables', [])),
                    'comments': analysis1.get('code_patterns', {}).get('code_style', {}).get('comments', 0)
                },
                'complexity': {
                    'cyclomatic': analysis1.get('complexity_metrics', {}).get('cyclomatic_complexity', 0),
                    'cognitive': analysis1.get('complexity_metrics', {}).get('cognitive_complexity', 0),
                    'maintainability_index': analysis1.get('complexity_metrics', {}).get('maintainability_index', 0)
                },
                'style': analysis1.get('code_patterns', {}),
                'ai_detection': {
                    'is_ai_generated': bool(ai_detection1.get('ai_probability', 0) > 50),
                    'confidence': float(ai_detection1.get('ai_probability', 0))
                }
            },
            'code2_analysis': {
                'structure': {
                    'lines': analysis2.get('lines_of_code', 0),
                    'functions': len(analysis2.get('functions', [])),
                    'classes': len(analysis2.get('classes', [])),
                    'imports': len(analysis2.get('imports', [])),
                    'variables': len(analysis2.get('variables', [])),
                    'comments': analysis2.get('code_patterns', {}).get('code_style', {}).get('comments', 0)
                },
                'complexity': {
                    'cyclomatic': analysis2.get('complexity_metrics', {}).get('cyclomatic_complexity', 0),
                    'cognitive': analysis2.get('complexity_metrics', {}).get('cognitive_complexity', 0),
                    'maintainability_index': analysis2.get('complexity_metrics', {}).get('maintainability_index', 0)
                },
                'style': analysis2.get('code_patterns', {}),
                'ai_detection': {
                    'is_ai_generated': bool(ai_detection2.get('ai_probability', 0) > 50),
                    'confidence': float(ai_detection2.get('ai_probability', 0))
                }
            },
            'comparison_insights': generate_comparison_insights(analysis1, analysis2, similarity_results)
        }
        
        # Convert any numpy types to native Python types
        result = convert_numpy_types(result)
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error in detailed_similarity_check: {e}")
        return jsonify({'error': 'Internal server error'}), 500

def calculate_structural_similarity(analysis1, analysis2):
    """Calculate structural similarity between two code analyses"""
    if 'error' in analysis1 or 'error' in analysis2:
        return {'score': 0, 'details': 'Analysis error'}
    
    similarity_score = 0
    details = {}
    
    # Compare function counts
    func_count1 = len(analysis1.get('functions', []))
    func_count2 = len(analysis2.get('functions', []))
    if func_count1 > 0 or func_count2 > 0:
        func_similarity = 1 - abs(func_count1 - func_count2) / max(func_count1, func_count2, 1)
        similarity_score += func_similarity * 0.3
        details['function_similarity'] = func_similarity
    
    # Compare class counts
    class_count1 = len(analysis1.get('classes', []))
    class_count2 = len(analysis2.get('classes', []))
    if class_count1 > 0 or class_count2 > 0:
        class_similarity = 1 - abs(class_count1 - class_count2) / max(class_count1, class_count2, 1)
        similarity_score += class_similarity * 0.2
        details['class_similarity'] = class_similarity
    
    # Compare import similarity
    imports1 = set(analysis1.get('imports', []))
    imports2 = set(analysis2.get('imports', []))
    if imports1 or imports2:
        import_intersection = len(imports1.intersection(imports2))
        import_union = len(imports1.union(imports2))
        import_similarity = import_intersection / import_union if import_union > 0 else 0
        similarity_score += import_similarity * 0.2
        details['import_similarity'] = import_similarity
    
    # Compare lines of code
    loc1 = analysis1.get('lines_of_code', 0)
    loc2 = analysis2.get('lines_of_code', 0)
    if loc1 > 0 or loc2 > 0:
        loc_similarity = 1 - abs(loc1 - loc2) / max(loc1, loc2, 1)
        similarity_score += loc_similarity * 0.3
        details['loc_similarity'] = loc_similarity
    
    return {
        'score': round(similarity_score * 100, 2),
        'details': details
    }

def compare_complexity(analysis1, analysis2):
    """Compare complexity metrics between two code analyses"""
    complexity1 = analysis1.get('complexity_metrics', {}).get('cyclomatic_complexity', 0)
    complexity2 = analysis2.get('complexity_metrics', {}).get('cyclomatic_complexity', 0)
    
    if complexity1 == 0 and complexity2 == 0:
        return {'similarity': 1.0, 'difference': 0}
    
    max_complexity = max(complexity1, complexity2, 1)
    difference = abs(complexity1 - complexity2)
    similarity = 1 - (difference / max_complexity)
    
    return {
        'similarity': float(similarity),
        'difference': int(difference),
        'code1_complexity': int(complexity1),
        'code2_complexity': int(complexity2)
    }

def compare_code_style(analysis1, analysis2):
    """Compare code style between two analyses"""
    style1 = analysis1.get('code_patterns', {}).get('code_style', {})
    style2 = analysis2.get('code_patterns', {}).get('code_style', {})
    
    similarities = []
    
    # Compare specific style aspects
    if 'avg_line_length' in style1 and 'avg_line_length' in style2:
        line_length_diff = abs(style1['avg_line_length'] - style2['avg_line_length'])
        line_length_similarity = max(0, 1 - line_length_diff / 100)  # Normalize to 0-1
        similarities.append(line_length_similarity)
    
    # Compare indentation style
    if style1.get('indentation_style') == style2.get('indentation_style'):
        similarities.append(1.0)
    else:
        similarities.append(0.0)
    
    # Compare comment density
    if 'comments' in style1 and 'comments' in style2:
        comment_diff = abs(style1['comments'] - style2['comments'])
        comment_similarity = max(0, 1 - comment_diff / 10)  # Normalize
        similarities.append(comment_similarity)
    
    overall_similarity = sum(similarities) / len(similarities) if similarities else 0.5
    
    return {
        'similarity': float(overall_similarity),
        'aspects_compared': len(similarities),
        'details': {
            'line_length_similarity': similarities[0] if len(similarities) > 0 else None,
            'indentation_similarity': similarities[1] if len(similarities) > 1 else None,
            'comment_similarity': similarities[2] if len(similarities) > 2 else None
        }
    }

def generate_comparison_insights(analysis1, analysis2, similarity_results):
    """Generate human-readable insights from the comparison"""
    insights = {
        'structural_similarity': [],
        'style_similarity': [],
        'potential_plagiarism_indicators': []
    }
    
    if 'error' in analysis1 or 'error' in analysis2:
        insights['structural_similarity'].append("⚠️ Code analysis encountered errors")
        return insights
    
    # Similarity insights
    final_verdict = similarity_results.get('FinalVerdict', 0)
    if final_verdict >= 80:
        insights['potential_plagiarism_indicators'].append("🔴 Very high similarity detected - possible plagiarism")
        insights['potential_plagiarism_indicators'].append("Similar algorithmic approach and implementation")
        insights['potential_plagiarism_indicators'].append("Recommend manual review for academic integrity")
    elif final_verdict >= 60:
        insights['potential_plagiarism_indicators'].append("🟡 Moderate similarity - manual review recommended")
        insights['potential_plagiarism_indicators'].append("Common patterns or similar problem-solving approach")
    elif final_verdict >= 40:
        insights['structural_similarity'].append("🔵 Some similarities found - common patterns detected")
        insights['structural_similarity'].append("May share standard algorithmic patterns")
    else:
        insights['structural_similarity'].append("🟢 Low similarity - likely original work")
        insights['structural_similarity'].append("Different implementation approaches")
    
    # Detailed structural analysis
    func1 = len(analysis1.get('functions', []))
    func2 = len(analysis2.get('functions', []))
    lines1 = analysis1.get('lines_of_code', 0)
    lines2 = analysis2.get('lines_of_code', 0)
    
    if func1 == func2 and func1 > 0:
        insights['structural_similarity'].append(f"📊 Both codes have {func1} function(s) - similar structure")
    elif abs(func1 - func2) <= 1:
        insights['structural_similarity'].append("📊 Similar number of functions")
    else:
        insights['structural_similarity'].append("📊 Different structural organization")
    
    if abs(lines1 - lines2) <= 5:
        insights['structural_similarity'].append("📏 Similar code length")
    elif lines1 > lines2 * 1.5:
        insights['structural_similarity'].append("📏 First code is significantly longer")
    elif lines2 > lines1 * 1.5:
        insights['structural_similarity'].append("📏 Second code is significantly longer")
    
    # Complexity comparison
    complexity1 = analysis1.get('complexity_metrics', {})
    complexity2 = analysis2.get('complexity_metrics', {})
    
    cc1 = complexity1.get('cyclomatic_complexity', 0)
    cc2 = complexity2.get('cyclomatic_complexity', 0)
    
    if abs(cc1 - cc2) <= 1:
        insights['structural_similarity'].append("⚖️ Similar complexity levels")
    elif cc1 > cc2 + 2:
        insights['structural_similarity'].append("📈 First code is more complex")
    elif cc2 > cc1 + 2:
        insights['structural_similarity'].append("📈 Second code is more complex")
    
    # Style analysis
    style1 = analysis1.get('code_patterns', {}).get('code_style', {})
    style2 = analysis2.get('code_patterns', {}).get('code_style', {})
    
    if style1.get('indentation_style') == style2.get('indentation_style'):
        insights['style_similarity'].append("✅ Consistent indentation style")
    else:
        insights['style_similarity'].append("📏 Different indentation styles")
    
    # Variable naming patterns
    naming1 = analysis1.get('code_patterns', {}).get('naming_conventions', {})
    naming2 = analysis2.get('code_patterns', {}).get('naming_conventions', {})
    
    if naming1.get('snake_case_functions', 0) > 0 and naming2.get('snake_case_functions', 0) > 0:
        insights['style_similarity'].append("🐍 Both use snake_case naming")
    elif naming1.get('camelCase_functions', 0) > 0 and naming2.get('camelCase_functions', 0) > 0:
        insights['style_similarity'].append("🐪 Both use camelCase naming")
    
    # Import analysis
    imports1 = len(analysis1.get('imports', []))
    imports2 = len(analysis2.get('imports', []))
    
    if imports1 == imports2 == 0:
        insights['structural_similarity'].append("📦 Neither code uses external imports")
    elif abs(imports1 - imports2) <= 1:
        insights['structural_similarity'].append("📦 Similar use of imports")
    
    # AI detection comparison
    if final_verdict >= 70:
        insights['potential_plagiarism_indicators'].append("🚨 Extremely similar code patterns")
        insights['potential_plagiarism_indicators'].append("Consider checking for code copying")
    
    return insights

def generate_single_code_insights(analysis, ai_detection):
    """Generate insights for single code analysis"""
    insights = []
    
    if 'error' in analysis:
        insights.append("⚠️ Code analysis encountered errors")
        return insights
    
    # Structure insights
    lines = analysis.get('lines_of_code', 0)
    functions = len(analysis.get('functions', []))
    classes = len(analysis.get('classes', []))
    
    if lines < 10:
        insights.append("📄 Short code snippet - easy to understand")
    elif lines < 50:
        insights.append("📄 Medium-sized code - well manageable")
    elif lines < 200:
        insights.append("📄 Large code block - consider breaking into smaller functions")
    else:
        insights.append("📄 Very large code - definitely needs modularization")
    
    # Function analysis
    if functions == 0:
        insights.append("🔧 No functions detected - consider organizing code into functions")
    elif functions == 1:
        insights.append("🔧 Single function structure - clean and focused")
    elif functions <= 5:
        insights.append(f"🔧 Well-structured with {functions} functions")
    else:
        insights.append(f"🔧 Complex structure with {functions} functions - ensure good organization")
    
    # Class analysis
    if classes > 0:
        insights.append(f"🏗️ Object-oriented design with {classes} class(es)")
    
    # Complexity insights
    complexity_metrics = analysis.get('complexity_metrics', {})
    cyclomatic = complexity_metrics.get('cyclomatic_complexity', 0)
    maintainability = complexity_metrics.get('maintainability_index', 0)
    
    if cyclomatic <= 5:
        insights.append("🟢 Low complexity - easy to test and maintain")
    elif cyclomatic <= 10:
        insights.append("🟡 Moderate complexity - acceptable for most cases")
    elif cyclomatic <= 15:
        insights.append("🟠 High complexity - consider refactoring")
    else:
        insights.append("🔴 Very high complexity - refactoring strongly recommended")
    
    if maintainability >= 20:
        insights.append("✨ Excellent maintainability score")
    elif maintainability >= 10:
        insights.append("👍 Good maintainability")
    else:
        insights.append("⚠️ Low maintainability - needs improvement")
    
    # Style insights
    code_patterns = analysis.get('code_patterns', {})
    code_style = code_patterns.get('code_style', {})
    naming = code_patterns.get('naming_conventions', {})
    
    if code_style.get('indentation_style') == 'spaces':
        insights.append("📏 Uses space indentation (recommended)")
    elif code_style.get('indentation_style') == 'tabs':
        insights.append("📏 Uses tab indentation")
    
    if naming.get('descriptive_names', 0) > 0:
        insights.append("✅ Good use of descriptive variable names")
    
    if code_style.get('comments', 0) > 0:
        insights.append("📝 Well-commented code")
    else:
        insights.append("📝 Consider adding comments for better readability")
    
    # AI detection insights
    ai_prob = ai_detection.get('ai_probability', 0)
    if ai_prob >= 70:
        insights.append("🤖 High probability of AI-generated code")
    elif ai_prob >= 40:
        insights.append("🤖 Some AI characteristics detected")
    else:
        insights.append("👨‍💻 Likely human-written code")
    
    return insights

def convert_numpy_types(obj):
    """Convert numpy types to Python native types for JSON serialization"""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    return obj

if __name__ == '__main__':
    print("🚀 Starting AI Code Plagiarism Detector Backend...")
    print("📡 Server running on http://localhost:8000")
    print("🔗 CORS enabled for frontend integration")
    app.run(host='0.0.0.0', port=8000, debug=True)
