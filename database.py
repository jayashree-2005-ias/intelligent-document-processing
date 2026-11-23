import sqlite3
import os

# Database file location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "documents.db")


# Create database and table
def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            file_type TEXT NOT NULL,
            extracted_text TEXT
        )
    """)

    conn.commit()
    conn.close()

    print("Database created successfully!")


# Save document details
def save_document(filename, file_type, extracted_text):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()


    cursor.execute("""
        INSERT INTO documents
        (filename, file_type, extracted_text)
        VALUES (?, ?, ?)
    """, (filename, file_type, extracted_text))

    conn.commit()
    conn.close()

    print("Document saved successfully!")


# Display saved documents
def get_documents():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, filename, file_type, extracted_text
        FROM documents
        ORDER BY id DESC
    """)

    documents = cursor.fetchall()

    conn.close()

    return documents