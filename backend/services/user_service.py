from database.db import get_db_connection
import json
import hashlib

# Simple hashing for demonstration (use bcrypt in production)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(full_name, email, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Check if email exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return {"error": "Email already exists"}
        
        password_hash = hash_password(password)
        
        cursor.execute(
            "INSERT INTO users (full_name, email, password_hash) VALUES (%s, %s, %s)",
            (full_name, email, password_hash)
        )
        conn.commit()
        
        user_id = cursor.lastrowid
        return {"success": True, "user_id": user_id, "name": full_name}
        
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()

def authenticate_user(email, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        password_hash = hash_password(password)
        cursor.execute(
            "SELECT user_id, full_name, email FROM users WHERE email = %s AND password_hash = %s",
            (email, password_hash)
        )
        user = cursor.fetchone()
        
        if user:
            return {"success": True, "user": user}
        else:
            return {"error": "Invalid email or password"}
            
    finally:
        cursor.close()
        conn.close()

def get_user_profile(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT full_name, email, interests, skills, subjects FROM users WHERE user_id = %s", (user_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def update_user_profile(user_id, data):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "UPDATE users SET interests = %s, skills = %s, subjects = %s WHERE user_id = %s",
            (data.get('interests'), data.get('skills'), data.get('subjects'), user_id)
        )
        conn.commit()
        return {"success": True}
    finally:
        cursor.close()
        conn.close()

def log_user_history(user_id, action_type, details):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        details_json = json.dumps(details)
        cursor.execute(
            "INSERT INTO user_history (user_id, action_type, details) VALUES (%s, %s, %s)",
            (user_id, action_type, details_json)
        )
        conn.commit()
        return {"success": True}
    except Exception as e:
        print(f"Error logging history: {e}")
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()

def get_user_history(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute(
            "SELECT action_type, details, created_at FROM user_history WHERE user_id = %s ORDER BY created_at DESC",
            (user_id,)
        )
        history = cursor.fetchall()
        
        # Parse JSON details
        for record in history:
            if isinstance(record['details'], str):
                record['details'] = json.loads(record['details'])
        
        return history
    finally:
        cursor.close()
        conn.close()

def get_analytics_data():
    """
    Generate aggregated reports from history data.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # report 1: Exam Popularity
        # Requires extracting exam type from JSON. 
        # Since JSON functions vary by MySQL version, we fetch all and aggregate in Python for safety/simplicity in this prototype
        # Or use simple string matching if volume is low.
        
        # Fetch all 'COLLEGE_CHECK' history
        cursor.execute("SELECT details FROM user_history WHERE action_type = 'COLLEGE_CHECK'")
        records = cursor.fetchall()
        
        exam_counts = {"CET": 0, "NEET": 0, "JEE": 0}
        career_counts = {}
        
        for record in records:
            try:
                details = json.loads(record['details']) if isinstance(record['details'], str) else record['details']
                
                # Count Exam
                if 'exam' in details:
                    exam = details['exam']
                    exam_counts[exam] = exam_counts.get(exam, 0) + 1
                    
                # Count Career
                if 'career' in details:
                    career = details['career']
                    career_counts[career] = career_counts.get(career, 0) + 1
                    
            except:
                continue
                
        # Sort careers by popularity
        sorted_careers = sorted(career_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "exam_popularity": exam_counts,
            "top_careers": dict(sorted_careers)
        }
        
    finally:
        cursor.close()
        conn.close()
