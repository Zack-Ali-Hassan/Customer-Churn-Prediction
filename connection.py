import sqlite3
from flask import g
from sqlite3 import Error

def get_db():
    if 'db' not in g:
        g.db = create_sqlite_database("somtelchurn.db")
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def create_sqlite_database(filename):
    try:
        conn = sqlite3.connect(filename, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        print("Connection to SQLite DB successful")
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_table():
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
        """)
        print("Table created successfully")
    except Error as e:
        print(f"Failed to create table: {e}")
