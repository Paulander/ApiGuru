from flask import Flask, render_template, request, jsonify
import requests
from db_utils import init_db, add_predefined_call, get_predefined_calls, verify_api_key, add_api_call_to_history, get_api_call_history, get_dashboard_data
import os
import time
import traceback

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
        start_time = time.time()
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=body)
        else:
            return jsonify({'error': 'Unsupported method'}), 400
        end_time = time.time()

        response_time = end_time - start_time

        content_type = response.headers.get('content-type', '')
        if 'application/json' in content_type:
            response_body = response.json()
        else:
            response_body = response.text

        response_data = {
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'body': response_body
        }

        # Add the API call to history
        add_api_call_to_history(url, method, headers, body, response.status_code, dict(response.headers), str(response_body), response_time)

        return jsonify(response_data)
    except requests.RequestException as e:
        app.logger.error(f"Error making API request: {str(e)}")
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
        app.logger.error(f"Error saving predefined call: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/get_predefined_calls', methods=['GET'])
def fetch_predefined_calls():
    try:
        calls = get_predefined_calls()
        return jsonify(calls)
    except Exception as e:
        app.logger.error(f"Error fetching predefined calls: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/verify_api_key', methods=['POST'])
def check_api_key():
    data = request.json
    api_key = data.get('api_key')

    try:
        is_valid = verify_api_key(api_key)
        return jsonify({'is_valid': is_valid})
    except Exception as e:
        app.logger.error(f"Error verifying API key: {str(e)}")
        return jsonify({'error': str(e)}),eschool

@app.route('/get_api_call_history', methods=['GET'])
def fetch_api_call_history():
    try:
        history = get_api_call_history()
        return jsonify(history)
    except Exception as e:
        app.logger.error(f"Error fetching API call history: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/get_dashboard_data', methods=['GET'])
def fetch_dashboard_data():
    try:
        dashboard_data = get_dashboard_data()
        if dashboard_data is None:
            app.logger.error("No dashboard data found")
            return jsonify({'error': 'No dashboard data available'}), 404
        return jsonify(dashboard_data)
    except Exception as e:
        app.logger.error(f"Error fetching dashboard data: {str(e)}")
        app.logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': 'An error occurred while fetching dashboard data', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)