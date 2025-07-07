from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'Test API is running'})

@app.route('/test')
def test():
    return jsonify({'message': 'Hello from Flask!'})

if __name__ == '__main__':
    print("Starting minimal test API on port 5002...")
    app.run(host='127.0.0.1', port=5002, debug=True)
