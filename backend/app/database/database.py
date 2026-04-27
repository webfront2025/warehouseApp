
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "database.db")

def get_connection():
    return sqlite3.connect(DB_PATH)
