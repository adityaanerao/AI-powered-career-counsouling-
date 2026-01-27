from flask import Flask, request, jsonify
from flask_cors import CORS
import json

from ai_modules.semantic_matcher import SemanticMatcher
from services.college_eligibility_service import get_eligible_colleges_cet
from services.neet_eligibility_service import get_eligible_colleges_neet
from services.college_eligibility_service import get_eligible_colleges_cet
from services.neet_eligibility_service import get_eligible_colleges_neet
from services.jee_eligibility_service import get_eligible_colleges_jee
from services.user_service import (
    register_user, authenticate_user, get_user_profile, 
    update_user_profile, log_user_history, get_user_history, get_analytics_data
)

app = Flask(__name__)
CORS(app)

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
# Load Career Data (AI part)
# =====================================================
with open("data/careers.json", "r", encoding="utf-8") as f:
    careers = json.load(f)

career_descriptions = [career["description"] for career in careers]

matcher = SemanticMatcher()

# =====================================================
# AI Career Recommendation API
# =====================================================
@app.route("/recommend", methods=["POST"])
def recommend_careers():
    data = request.json

    interests = data.get("interests", "")
    skills = data.get("skills", "")
    subjects = data.get("subjects", "")
    cet = float(data.get("cet_percentile", 0))
    twelfth = float(data.get("twelfth_percent", 0))

    user_text = f"Interests: {interests}. Skills: {skills}. Subjects: {subjects}."

    results = matcher.match_careers(user_text, career_descriptions)

    recommendations = []

    for idx, sbert_score in results:
        # Suitability score (Explainable)
        suitability_score = (
            (sbert_score * 60) +
            (cet * 0.3) +
            (twelfth * 0.1)
        )

        # Explanation (Rule-based)
        explanation = []

        if "technology" in interests.lower() or "coding" in skills.lower():
            explanation.append("Strong interest in technology and programming")

        if cet >= 90:
            explanation.append("High CET percentile indicating strong aptitude")

        if twelfth >= 70:
            explanation.append("Good academic performance in 12th standard")

        recommendations.append({
            "career": careers[idx]["title"],
            "description": careers[idx]["description"],
            "sbert_score": round(sbert_score, 3),
            "suitability_score": round(suitability_score, 2),
            "explanation": explanation
        })

    return jsonify({
        "recommendations": recommendations
    })


# =====================================================
# ELIGIBLE COLLEGES API (CET & NEET Support)
# =====================================================
@app.route("/eligible-colleges", methods=["POST"])
def eligible_colleges():
    data = request.json

    career = data.get("career")
    category_code = data.get("category_code")
    exam_type = data.get("exam_type", "CET")  # Default to CET for backward compatibility

    # Optional filters - default to None if not provided
    university_id = data.get("university_id", None)
    city = data.get("city", None)
    preferred_branch = data.get("preferred_branch", None)

    # Route to appropriate service based on exam type
    if exam_type == "NEET":
        neet_percentile = float(data.get("neet_percentile", 0))
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
        jee_percentile = float(data.get("jee_percentile", 0))
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
    else:  # CET
        cet_percentile = float(data.get("cet_percentile", 0))
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
