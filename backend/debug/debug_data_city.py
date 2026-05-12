import mysql.connector
from database.db import get_db_connection

def debug_city():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    print("--- Searching by city='Aurangabad' ---")
    cursor.execute("SELECT * FROM colleges WHERE city = 'Aurangabad'")
    rows = cursor.fetchall()
    print(f"Found {len(rows)} records.")
    for r in rows:
        print(r)
            
    print("\n--- Searching by Name LIKE '%Aurangabad%' ---")
    cursor.execute("SELECT * FROM colleges WHERE college_name LIKE '%Aurangabad%'")
    rows = cursor.fetchall()
    print(f"Found {len(rows)} records.")
    for r in rows:
        print(r)
        
    conn.close()

if __name__ == "__main__":
    debug_city()
