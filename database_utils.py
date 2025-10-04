import sqlite3
from config import DATABASE_PATH

def get_db_connection():
    """
    Establishes and returns a connection to the SQLite database.
    
    Returns:
        sqlite3.Connection: A connection object to the database.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    # This allows you to access columns by name (like a dictionary).
    conn.row_factory = sqlite3.Row 
    return conn

