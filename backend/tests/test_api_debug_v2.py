from app import app
import json

def test_endpoint(payload, name):
    print(f"\n--- Testing {name} ---")
    with app.test_client() as client:
        try:
            response = client.post('/eligible-colleges', json=payload)
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                print("Response: Success")
            else:
                print("Response: Error")
                # print details if available
                try: print(response.json)
                except: print(response.data)
        except Exception as e:
            print(f"Client Crash: {e}")

# Test Case 1: SSC with NO branch (should default to all or handle gracefully)
payload_ssc_minimal = {
    "exam_type": "SSC",
    "cet_percentile": 80,
    # city, branch omitted
}

# Test Case 2: PG (GATE)
payload_pg = {
    "exam_type": "GATE",
    "cet_percentile": 90,
    "career": "Software Engineer"
}

# Test Case 3: Malformed payload (Missing critical fields? Percentile is robust now)
payload_bad = {
    "exam_type": "SSC",
    # No percentile
}

if __name__ == "__main__":
    test_endpoint(payload_ssc_minimal, "SSC Minimal")
    test_endpoint(payload_pg, "PG Request")
    test_endpoint(payload_bad, "Bad Request")
