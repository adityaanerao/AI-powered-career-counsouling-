from database.db import get_db_connection

def fix_database_schema():
    """
    Fix the database schema by adding the missing full_name column to users table
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if full_name column exists
        cursor.execute("SHOW COLUMNS FROM users LIKE 'full_name'")
        result = cursor.fetchone()
        
        if not result:
            print("Adding full_name column to users table...")
            # Add the full_name column
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN full_name VARCHAR(100) NOT NULL DEFAULT 'User'
                AFTER user_id
            """)
            conn.commit()
            print("[SUCCESS] Successfully added full_name column to users table")
        else:
            print("[OK] full_name column already exists in users table")
        
        # Verify the schema
        cursor.execute("DESCRIBE users")
        schema = cursor.fetchall()
        print("\nCurrent users table schema:")
        for column in schema:
            print(f"  - {column[0]}: {column[1]}")
        
        return {"success": True, "message": "Database schema fixed successfully"}
        
    except Exception as e:
        print(f"[ERROR] Error fixing database schema: {e}")
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    result = fix_database_schema()
    if "error" in result:
        print(f"\nFailed: {result['error']}")
    else:
        print(f"\n{result['message']}")

