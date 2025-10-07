import sqlite3
from config import DATABASE_PATH

def get_db_connection():
   #returns a new connection to the SQLite database
    conn = sqlite3.connect(DATABASE_PATH)
   
    conn.row_factory = sqlite3.Row 
    return conn

