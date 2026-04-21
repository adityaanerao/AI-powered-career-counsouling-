import mysql.connector
from database.db import get_db_connection

def debug_data():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    print("Checking for Aurangabad colleges...")
    cursor.execute("SELECT * FROM colleges WHERE college_name LIKE '%Aurangabad%'")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        
    print("\nChecking for potential duplicates (Name + Branch)...")
    cursor.execute("""
        SELECT college_name, branch, COUNT(*) as count 
        FROM colleges 
        GROUP BY college_name, branch 
        HAVING count > 1
    """)
    dupes = cursor.fetchall()
    for d in dupes:
        print(d)

    conn.close()

if __name__ == "__main__":
    debug_data()
