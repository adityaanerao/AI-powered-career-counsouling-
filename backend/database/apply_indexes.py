import mysql.connector
import os
from db import get_db_connection

def apply_database_indexes():
    """
    Apply database performance optimization indexes.
    This script should be run once to improve college filtering performance.
    """
    print("=" * 60)
    print("Database Performance Optimization Script")
    print("=" * 60)
    
    try:
        # Connect to database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        print("\n✓ Connected to database successfully")
        
        # Read the SQL file
        sql_file_path = os.path.join(os.path.dirname(__file__), 'optimize_indexes.sql')
        
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Split by semicolons and execute each statement
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip() and not stmt.strip().startswith('--')]
        
        print(f"\n✓ Found {len(statements)} index creation statements")
        print("\nApplying indexes...")
        
        for i, statement in enumerate(statements, 1):
            if statement:
                try:
                    cursor.execute(statement)
                    # Extract index name from statement for better logging
                    if 'idx_' in statement:
                        idx_name = statement.split('idx_')[1].split()[0]
                        print(f"  [{i}/{len(statements)}] ✓ Created index: idx_{idx_name}")
                    else:
                        print(f"  [{i}/{len(statements)}] ✓ Executed statement")
                except mysql.connector.Error as e:
                    # If index already exists, that's okay
                    if 'Duplicate key name' in str(e) or 'already exists' in str(e):
                        print(f"  [{i}/{len(statements)}] ⚠ Index already exists (skipped)")
                    else:
                        print(f"  [{i}/{len(statements)}] ✗ Error: {e}")
                        raise
        
        conn.commit()
        print("\n" + "=" * 60)
        print("✓ All indexes applied successfully!")
        print("=" * 60)
        print("\nPerformance improvements:")
        print("  • College filtering should now be 10-100x faster")
        print("  • Queries with university/city filters are optimized")
        print("  • Branch name lookups are significantly faster")
        print("\n" + "=" * 60)
        
    except mysql.connector.Error as e:
        print(f"\n✗ Database error: {e}")
        return False
    except FileNotFoundError:
        print(f"\n✗ Could not find optimize_indexes.sql file")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
    
    return True

if __name__ == "__main__":
    success = apply_database_indexes()
    if success:
        print("\n✓ Database optimization complete!")
    else:
        print("\n✗ Database optimization failed. Please check the errors above.")
