import os
import psycopg2
from datetime import datetime
from flask import Flask, jsonify

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(os.environ.get("DATABASE_URL"))

@app.route("/")
def home():
    return """
    <html>
        <body>
            <h1>URL Health Monitor 🏥</h1>
            <p>Running on Kubernetes pod: <b>{}</b></p>
            <a href="/health">View health check results →</a>
        </body>
    </html>
    """.format(os.environ.get("HOSTNAME", "unknown"))

@app.route("/health")
def get_health():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT url, status, last_checked FROM health_checks ORDER BY last_checked DESC LIMIT 20")
    rows = cur.fetchall()
    conn.close()
    
    results = []
    for row in rows:
        results.append({
            "url": row[0],
            "status": row[1],
            "last_checked": row[2]
        })
    
    return jsonify(results)

@app.route("/health/<url>")
def check_single(url):
    import requests
    try:
        response = requests.get(f"http://{url}", timeout=5)
        status = "UP" if response.status_code == 200 else "DOWN"
    except:
        status = "DOWN"
    
    return jsonify({"url": url, "status": status})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
