import requests
import json

def test_recommendation_engine():
    url = "http://127.0.0.1:5000/recommend"
    
    # Test Case 1: Technical (Software)
    print("\n=== Test Case 1: Technical User (Coding) ===")
    payload_tech = {
        "interests": "coding, technology, problem solving",
        "skills": "python, java, programming",
        "subjects": "computer science, mathematics",
        "cet_percentile": 92.5,
        "twelfth_percent": 85.0
    }
    
    try:
        response = requests.post(url, json=payload_tech)
        data = response.json()
        
        print(f"Dominant Category: {data.get('dominant_category')}")
        print(f"Recommendations: {len(data.get('recommendations', []))}")
        
        for rec in data.get('recommendations', [])[:3]:
            print(f"- {rec['career']} ({rec['match_percentage']}%) [{rec['category']}]")
            print(f"  Explain: {rec['explanation'][0]}")
            
    except Exception as e:
        print(f"Error: {e}")

    # Test Case 2: Medical (Doctor)
    print("\n=== Test Case 2: Medical User (Biology) ===")
    payload_med = {
        "interests": "biology, healing, patient care",
        "skills": "empathy, diagnosis",
        "subjects": "biology, chemistry",
        "cet_percentile": 96.0, # High enough for Medical
        "twelfth_percent": 88.0
    }
    
    try:
        response = requests.post(url, json=payload_med)
        data = response.json()
        
        print(f"Dominant Category: {data.get('dominant_category')}")
        for rec in data.get('recommendations', [])[:2]:
            print(f"- {rec['career']} ({rec['match_percentage']}%)")
            
    except Exception as e:
        print(f"Error: {e}")

    # Test Case 3: Mixed/Low Score (Should filter strict fields)
    print("\n=== Test Case 3: Low Score Engineering Check ===")
    payload_low = {
        "interests": "engineering, machines",
        "skills": "repairing",
        "subjects": "physics",
        "cet_percentile": 40.0, # Low score
        "twelfth_percent": 45.0 # Low score
    }
    
    try:
        response = requests.post(url, json=payload_low)
        data = response.json()
        
        print(f"Dominant Category: {data.get('dominant_category')}")
        print("Recommendations:")
        for rec in data.get('recommendations', []):
            print(f"- {rec['career']} (Score: {rec['match_percentage']}%)")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_recommendation_engine()
