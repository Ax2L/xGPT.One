import psycopg2
import streamlit as st
from postgres import run_query

def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()  # Initialize connection within the function

def db_init():
    table_queries = [
        """
        CREATE TABLE IF NOT EXISTS Users (
            user_id VARCHAR(255) PRIMARY KEY,
            email VARCHAR(255) UNIQUE,
            openai_key VARCHAR(255),
            theme VARCHAR(50),
            language VARCHAR(50),
            dev_mode BOOLEAN,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        );
        """
    ]

    try:
        for query in table_queries:
            run_query(conn, query, return_type='none')  # Pass `conn` to `run_query()`
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
    finally:
        conn.close()  # Ensure to close the connection when done

# Initialize tables if not exist
db_init()
