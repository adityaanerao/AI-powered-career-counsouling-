import mysql.connector
from database.db import get_db_connection

def debug_govt():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    print("--- Searching by Name LIKE '%Government%' ---")
    cursor.execute("SELECT * FROM colleges WHERE college_name LIKE '%Government%'")
    rows = cursor.fetchall()
    print(f"Found {len(rows)} records.")
    for r in rows:
        print(r)
        
    conn.close()

if __name__ == "__main__":
    debug_govt()
