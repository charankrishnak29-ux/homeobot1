import sqlite3
from datetime import datetime

# This function creates the database and table if they don't exist
def init_db():
    conn = sqlite3.connect("patients.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            symptoms TEXT,
            condition TEXT,
            medicines TEXT,
            advice TEXT,
            date TEXT
        )
    """)
    
    conn.commit()
    conn.close()

# This function saves a consultation to the database
def save_consultation(patient_name, symptoms, condition, medicines, advice):
    conn = sqlite3.connect("patients.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO consultations 
        (patient_name, symptoms, condition, medicines, advice, date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        patient_name,
        symptoms,
        condition,
        medicines,
        advice,
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))
    
    conn.commit()
    conn.close()

# This function gets all consultations from the database
def get_all_consultations():
    conn = sqlite3.connect("patients.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM consultations ORDER BY id DESC
    """)
    
    rows = cursor.fetchall()
    conn.close()
    return rows