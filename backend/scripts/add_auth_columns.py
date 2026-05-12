from database.db import get_db_connection

def add_missing_columns():
    """
    Add missing email and password_hash columns to users table
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check current schema
        cursor.execute("DESCRIBE users")
        schema = cursor.fetchall()
        existing_columns = [col[0] for col in schema]
        
        print("Current columns:", existing_columns)
        
        # Add email column if missing
        if 'email' not in existing_columns:
            print("\nAdding email column...")
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN email VARCHAR(100) UNIQUE
                AFTER full_name
            """)
            conn.commit()
            print("[SUCCESS] Added email column")
        else:
            print("[OK] email column already exists")
        
        # Add password_hash column if missing
        if 'password_hash' not in existing_columns:
            print("\nAdding password_hash column...")
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN password_hash VARCHAR(255)
                AFTER email
            """)
            conn.commit()
            print("[SUCCESS] Added password_hash column")
        else:
            print("[OK] password_hash column already exists")
        
        # Verify final schema
        cursor.execute("DESCRIBE users")
        schema = cursor.fetchall()
        print("\n=== Final users table schema ===")
        for column in schema:
            print(f"  {column[0]}: {column[1]} {column[2]}")
        
        return {"success": True}
        
    except Exception as e:
        print(f"[ERROR] {e}")
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    result = add_missing_columns()
    if "error" in result:
        print(f"\nFailed: {result['error']}")
    else:
        print("\n[SUCCESS] All required columns are present!")
