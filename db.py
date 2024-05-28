import sqlite3
import json

def create_database():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_progress (
            user_id TEXT PRIMARY KEY,
            messages TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_user_data(user_id, messages):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO user_progress (user_id, messages)
        VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET messages=excluded.messages
    ''', (user_id, json.dumps(messages)))
    conn.commit()
    conn.close()

def load_user_data(user_id):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT messages FROM user_progress WHERE user_id=?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return json.loads(result[0])
    return []
