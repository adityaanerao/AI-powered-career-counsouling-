import requests
import json
import time

def test_endpoint():
    url = "http://127.0.0.1:5000/eligible-colleges"
    
    payload = {
        "exam_type": "SSC",
        "cet_percentile": 85,
        "city": "Pune",
        "preferred_branch": None,
        "category_code": "OPEN"
    }

    try:
        print(f"Sending POST to {url}")
        start = time.time()
        response = requests.post(url, json=payload, timeout=10)
        end = time.time()
        
        print(f"Status Code: {response.status_code}")
        print(f"Time Taken: {end - start:.2f}s")
        
        try:
            print("Response JSON:", response.json())
        except:
            print("Response Text:", response.text)
            
    except Exception as e:
        print(f"Request Failed: {e}")

if __name__ == "__main__":
    test_endpoint()
