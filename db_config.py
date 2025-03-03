# database/db_config.py

import mysql.connector

def get_db_connection():
    """Establish a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(
            host="localhost",    # Change to your database host if needed
            user="root",         # Change to your MySQL username
            password="Welcome@123456",  # Change to your MySQL password
            database="fitness_tracker"  # Ensure this database exists in MySQL
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
        return None
