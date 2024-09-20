import psycopg2
import os
import json

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
