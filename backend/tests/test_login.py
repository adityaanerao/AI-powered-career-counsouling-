import requests
import json

# Test the login endpoint
def test_login():
    url = "http://127.0.0.1:5000/api/login"
    
    # First, let's register a test user
    register_url = "http://127.0.0.1:5000/api/register"
    register_data = {
        "full_name": "Test User",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    print("=== Testing Registration ===")
    try:
        response = requests.post(register_url, json=register_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
    except Exception as e:
        print(f"Registration Error: {e}")
        print()
    
    # Now test login
    print("=== Testing Login ===")
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(url, json=login_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.json()}")
        
        # Check for CORS headers
        if 'Access-Control-Allow-Origin' in response.headers:
            print(f"\n[SUCCESS] CORS header present: {response.headers['Access-Control-Allow-Origin']}")
        else:
            print("\n[WARNING] CORS header missing!")
        
        if response.status_code == 200:
            print("\n[SUCCESS] Login successful!")
        else:
            print(f"\n[ERROR] Login failed with status {response.status_code}")
            
    except Exception as e:
        print(f"[ERROR] Request failed: {e}")

if __name__ == "__main__":
    test_login()
