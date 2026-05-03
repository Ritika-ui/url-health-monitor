import os
import time
import requests
import psycopg2
from datetime import datetime
from database import get_db_connection

# List of URLs to monitor
URLS = [
    "google.com",
    "github.com",
    "stackoverflow.com",
    "reddit.com",
    "amazon.com"
]

def get_db_connection():
    return psycopg2.connect(os.environ.get("DATABASE_URL"))

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS health_checks (
            id SERIAL PRIMARY KEY,
            url TEXT NOT NULL,
            status TEXT NOT NULL,
            last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def check_url(url):
    try:
        response = requests.get(f"http://{url}", timeout=5)
        return "UP" if response.status_code == 200 else "DOWN"
    except:
        return "DOWN"

def save_result(url, status):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO health_checks (url, status) VALUES (%s, %s)",
        (url, status)
    )
    conn.commit()
    conn.close()

def monitor_loop():
    while True:
        for url in URLS:
            status = check_url(url)
            save_result(url, status)
            print(f"[{datetime.now()}] {url} → {status}")
        time.sleep(30)  # Check every 30 seconds

if __name__ == "__main__":
    init_db()
    print("Starting URL Health Monitor...")
    monitor_loop()
