import os
import psycopg2
import psycopg2.extras
from flask import Flask, render_template, request, redirect, url_for, flash, abort


db_url = os.environ.get("DATABASE_URL")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "devkey")

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

def get_product(product_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cur.fetchone()
    cur.close()
    conn.close()
    if not product:
        abort(404)
    return product


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

@app.route('/products/<int:product_id>')
def product_detail(product_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cur.fetchone()
    cur.close()
    conn.close()
    if not product:
        abort(404)
    return render_template('product.html', product=product)

@app.route('/products/new', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        price_cents = int(float(request.form['price']) * 100)
        sku = request.form.get('sku')
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO products (name, description, price_cents, sku) VALUES (%s, %s, %s, %s)",
            (name, description, price_cents, sku)
        )
        conn.commit()
        cur.close()
        conn.close()
        flash('Product created.')
        return redirect(url_for('products'))
    return render_template('new_product.html')

@app.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cur.fetchone()
    if not product:
        cur.close()
        conn.close()
        abort(404)
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        price_cents = int(float(request.form['price']) * 100)
        sku = request.form.get('sku')
        cur.execute(
            "UPDATE products SET name=%s, description=%s, price_cents=%s, sku=%s WHERE id=%s",
            (name, description, price_cents, sku, product_id)
        )
        conn.commit()
        cur.close()
        conn.close()
        flash('Product updated.')
        return redirect(url_for('product_detail', product_id=product_id))
    cur.close()
    conn.close()
    return render_template('edit_product.html', product=product)

@app.route('/products/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id = %s", (product_id,))
    conn.commit()
    cur.close()
    conn.close()
    flash('Product deleted.')
    return redirect(url_for('products'))

