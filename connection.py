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
        print("Table users created successfully")
    except Error as e:
        print(f"Failed to create table users: {e}")

def create_predictinTable():
    
    try:
        conn = sqlite3.connect("somtelchurn.db")
        
        cursor = conn.cursor()
      
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                gender TEXT,
                partner TEXT,
                dependents TEXT,
                phone_service TEXT,
                multiple_lines TEXT,
                internet_service TEXT,
                online_security TEXT,
                online_backup TEXT,
                device_protection TEXT,
                tech_support TEXT,
                streaming_tv TEXT,
                streaming_movies TEXT,
                contract TEXT,
                payment_method TEXT,
                paperless_billing TEXT,
                monthly_charges REAL,
                total_charges REAL,
                number_of_months INTEGER,
                predictedType TEXT
             
            );
        """)
      
        print("Prediction Table created successfully")
    except Error as e:
        print(f"Failed to create table prediction: {e}")

def InsertPredictionsData(gender,partner,dependents,phone_service,multiple_lines,internet_service,online_security,online_backup,device_protection,tech_support,streaming_tv,streaming_movies,contract,payment_method,paperless_billing,monthly_charges,total_charges,number_of_months,predictedType):
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO predictions(gender,partner,dependents,phone_service,multiple_lines,internet_service,online_security,online_backup,device_protection,tech_support,streaming_tv,streaming_movies,contract,payment_method,paperless_billing,monthly_charges,total_charges,number_of_months,predictedType) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (gender,partner,dependents,phone_service,multiple_lines,internet_service,online_security,online_backup,device_protection,tech_support,streaming_tv,streaming_movies,contract,payment_method,paperless_billing,monthly_charges,total_charges,number_of_months,predictedType))
        conn.commit()
        conn.close()
        print("inserted successfully")
    except Error as e:
        print(f"Failed to insert data into table predictions: {e}")

def SummarizePrediction(type):
    conn = get_db()
    cursor = conn.cursor()
    results = None
    try:
        if type == 'table':
            cursor.execute("SELECT * FROM predictions")
            results = cursor.fetchall() 
            print("Reading all data")

        elif type == 'churn':
            cursor.execute("SELECT * FROM predictions WHERE predictedType = 'Churn'")
            results = cursor.fetchall()  
            print("Reading all churn data")

        elif type == 'not churn':
            cursor.execute("SELECT * FROM predictions WHERE predictedType = 'Not churn'")
            results = cursor.fetchall()
            print("Reading all not churn data")

        elif type == 'all':
            cursor.execute("SELECT predictedType, COUNT(*) FROM predictions GROUP BY predictedType")
            results = cursor.fetchall()  
            print("Reading summary of all data")

    except Error as e:
        print(f"Failed to read data from table predictions: {e}")


    return results  

