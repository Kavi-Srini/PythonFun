#!/usr/bin/env python3
# Minimal migration runner: records applied files in schema_migrations table.
import os, time
import psycopg2
from pathlib import Path

MIGRATIONS_DIR = Path(__file__).parent / "migrations"
DB_PARAMS = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "commerce"),
    "user": os.getenv("DB_USER", "spiced"),
    "password": os.getenv("DB_PASSWORD", "secretpassword"),
}

def wait_connect():
    while True:
        try:
            conn = psycopg2.connect(**DB_PARAMS)
            conn.autocommit = True
            return conn
        except Exception:
            time.sleep(1)

def ensure_migrations_table(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS schema_migrations (
      filename TEXT PRIMARY KEY,
      applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

def applied_files(cur):
    cur.execute("SELECT filename FROM schema_migrations;")
    return {r[0] for r in cur.fetchall()}

def apply_migration(cur, sql, filename):
    cur.execute(sql)
    cur.execute("INSERT INTO schema_migrations (filename) VALUES (%s) ON CONFLICT DO NOTHING;", (filename,))

def main():
    conn = wait_connect()
    cur = conn.cursor()
    ensure_migrations_table(cur)
    done = applied_files(cur)
    files = sorted(p.name for p in MIGRATIONS_DIR.glob("*.sql"))
    for f in files:
        if f in done:
            continue
        sql = (MIGRATIONS_DIR / f).read_text()
        apply_migration(cur, sql, f)
        conn.commit()
        print("applied:", f)
    cur.close()
    conn.close()
    print("migrations complete")

if __name__ == "__main__":
    main()