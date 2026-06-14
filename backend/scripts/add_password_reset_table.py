#!/usr/bin/env python3
"""
Script to add password_reset_tokens table to the database.
Run this script before testing the forgot password functionality.
"""

from database.db import get_db_connection

def add_password_reset_table():
    """Create password_reset_tokens table if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if table already exists
        cursor.execute("SHOW TABLES LIKE 'password_reset_tokens'")
        if cursor.fetchone():
            print("Table 'password_reset_tokens' already exists.")
            return True
        
        # Create the table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS password_reset_tokens (
            token_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            email VARCHAR(100) NOT NULL,
            otp_code VARCHAR(10) NOT NULL,
            token_hash VARCHAR(255) NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            used BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
            INDEX idx_token_hash (token_hash),
            INDEX idx_email_otp (email, otp_code)
        );
        """
        
        cursor.execute(create_table_sql)
        conn.commit()
        print("Table 'password_reset_tokens' created successfully.")
        return True
        
    except Exception as e:
        print(f"Error creating table: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("Adding password_reset_tokens table to database...")
    success = add_password_reset_table()
    if success:
        print("Database schema updated successfully.")
    else:
        print("Failed to update database schema.")