from app import app
import json

def test_endpoint(payload, name):
    print(f"\n--- Testing {name} ---")
    with app.test_client() as client:
        try:
            response = client.post('/eligible-colleges', json=payload)
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                print("Response: Success (truncated)")
                print(str(response.json)[:200])
            else:
                print("Response: Error")
                print(response.json)
        except Exception as e:
            print(f"Client Crash: {e}")

# Test Case 1: Engineering (CET)
payload_cet = {
    "exam_type": "CET",
    "cet_percentile": 88,
    "career": "Software Engineer",
    "category_code": "OPEN",
    "city": "Aurangabad"
}

# Test Case 2: SSC
payload_ssc = {
    "exam_type": "SSC",
    "cet_percentile": 85,
    "preferred_branch": "Science", 
    "category_code": "OPEN",
    "city": "Pune"
}

if __name__ == "__main__":
    test_endpoint(payload_cet, "CET Request")
    test_endpoint(payload_ssc, "SSC Request")
