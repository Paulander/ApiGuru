from flask import Flask, render_template, request, jsonify
import requests
from db_utils import init_db, add_predefined_call, get_predefined_calls, verify_api_key
import os

app = Flask(__name__)

# Initialize database
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/make_request', methods=['POST'])
def make_request():
    data = request.json
    url = data.get('url')
    method = data.get('method')
    headers = data.get('headers', {})
    body = data.get('body', {})

    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=body)
        else:
            return jsonify({'error': 'Unsupported method'}), 400

        return jsonify({
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'body': response.json() if response.headers.get('content-type') == 'application/json' else response.text
        })
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/save_predefined_call', methods=['POST'])
def save_predefined_call():
    data = request.json
    name = data.get('name')
    url = data.get('url')
    method = data.get('method')
    headers = data.get('headers', {})
    body = data.get('body', {})

    try:
        add_predefined_call(name, url, method, headers, body)
        return jsonify({'message': 'Predefined call saved successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_predefined_calls', methods=['GET'])
def fetch_predefined_calls():
    try:
        calls = get_predefined_calls()
        return jsonify(calls)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/verify_api_key', methods=['POST'])
def check_api_key():
    data = request.json
    api_key = data.get('api_key')

    try:
        is_valid = verify_api_key(api_key)
        return jsonify({'is_valid': is_valid})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
