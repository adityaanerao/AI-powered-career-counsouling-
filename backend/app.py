from flask import Flask, request, jsonify
from flask_cors import CORS
import json

from ai_modules.semantic_matcher import SemanticMatcher
from services.college_eligibility_service import get_eligible_colleges_cet, get_eligible_colleges_flat
from services.neet_eligibility_service import get_eligible_colleges_neet


from services.neet_eligibility_service import get_eligible_colleges_neet
from services.jee_eligibility_service import get_eligible_colleges_jee
from services.user_service import (
    register_user, authenticate_user, get_user_profile, 
    update_user_profile, log_user_history, get_user_history, get_analytics_data
)

app = Flask(__name__)

# Configure CORS to allow all origins for development
# In production, replace "*" with specific allowed origins
CORS(app, 
     origins="*",  # Allow all origins for development
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
     supports_credentials=False  # Must be False when using wildcard origin
)

# =====================================================
# AUTH & PROFILE ROUTES
# =====================================================
@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    result = register_user(data.get("full_name"), data.get("email"), data.get("password"))
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    result = authenticate_user(data.get("email"), data.get("password"))
    if "error" in result:
        return jsonify(result), 401
    return jsonify(result)

@app.route("/api/profile/<int:user_id>", methods=["GET", "POST"])
def profile(user_id):
    if request.method == "GET":
        profile = get_user_profile(user_id)
        if not profile:
            return jsonify({"error": "User not found"}), 404
        return jsonify(profile)
    else:
        # Update profile
        data = request.json
        result = update_user_profile(user_id, data)
        return jsonify(result)

@app.route("/api/history/<int:user_id>", methods=["GET"])
def history(user_id):
    history = get_user_history(user_id)
    return jsonify({"history": history})

@app.route("/api/analytics", methods=["GET"])
def analytics():
    data = get_analytics_data()
    return jsonify(data)

# Temporary route to fix DB schema issues
@app.route("/fix-db-schema", methods=["GET"])
def fix_db_schema():
    from database.db import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Drop old tables
        cursor.execute("DROP TABLE IF EXISTS user_history")
        cursor.execute("DROP TABLE IF EXISTS users")
        
        # Recreate tables
        # Users Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            interests TEXT,
            skills TEXT,
            subjects TEXT,
            exam_details JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        # History Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_history (
            history_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            action_type VARCHAR(50) NOT NULL,
            details JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
        """)
        
        conn.commit()
        return jsonify({"message": "Database schema recreated successfully. Users table now has email column."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# =====================================================
# HYBRID AI RECOMMENDATION ENGINE
# =====================================================

# 1. Load Careers from DB (Caching)
def load_careers_from_db():
    from database.db import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM careers")
        careers = cursor.fetchall()
        
        # Parse JSON fields
        for c in careers:
            c['skills'] = json.loads(c['skills']) if isinstance(c['skills'], str) else c['skills']
            c['subjects'] = json.loads(c['subjects']) if isinstance(c['subjects'], str) else c['subjects']
            c['top_colleges'] = json.loads(c['top_colleges']) if isinstance(c['top_colleges'], str) else c['top_colleges']
            c['entrance_exams'] = json.loads(c['entrance_exams']) if isinstance(c['entrance_exams'], str) else c['entrance_exams']
            c['career_path'] = json.loads(c['career_path']) if isinstance(c['career_path'], str) else c['career_path']
        return careers
    except Exception as e:
        print(f"Error loading careers: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

# Load at startup
CACHED_CAREERS = load_careers_from_db()
print(f"Loaded {len(CACHED_CAREERS)} careers from database.")

matcher = SemanticMatcher()

# 2. Rule-Based Category Detection
CATEGORY_KEYWORDS = {
    "Technical": ["coding", "technology", "software", "computer", "programming", "engineering", "machine", "data", "ai", "electronics"],
    "Medical": ["biology", "doctor", "medicine", "health", "hospital", "patient", "pharmacy", "healing"],
    "Business": ["management", "finance", "marketing", "business", "money", "economics", "leadership", "sales", "strategy"],
    "Arts": ["design", "drawing", "creative", "art", "writing", "music", "media", "film", "story", "animation"],
    "Government": ["upsc", "civil service", "government", "policy", "social work", "public service", "law", "police"],
    "Emerging": ["digital", "crypto", "blockchain", "startup", "innovation", "trend"]
}

def detect_dominant_category(text):
    text = text.lower()
    scores = {cat: 0 for cat in CATEGORY_KEYWORDS}
    
    for cat, keywords in CATEGORY_KEYWORDS.items():
        for word in keywords:
            if word in text:
                scores[cat] += 1
    
    # Return category with max score if score > 0
    best_cat = max(scores, key=scores.get)
    return best_cat if scores[best_cat] > 0 else None

# 3. Hybrid Scoring Logic
def calculate_hybrid_score(career, user_input, semantic_score, dominant_category):
    score = 0
    explanation = []
    
    # A. Semantic Score (Weight: 60%)
    score += semantic_score * 0.6
    
    # B. Category Match (Weight: 20%)
    if dominant_category and career['category'] == dominant_category:
        score += 0.2
        explanation.append(f"Matches your dominant interest in {dominant_category} fields")
        
        # Apply category weight from DB (e.g. 1.2x boost for high priority)
        if career.get('category_weight'):
            score *= career['category_weight']
            
    # C. Academic/Trending Boost (Weight: 20%)
    # Trending Boost
    if career.get('is_trending'):
        score += 0.1
        explanation.append("This is a high-demand trending career")
        
    # User Academic Inputs (Simplified for this function, detailed filtering happens before)
    if user_input['cet_percentile'] >= career.get('min_cet_percentile', 0):
        score += 0.1
    
    return score, explanation

# 4. Recommendation API
@app.route("/recommend", methods=["POST"])
def recommend_careers():
    try:
        data = request.json
        interests = data.get("interests", "")
        skills = data.get("skills", "")
        subjects = data.get("subjects", "")
        cet = float(data.get("cet_percentile", 0))
        twelfth = float(data.get("twelfth_percent", 0))
        
        user_text = f"{interests} {skills} {subjects}"
        dominant_cat = detect_dominant_category(user_text)
        
        # Reload careers if cache is empty (fail-safe)
        global CACHED_CAREERS
        if not CACHED_CAREERS:
            CACHED_CAREERS = load_careers_from_db()
            
        candidate_careers = []
        
        # A. Strict Filtering (Academic)
        for career in CACHED_CAREERS:
            # 1. Medical Strict Filter
            if career['category'] == 'Medical':
                # Require biology in user text OR strict high scores
                if "biology" not in user_text.lower() and twelfth < 50:
                    continue # Skip if no biology background
                    
            # 2. Engineering Strict Filter (if specified)
            if career['category'] == 'Technical' and 'Engineer' in career['title']:
                if twelfth < 50: # Basic science requirement
                    continue
            
            candidate_careers.append(career)
            
        # B. Semantic Matching
        descriptions = [c['description'] + " " + " ".join(c['skills']) for c in candidate_careers]
        matches = matcher.match_careers(user_text, descriptions) # Returns [(index, score), ...]
        
        # C. Hybrid Scoring & Ranking
        final_results = []
        ids_seen = set()
        
        for idx, sem_score in matches:
            if idx >= len(candidate_careers): continue
            
            career = candidate_careers[idx]
            if career['id'] in ids_seen: continue
            
            hybrid_score, expl = calculate_hybrid_score(career, 
                                                      {'cet_percentile': cet, 'twelfth_percent': twelfth}, 
                                                      sem_score, 
                                                      dominant_cat)
            
            # Format Explanation
            if sem_score > 0.4:
                expl.insert(0, "Strong match with your skills and interests")
            
            # Add strict academic feedback to explanation
            if cet >= career.get('min_cet_percentile', 0) and career.get('min_cet_percentile', 0) > 0:
                expl.append(f"Your CET ({cet}%) meets the requirement ({career['min_cet_percentile']}%)")
            
            res_obj = {
                "career": career['title'],
                "category": career['category'],
                "description": career['description'],
                "hybrid_score": round(hybrid_score * 100, 1), # Convert to percentage-like
                "match_percentage": round(hybrid_score * 100),
                "explanation": expl,
                "salary": career['average_salary'],
                "outlook": career['demand_outlook'],
                "top_colleges": career['top_colleges'],
                "entrance_exams": career['entrance_exams'],
                "career_path": career['career_path']
            }
            final_results.append(res_obj)
            ids_seen.add(career['id'])
            
        # Sort by Hybrid Score
        final_results.sort(key=lambda x: x['hybrid_score'], reverse=True)
        
        # D. Diversity Control (Max 3 per category)
        diverse_results = []
        cat_counts = {}
        for res in final_results:
            cat = res['category']
            if cat_counts.get(cat, 0) < 3:
                diverse_results.append(res)
                cat_counts[cat] = cat_counts.get(cat, 0) + 1
            if len(diverse_results) >= 6: # Limit total results
                break
                
        return jsonify({
            "recommendations": diverse_results,
            "dominant_category": dominant_cat
        })
        
    except Exception as e:
        print(f"Recommendation Error: {e}")
        return jsonify({"error": str(e)}), 500


# =====================================================
# ELIGIBLE COLLEGES API (CET & NEET Support)
# =====================================================
@app.route("/eligible-colleges", methods=["POST"])
def eligible_colleges():
    try:
        data = request.json
        print("DEBUG: /eligible-colleges payload:", data)  # Debug print

        career = data.get("career")
        category_code = data.get("category_code")
        exam_type = data.get("exam_type", "CET")  # Default to CET for backward compatibility

        # Optional filters - default to None if not provided
        university_id = data.get("university_id", None)
        city = data.get("city", None)
        preferred_branch = data.get("preferred_branch", None)

        # Route to appropriate service based on exam type
        if exam_type == "NEET":
            neet_percentile = float(data.get("neet_percentile") or 0)
            colleges = get_eligible_colleges_neet(
                career=career,
                neet_percentile=neet_percentile,
                category_code=category_code,
                university_id=university_id,
                city=city,
                preferred_branch=preferred_branch
            )
            percentile_key = "neet_percentile"
            percentile_value = neet_percentile
        elif exam_type == "JEE":
            jee_percentile = float(data.get("jee_percentile") or 0)
            colleges = get_eligible_colleges_jee(
                career=career,
                jee_percentile=jee_percentile,
                category_code=category_code,
                university_id=university_id,
                city=city,
                preferred_branch=preferred_branch
            )
            percentile_key = "jee_percentile"
            percentile_value = jee_percentile
        elif exam_type in ["CET", "MHT-CET"]:
            cet_percentile = float(data.get("cet_percentile") or 0)
            colleges = get_eligible_colleges_cet(
                career=career,
                cet_percentile=cet_percentile,
                category_code=category_code,
                university_id=university_id,
                city=city,
                preferred_branch=preferred_branch
            )
            percentile_key = "cet_percentile"
            percentile_value = cet_percentile
        else:
            # SSC, CAT, GATE, MCA-CET, CET-PG (Use Flat Table)
            # script.js sends 'cet_percentile' for these types in the 'else' block
            exam_percentile = float(data.get("cet_percentile") or 0)
            colleges = get_eligible_colleges_flat(
                exam_type=exam_type,
                cutoff_percentile=exam_percentile,
                city=city,
                preferred_branch=preferred_branch
            )
            percentile_key = "exam_percentile"
            percentile_value = exam_percentile

        # HISTORY LOGGING
        # Check if user_id was sent in request (optional, only if logged in)
        user_id = data.get("user_id")
        if user_id:
            # Create a snapshot of this search
            history_details = {
                "exam": exam_type,
                "percentile": percentile_value,
                "category": category_code,
                "career": career,
                "colleges_found_count": len(colleges) if colleges else 0,
                "preferred_branch": preferred_branch,
                "city_filter": city
            }
            # Log it (async or fire-and-forget in production, but synchronous here is fine)
            log_user_history(user_id, "COLLEGE_CHECK", history_details)

        return jsonify({
            "exam_type": exam_type,
            "career": career,
            "category": category_code,
            percentile_key: percentile_value,
            "eligible_colleges": colleges
        })

    except Exception as e:
        import traceback
        error_msg = str(e)
        print("ERROR in /eligible-colleges:", error_msg)
        print(traceback.format_exc())
        return jsonify({"error": error_msg, "details": traceback.format_exc()}), 500



# Temporary route to optimize DB (Add Indexes)
@app.route("/optimize-db", methods=["GET"])
def optimize_db():
    from database.db import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Array of index creation commands
        indexes = [
            "CREATE INDEX idx_users_email ON users(email)",
            "CREATE INDEX idx_colleges_course ON colleges(course)",
            "CREATE INDEX idx_colleges_city ON colleges(city)",
            "CREATE INDEX idx_colleges_cutoff ON colleges(cutoff)"
        ]
        
        results = []
        for idx_sql in indexes:
            try:
                cursor.execute(idx_sql)
                results.append(f"Success: {idx_sql}")
            except Exception as e:
                # Ignore if index already exists (Error 1061)
                if "Duplicate key name" in str(e):
                    results.append(f"Skipped (Exists): {idx_sql}")
                else:
                    results.append(f"Error: {str(e)}")
        
        conn.commit()
        return jsonify({"message": "Optimization completed", "details": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# =====================================================
# App Runner
# Temporary route to debug DB schema
@app.route("/debug-schema", methods=["GET"])
def debug_schema():
    from database.db import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DESCRIBE users")
        users_schema = cursor.fetchall()
        
        cursor.execute("DESCRIBE user_history")
        history_schema = cursor.fetchall()
        
        return jsonify({
            "users_table": users_schema,
            "history_table": history_schema
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# =====================================================
if __name__ == "__main__":
    app.run(debug=True)
