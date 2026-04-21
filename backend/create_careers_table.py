from database.db import get_db_connection

def create_careers_table():
    """
    Create the advanced careers table with rich metadata
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        print("Creating careers table...")
        
        # Drop table if exists to ensure clean schema (since we are migrating from json)
        # In production, we would use ALTER, but for this upgrade, a fresh table is cleaner
        cursor.execute("DROP TABLE IF EXISTS careers")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS careers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(150) NOT NULL,
            category VARCHAR(100) NOT NULL,
            description TEXT,
            
            -- JSON Fields for flexibility
            skills JSON,
            subjects JSON,
            top_colleges JSON,
            entrance_exams JSON,
            career_path JSON, 
            
            -- Academic Criteria
            min_cet_percentile FLOAT DEFAULT 0,
            min_twelfth_percent FLOAT DEFAULT 0,
            min_diploma_percent FLOAT DEFAULT 0,
            
            -- Metadata for Hybrid Scoring
            category_weight FLOAT DEFAULT 1.0,
            is_trending BOOLEAN DEFAULT FALSE,
            demand_outlook VARCHAR(50), -- High, Stable, Growing
            average_salary VARCHAR(100),
            
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        conn.commit()
        print("[SUCCESS] careers table created with advanced schema!")
        
        # Verify
        cursor.execute("DESCRIBE careers")
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
    create_careers_table()
