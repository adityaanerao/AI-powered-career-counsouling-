import requests
import json

def test_history():
    user_id = 1
    url = f"http://127.0.0.1:5000/api/history/{user_id}"
    
    print(f"Testing History API for user {user_id}...")
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.json()}")
        
        if response.status_code == 200:
            print("\n[SUCCESS] History API works!")
        else:
            print(f"\n[ERROR] History API failed with status {response.status_code}")
            
    except Exception as e:
        print(f"[ERROR] Request failed: {e}")

if __name__ == "__main__":
    test_history()
