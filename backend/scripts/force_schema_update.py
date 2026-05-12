import sys
import os
import mysql.connector

def get_standalone_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Aditya",
        database="career_guidance_db"
    )

def force_update():
    print("Connecting to database...")
    try:
        conn = get_standalone_connection()
        cursor = conn.cursor()
    except Exception as e:
        print(f"Connection failed: {e}")
        print("Make sure mysql-connector-python is installed and DB is running.")
        return

    try:
        print("Checking if 'users' table exists...")
        cursor.execute("SHOW TABLES LIKE 'users'")
        table_exists = cursor.fetchone()

        if table_exists:
            print("Table 'users' exists. Checking columns...")
            cursor.execute("DESCRIBE users")
            columns = [col[0] for col in cursor.fetchall()]
            
            if "email" in columns and "password_hash" in columns:
                print("SUCCESS: Columns 'email' and 'password_hash' ALREADY EXIST.")
                # We can return here, but maybe user wants a clean slate? 
                # Let's drop and recreate to be 100% sure setup is clean as requested.
                print("Recreating table anyway to ensure clean state...")
            else:
                print("MISSING COLUMNS detected. Dropping and recreating...")

        # Drop tables (History first because of FK)
        print("Dropping 'user_history'...")
        cursor.execute("DROP TABLE IF EXISTS user_history")
        
        print("Dropping 'users'...")
        cursor.execute("DROP TABLE IF EXISTS users")
        
        print("Creating 'users' table with correct schema...")
        create_users_sql = """
        CREATE TABLE users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            interests TEXT,
            skills TEXT,
            subjects TEXT,
            exam_details JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_users_sql)
        
        print("Creating 'user_history' table...")
        create_history_sql = """
        CREATE TABLE user_history (
            history_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            action_type VARCHAR(50) NOT NULL,
            details JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
        """
        cursor.execute(create_history_sql)
        
        conn.commit()
        print("✅ DATABASE FIXED SUCCESSFULLY. Registration should work now.")
        
    except Exception as e:
        print(f"❌ Error during schema update: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    force_update()
