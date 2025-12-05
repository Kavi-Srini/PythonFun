import os
import psycopg2
import psycopg2.extras
from flask import Flask, render_template

db_url = os.environ.get("DATABASE_URL")

app = Flask(__name__)

def get_db_connection():
    if db_url:
        # DATABASE_URL like: postgresql://spiced:secretpassword@host.docker.internal:5432/spiceddb
        return psycopg2.connect(db_url)

    # Fallback: use individual env vars (e.g. when running locally without Docker)
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "commerce"),
        user=os.getenv("DB_USER", "spicedmocha"),
        password=os.getenv("DB_PASSWORD", "password"),
    )

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT id, name, description, price_cents, sku FROM products WHERE featured = TRUE ORDER BY id;")
    featured = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', featured=featured)

@app.route('/products')
def products():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT id, name, description, price_cents, sku FROM products ORDER BY id;")
    products = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('products.html', products=products)