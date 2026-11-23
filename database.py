import sqlite3
import os


# Get project folder location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database file location
DB_PATH = os.path.join(BASE_DIR, "documents.db")


# Connect to database
def get_connection():

    conn = sqlite3.connect(DB_PATH)

    return conn


# Create database and table
def create_database():

    conn = get_connection()

    try:

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

        # Check table exists
        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name = 'documents'
        """)

        result = cursor.fetchone()

        print("Database location:", DB_PATH)

        if result:

            print("Documents table created successfully!")

        else:

            print("Documents table not found!")

    finally:

        conn.close()


# Save document details
def save_document(filename, file_type, extracted_text):

    # Ensure table exists
    create_database()

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO documents
            (filename, file_type, extracted_text)

            VALUES (?, ?, ?)
        """, (filename, file_type, extracted_text))

        conn.commit()

        print("Document saved successfully!")

    finally:

        conn.close()


# Retrieve saved documents
def get_documents():

    # Ensure table exists
    create_database()

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                filename,
                file_type,
                extracted_text

            FROM documents

            ORDER BY id DESC
        """)

        documents = cursor.fetchall()

        return documents

    finally:

        conn.close()