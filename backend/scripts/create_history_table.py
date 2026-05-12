from database.db import get_db_connection

def create_history_table():
    """
    Create the missing user_history table
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        print("Creating user_history table...")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_history (
            history_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            action_type VARCHAR(50) NOT NULL,
            details JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
        """)
        
        conn.commit()
        print("[SUCCESS] user_history table created!")
        
        # Verify
        cursor.execute("DESCRIBE user_history")
        schema = cursor.fetchall()
        print("\nTable schema:")
        for col in schema:
            print(f"  {col[0]}: {col[1]}")
            
        return {"success": True}
        
    except Exception as e:
        print(f"[ERROR] {e}")
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_history_table()
