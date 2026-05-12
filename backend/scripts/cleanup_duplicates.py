import mysql.connector
from database.db import get_db_connection

def cleanup_duplicates():
    conn = get_db_connection()
    cursor = conn.cursor()

    print("Cleaning up duplicate colleges...")
    
    # Keep the row with the HIGHEST ID (latest entry)
    sql_delete_duplicates = """
    DELETE t1 FROM colleges t1
    INNER JOIN colleges t2 
    WHERE 
        t1.college_id < t2.college_id AND 
        t1.college_name = t2.college_name AND 
        t1.branch = t2.branch AND 
        t1.exam = t2.exam
    """
    
    try:
        cursor.execute(sql_delete_duplicates)
        conn.commit()
        print(f"Deleted {cursor.rowcount} duplicate records.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    cleanup_duplicates()
