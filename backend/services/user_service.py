from database.db import get_db_connection
import json
import hashlib
import random
import string
import time
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config

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


# =====================================================
# PASSWORD RESET FUNCTIONS
# =====================================================

def generate_otp(length=6):
    """Generate a numeric OTP code."""
    return ''.join(random.choices(string.digits, k=length))

def send_otp_email(email, otp_code):
    """
    Send OTP via email using SMTP.
    """
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = f"{config.SMTP_FROM_NAME} <{config.SMTP_FROM_EMAIL}>"
        msg['To'] = email
        msg['Subject'] = config.EMAIL_SUBJECT
        
        body = config.EMAIL_BODY_TEMPLATE.format(
            otp_code=otp_code,
            expiry_minutes=config.OTP_EXPIRY_MINUTES
        )
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to SMTP server
        server = smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT)
        server.starttls()
        server.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"[EMAIL SENT] OTP for {email}: {otp_code}")
        return True
    except Exception as e:
        # Fallback to console simulation if email fails
        print(f"[EMAIL FAILED] Could not send email: {e}")
        print(f"[EMAIL SIMULATION] OTP for {email}: {otp_code}")
        return False

def initiate_password_reset(email):
    """
    Initiate password reset process by generating OTP and sending email.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Check if user exists
        cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        if not user:
            return {"error": "No account found with this email"}
        
        user_id = user['user_id']
        
        # Generate OTP
        otp_code = generate_otp()
        
        # Create token hash (for security, we store hash of OTP)
        token_hash = hashlib.sha256(otp_code.encode()).hexdigest()
        
        # Set expiration (10 minutes from now)
        expires_at = datetime.datetime.now() + datetime.timedelta(minutes=10)
        
        # Store in password_reset_tokens table
        cursor.execute(
            """INSERT INTO password_reset_tokens
               (user_id, email, otp_code, token_hash, expires_at, used)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (user_id, email, otp_code, token_hash, expires_at, False)
        )
        conn.commit()
        
        # Send OTP via email (simulated)
        send_otp_email(email, otp_code)
        
        return {
            "success": True,
            "message": "OTP sent to your email",
            "email": email,
            "otp_length": len(otp_code)
        }
        
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()

def verify_otp(email, otp_code):
    """
    Verify OTP code for password reset.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Find valid, unused token
        cursor.execute(
            """SELECT token_id, user_id, expires_at, used
               FROM password_reset_tokens
               WHERE email = %s AND otp_code = %s AND used = FALSE
               ORDER BY created_at DESC LIMIT 1""",
            (email, otp_code)
        )
        token = cursor.fetchone()
        
        if not token:
            return {"error": "Invalid or expired OTP"}
        
        # Check if token is expired
        if token['expires_at'] < datetime.datetime.now():
            return {"error": "OTP has expired"}
        
        # Mark token as used
        cursor.execute(
            "UPDATE password_reset_tokens SET used = TRUE WHERE token_id = %s",
            (token['token_id'],)
        )
        conn.commit()
        
        # Generate a reset token for the next step
        reset_token = hashlib.sha256(f"{email}{otp_code}{time.time()}".encode()).hexdigest()
        
        # Store reset token (simplified - in production use JWT or similar)
        cursor.execute(
            """INSERT INTO password_reset_tokens
               (user_id, email, otp_code, token_hash, expires_at, used)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (token['user_id'], email, 'RESET', reset_token,
             datetime.datetime.now() + datetime.timedelta(minutes=15), False)
        )
        conn.commit()
        
        return {
            "success": True,
            "message": "OTP verified successfully",
            "reset_token": reset_token,
            "user_id": token['user_id']
        }
        
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()

def reset_password(email, reset_token, new_password):
    """
    Reset password using valid reset token.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Find valid reset token
        cursor.execute(
            """SELECT user_id, expires_at, used
               FROM password_reset_tokens
               WHERE email = %s AND token_hash = %s AND otp_code = 'RESET' AND used = FALSE
               ORDER BY created_at DESC LIMIT 1""",
            (email, reset_token)
        )
        token = cursor.fetchone()
        
        if not token:
            return {"error": "Invalid or expired reset token"}
        
        user_id, expires_at, used = token
        
        # Check if token is expired
        if expires_at < datetime.datetime.now():
            return {"error": "Reset token has expired"}
        
        # Hash new password
        new_password_hash = hash_password(new_password)
        
        # Update user password
        cursor.execute(
            "UPDATE users SET password_hash = %s WHERE user_id = %s",
            (new_password_hash, user_id)
        )
        
        # Mark token as used
        cursor.execute(
            "UPDATE password_reset_tokens SET used = TRUE WHERE token_hash = %s",
            (reset_token,)
        )
        
        conn.commit()
        
        return {
            "success": True,
            "message": "Password reset successfully"
        }
        
    except Exception as e:
        return {"error": str(e)}
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
