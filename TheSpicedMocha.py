import os
import psycopg2
import psycopg2.extras
from flask import Flask, render_template

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "commerce"),
        user=os.getenv("DB_USER", "user"),
        password=os.getenv("DB_PASSWORD", "password"),
    )

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT id, name, description, price_cents, sku FROM products ORDER BY id;")
    products = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', products=products)