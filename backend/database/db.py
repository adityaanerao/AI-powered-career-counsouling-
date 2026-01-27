import mysql.connector
from mysql.connector import pooling

# Create a connection pool
db_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="career_pool",
    pool_size=10,
    pool_reset_session=True,
    host="localhost",
    user="root",
    password="Aditya",
    database="career_guidance_db"
)

def get_db_connection():
    try:
        connection = db_pool.get_connection()
        if connection.is_connected():
            return connection
    except Exception as e:
        print(f"Error getting connection from pool: {e}")
        # Fallback if pool is exhausted (optional, or just raise)
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Aditya",
            database="career_guidance_db"
        )
