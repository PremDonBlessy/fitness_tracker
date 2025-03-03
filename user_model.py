import mysql.connector
import hashlib
from database.db_config import get_db_connection  # Importing the DB connection function


def hash_password(password):
    """Hash the password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def login(username, password):
    """Check user credentials for login"""
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_password = hash_password(password)

    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, hashed_password))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user is not None


def signup(username, password):
    """Register a new user"""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        hashed_password = hash_password(password)
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username, hashed_password))
        conn.commit()
        success = True
    except mysql.connector.Error:
        success = False  # Username already exists or other DB issue

    cursor.close()
    conn.close()
    return success
