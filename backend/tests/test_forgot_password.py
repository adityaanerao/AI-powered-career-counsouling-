#!/usr/bin/env python3
"""
Test script for the forgot password flow.
Tests all three API endpoints: forgot-password, verify-otp, reset-password
"""

import requests
import json
import sys
import time

BASE_URL = "http://127.0.0.1:5000"

def test_forgot_password(email):
    """Test initiating password reset"""
    print(f"\n=== Testing forgot-password for {email} ===")
    payload = {"email": email}
    
    try:
        response = requests.post(f"{BASE_URL}/api/forgot-password", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('message', 'No message')}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"Request failed: {e}")
        return False

def test_verify_otp(email, otp):
    """Test OTP verification"""
    print(f"\n=== Testing verify-otp for {email} ===")
    payload = {"email": email, "otp": otp}
    
    try:
        response = requests.post(f"{BASE_URL}/api/verify-otp", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            reset_token = data.get("reset_token")
            print(f"Success! Reset token: {reset_token[:20]}...")
            return reset_token
        else:
            print(f"Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"Request failed: {e}")
        return None

def test_reset_password(email, reset_token, new_password):
    """Test password reset"""
    print(f"\n=== Testing reset-password for {email} ===")
    payload = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/reset-password", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('message', 'No message')}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"Request failed: {e}")
        return False

def test_login(email, password):
    """Test login with new password"""
    print(f"\n=== Testing login with new password for {email} ===")
    payload = {"email": email, "password": password}
    
    try:
        response = requests.post(f"{BASE_URL}/api/login", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Login successful! User ID: {data.get('user_id')}")
            return True
        else:
            print(f"Login failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"Request failed: {e}")
        return False

def main():
    print("=== Forgot Password Flow Test ===\n")
    
    # Test with a known user email
    test_email = "test@example.com"
    test_otp = "123456"  # This will be printed in console by send_otp_email
    new_password = "newpassword123"
    
    # Step 1: Initiate password reset
    if not test_forgot_password(test_email):
        print("Failed to initiate password reset. Checking if user exists...")
        
        # Try to create a test user first
        print("\nCreating test user...")
        create_payload = {
            "full_name": "Test User",
            "email": test_email,
            "password": "password123"
        }
        try:
            response = requests.post(f"{BASE_URL}/api/register", json=create_payload)
            if response.status_code == 200:
                print("Test user created successfully")
                # Try forgot password again
                if not test_forgot_password(test_email):
                    print("Still failing. Exiting.")
                    return
            else:
                print(f"Failed to create test user: {response.text}")
                return
        except Exception as e:
            print(f"Failed to create test user: {e}")
            return
    
    # Step 2: Check console for OTP (simulated email)
    print("\n=== IMPORTANT ===")
    print("Check the server console for the OTP that was 'sent' via email.")
    print("The OTP should be printed in the console where app.py is running.")
    print("Enter that OTP below to continue testing.")
    print("=================\n")
    
    # For automated testing, we need to get the OTP from the database
    # Let's try to fetch it
    import mysql.connector
    from database.db import get_db_connection
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT otp_code FROM password_reset_tokens 
            WHERE email = %s AND used = 0 AND expires_at > NOW()
            ORDER BY created_at DESC LIMIT 1
        """, (test_email,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if result:
            actual_otp = result["otp_code"]
            print(f"Found OTP in database: {actual_otp}")
            test_otp = actual_otp
        else:
            print("No OTP found in database. Using default 123456")
    except Exception as e:
        print(f"Could not fetch OTP from database: {e}")
        print("Using default OTP: 123456")
    
    # Step 3: Verify OTP
    reset_token = test_verify_otp(test_email, test_otp)
    if not reset_token:
        print("OTP verification failed. Exiting.")
        return
    
    # Step 4: Reset password
    if not test_reset_password(test_email, reset_token, new_password):
        print("Password reset failed. Exiting.")
        return
    
    # Step 5: Test login with new password
    if not test_login(test_email, new_password):
        print("Login with new password failed.")
        return
    
    print("\n=== TEST COMPLETE ===")
    print("Forgot password flow works correctly!")

if __name__ == "__main__":
    main()