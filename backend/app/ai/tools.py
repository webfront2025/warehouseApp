import sqlite3
from app.database.database import DB_PATH


def get_low_stock_products(threshold=20):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, quantity 
        FROM products 
        WHERE quantity < ?
    """, (threshold,))

    rows = cursor.fetchall()
    conn.close()

    return rows


def get_all_products():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name, quantity, price FROM products")
    rows = cursor.fetchall()

    conn.close()
    return rows