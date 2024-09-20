import psycopg2
import os
import json
from datetime import datetime

def get_db_connection():
    return psycopg2.connect(
        host=os.environ['PGHOST'],
        port=os.environ['PGPORT'],
        database=os.environ['PGDATABASE'],
        user=os.environ['PGUSER'],
        password=os.environ['PGPASSWORD']
    )

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS predefined_calls (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            method TEXT NOT NULL,
            headers JSONB,
            body JSONB
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS api_call_history (
            id SERIAL PRIMARY KEY,
            url TEXT NOT NULL,
            method TEXT NOT NULL,
            headers JSONB,
            body JSONB,
            response_status INTEGER,
            response_headers JSONB,
            response_body TEXT,
            response_time FLOAT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

def add_predefined_call(name, url, method, headers, body):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO predefined_calls (name, url, method, headers, body) VALUES (%s, %s, %s, %s, %s)",
        (name, url, method, json.dumps(headers), json.dumps(body))
    )
    conn.commit()
    cur.close()
    conn.close()

def get_predefined_calls():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, url, method, headers, body FROM predefined_calls")
    calls = [
        {
            'name': row[0],
            'url': row[1],
            'method': row[2],
            'headers': row[3],
            'body': row[4]
        }
        for row in cur.fetchall()
    ]
    cur.close()
    conn.close()
    return calls

def verify_api_key(api_key):
    # This is a mock implementation. In a real-world scenario, you would
    # check the API key against a database or external service.
    return len(api_key) > 0 and api_key.startswith('valid_')

def add_api_call_to_history(url, method, headers, body, response_status, response_headers, response_body, response_time):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO api_call_history (url, method, headers, body, response_status, response_headers, response_body, response_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (url, method, json.dumps(headers), json.dumps(body), response_status, json.dumps(response_headers), response_body, response_time)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_api_call_history():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT url, method, headers, body, response_status, response_headers, response_body, response_time, timestamp FROM api_call_history ORDER BY timestamp DESC")
    history = [
        {
            'url': row[0],
            'method': row[1],
            'headers': row[2],
            'body': row[3],
            'response_status': row[4],
            'response_headers': row[5],
            'response_body': row[6],
            'response_time': row[7],
            'timestamp': row[8].isoformat()
        }
        for row in cur.fetchall()
    ]
    cur.close()
    conn.close()
    return history

def get_dashboard_data():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Get total number of API calls
    cur.execute("SELECT COUNT(*) FROM api_call_history")
    total_calls = cur.fetchone()[0] or 0
    
    # Get average response time
    cur.execute("SELECT AVG(response_time) FROM api_call_history")
    avg_response_time = cur.fetchone()[0] or 0
    
    # Get API usage by method
    cur.execute("SELECT method, COUNT(*) FROM api_call_history GROUP BY method")
    usage_by_method = dict(cur.fetchall()) or {}
    
    # Get top 5 most called APIs
    cur.execute("SELECT url, COUNT(*) as call_count FROM api_call_history GROUP BY url ORDER BY call_count DESC LIMIT 5")
    top_apis = [{'url': row[0], 'count': row[1]} for row in cur.fetchall()] or []
    
    cur.close()
    conn.close()
    
    return {
        'total_calls': total_calls,
        'avg_response_time': avg_response_time,
        'usage_by_method': usage_by_method,
        'top_apis': top_apis
    }
