import mysql.connector
from database.db import get_db_connection

def debug_cutoffs():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    print("--- Searching cutoffs for college_id=43 ---")
    cursor.execute("SELECT * FROM college_branch_cutoffs WHERE college_id = 43")
    rows = cursor.fetchall()
    print(f"Found {len(rows)} records.")
    for r in rows:
        print(r)
        
    conn.close()

if __name__ == "__main__":
    debug_cutoffs()
