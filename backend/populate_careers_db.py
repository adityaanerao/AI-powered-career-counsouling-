from database.db import get_db_connection
import json

CAREER_DATA = [
    # 1. TECHNICAL (STEM)
    {
        "title": "Software Developer",
        "category": "Technical",
        "description": "Design, build, and maintain software applications. Requires strong logic and coding skills.",
        "skills": ["Java/Python", "Problem Solving", "Data Structures", "SQL"],
        "subjects": ["Computer Science", "Mathematics"],
        "min_cet_percentile": 85.0,
        "min_twelfth_percent": 60.0,
        "average_salary": "₹5 - ₹12 LPA",
        "demand_outlook": "High Growth",
        "is_trending": True,
        "top_colleges": ["IITs", "NITs", "COEP", "VJTI", "SPIT"],
        "entrance_exams": ["JEE Mains", "MHT-CET", "BITSAT"],
        "career_path": {
            "recommended_degree": "B.Tech in Computer Science / IT",
            "after_10th_path": "11th-12th Science (PCM)",
            "alternative_path": "BCA + MCA"
        },
        "category_weight": 1.2
    },
    {
        "title": "Data Scientist",
        "category": "Technical",
        "description": "Analyze complex data to help organizations make better decisions. Uses statistics and ML.",
        "skills": ["Python/R", "Statistics", "Machine Learning", "Data Visualization"],
        "subjects": ["Mathematics", "Statistics", "Computer Science"],
        "min_cet_percentile": 90.0,
        "min_twelfth_percent": 65.0,
        "average_salary": "₹8 - ₹15 LPA",
        "demand_outlook": "Very High",
        "is_trending": True,
        "top_colleges": ["IITs", "BITS Pilani", "IIIT Hyderabad", "ISI Kolkata"],
        "entrance_exams": ["JEE Advanced", "GATE (for Masters)"],
        "career_path": {
            "recommended_degree": "B.Tech in CS / B.Sc Statistics",
            "after_10th_path": "11th-12th Science (PCM)",
            "alternative_path": "B.Sc Data Science"
        },
        "category_weight": 1.2
    },
    {
        "title": "AI / ML Engineer",
        "category": "Technical",
        "description": "Build artificial intelligence models and machine learning systems.",
        "skills": ["Deep Learning", "Python", "TensorFlow", "Mathematics"],
        "subjects": ["Mathematics", "Computer Science"],
        "min_cet_percentile": 92.0,
        "min_twelfth_percent": 70.0,
        "average_salary": "₹10 - ₹20 LPA",
        "demand_outlook": "Explosive Growth",
        "is_trending": True,
        "top_colleges": ["IITs", "IIITs", "IISc Bangalore"],
        "entrance_exams": ["JEE Advanced", "GATE"],
        "career_path": {
            "recommended_degree": "B.Tech in AI & DS",
            "after_10th_path": "11th-12th Science (PCM)",
            "alternative_path": "B.Tech CS with AI Specialization"
        },
        "category_weight": 1.3
    },
    {
        "title": "Mechanical Engineer",
        "category": "Technical",
        "description": "Design, manufacture, and maintain mechanical systems and machinery.",
        "skills": ["CAD/CAM", "Thermodynamics", "Mechanics", "Problem Solving"],
        "subjects": ["Physics", "Mathematics"],
        "min_cet_percentile": 75.0,
        "min_twelfth_percent": 60.0,
        "average_salary": "₹4 - ₹8 LPA",
        "demand_outlook": "Stable",
        "is_trending": False,
        "top_colleges": ["IITs", "NITs", "COEP", "VJTI"],
        "entrance_exams": ["JEE Mains", "MHT-CET"],
        "career_path": {
            "recommended_degree": "B.E. / B.Tech Mechanical Engineering",
            "after_10th_path": "11th-12th Science (PCM)",
            "alternative_path": "Diploma in Mechanical Engg (3 Years)"
        },
        "category_weight": 1.0
    },
    {
        "title": "Civil Engineer",
        "category": "Technical",
        "description": "Plan, design, and oversee construction of infrastructure like roads, bridges, and buildings.",
        "skills": ["Structural Analysis", "AutoCAD", "Project Management"],
        "subjects": ["Physics", "Mathematics"],
        "min_cet_percentile": 70.0,
        "min_twelfth_percent": 55.0,
        "average_salary": "₹3.5 - ₹7 LPA",
        "demand_outlook": "Stable",
        "is_trending": False,
        "top_colleges": ["IITs", "NITs", "COEP", "Sardar Patel"],
        "entrance_exams": ["JEE Mains", "MHT-CET"],
        "career_path": {
            "recommended_degree": "B.E. Civil Engineering",
            "after_10th_path": "11th-12th Science (PCM)",
            "alternative_path": "Diploma in Civil Engg"
        },
        "category_weight": 1.0
    },

    # 2. NON-TECHNICAL (Business / Govt)
    {
        "title": "Business Analyst",
        "category": "Business",
        "description": "Bridge the gap between IT and business using data analytics to assess processes.",
        "skills": ["Data Analysis", "Communication", "SQL", "Excel"],
        "subjects": ["Mathematics", "Economics", "Business Studies"],
        "min_cet_percentile": 0,
        "min_twelfth_percent": 60.0,
        "average_salary": "₹6 - ₹12 LPA",
        "demand_outlook": "High",
        "is_trending": True,
        "top_colleges": ["IIMs", "NMIMS", "Symbiosis"],
        "entrance_exams": ["CAT", "XAT", "NMAT"],
        "career_path": {
            "recommended_degree": "MBA / PGDM in Business Analytics",
            "after_10th_path": "Any Stream (Science/Commerce preferred)",
            "alternative_path": "BBA + Work Ex"
        },
        "category_weight": 1.1
    },
    {
        "title": "Chartered Accountant (CA)",
        "category": "Business",
        "description": "Manage finances, taxation, auditing, and financial planning for businesses.",
        "skills": ["Accounting", "Taxation", "Auditing", "Financial Reporting"],
        "subjects": ["Accountancy", "Economics", "Maths"],
        "min_cet_percentile": 0,
        "min_twelfth_percent": 50.0, # Just passing usually, but high dedication
        "average_salary": "₹7 - ₹15 LPA",
        "demand_outlook": "Stable & High",
        "is_trending": False,
        "top_colleges": ["ICAI (Institute)"],
        "entrance_exams": ["CA Foundation", "CA Intermediate", "CA Final"],
        "career_path": {
            "recommended_degree": "CA Certification",
            "after_10th_path": "11th-12th Commerce",
            "alternative_path": "Direct Entry after Graduation"
        },
        "category_weight": 1.0
    },
    {
        "title": "Investment Banker",
        "category": "Business",
        "description": "Raise capital for corporations and governments, provide financial advice.",
        "skills": ["Financial Modeling", "Valuation", "Economics", "High Pressure Tolerance"],
        "subjects": ["Finance", "Economics", "Maths"],
        "min_cet_percentile": 0,
        "min_twelfth_percent": 75.0,
        "average_salary": "₹15 - ₹35 LPA",
        "demand_outlook": "High Rewards",
        "is_trending": True,
        "top_colleges": ["IIM A/B/C", "ISB", "JBIMS"],
        "entrance_exams": ["CAT", "GMAT"],
        "career_path": {
            "recommended_degree": "MBA in Finance",
            "after_10th_path": "11th-12th Commerce/Science",
            "alternative_path": "CFA Certification"
        },
        "category_weight": 1.2
    },
    {
        "title": "UPSC (IAS/IPS)",
        "category": "Government",
        "description": "Serve the nation in top administrative and police roles.",
        "skills": ["General Knowledge", "Decision Making", "Leadership", "Ethics"],
        "subjects": ["History", "Polity", "Geography", "Current Affairs"],
        "min_cet_percentile": 0,
        "min_twelfth_percent": 40.0, # Degree required
        "average_salary": "₹56,100 (Start) + Perks",
        "demand_outlook": "Competitive",
        "is_trending": False,
        "top_colleges": ["Any Recognized University"],
        "entrance_exams": ["UPSC Civil Services Exam"],
        "career_path": {
            "recommended_degree": "Any Graduation (BA/BSc/BCom/BTech)",
            "after_10th_path": "11th-12th Arts (Ideal for foundation)",
            "alternative_path": "Any Stream"
        },
        "category_weight": 1.0
    },

    # 3. ARTS & CREATIVE
    {
        "title": "Graphic Designer",
        "category": "Arts",
        "description": "Create visual concepts using computer software or by hand.",
        "skills": ["Creativity", "Adobe Suite", "Typography", "Visual Design"],
        "subjects": ["Art", "Drawing"],
        "min_cet_percentile": 0,
        "min_twelfth_percent": 50.0,
        "average_salary": "₹3 - ₹8 LPA",
        "demand_outlook": "Growing",
        "is_trending": True,
        "top_colleges": ["NID", "NIFT", "JJ School of Arts"],
        "entrance_exams": ["NID DAT", "UCEED"],
        "career_path": {
            "recommended_degree": "B.Des (Bachelor of Design)",
            "after_10th_path": "11th-12th Arts/Science/Commerce",
            "alternative_path": "Certification Courses / Portfolio"
        },
        "category_weight": 1.0
    },
    {
        "title": "Journalist / Content Writer",
        "category": "Arts",
        "description": "Research, write, and present news or content for media.",
        "skills": ["Writing", "Communication", "Research", "Curiosity"],
        "subjects": ["Literature", "Political Science"],
        "min_cet_percentile": 0,
        "min_twelfth_percent": 55.0,
        "average_salary": "₹3 - ₹7 LPA",
        "demand_outlook": "Digital Media Growing",
        "is_trending": False,
        "top_colleges": ["Asian College of Journalism", "IIMC", "Xavier's"],
        "entrance_exams": ["JMI Entrance", "IIMC Entrance"],
        "career_path": {
            "recommended_degree": "BMM / BA in Journalism",
            "after_10th_path": "11th-12th Arts",
            "alternative_path": "Blogging / Freelancing"
        },
        "category_weight": 1.0
    },

    # 4. MEDICAL (Science Non-Engg)
    {
        "title": "Doctor (MBBS)",
        "category": "Medical",
        "description": "Diagnose and treat illnesses. Requires extreme dedication.",
        "skills": ["Empathy", "Biology knowledge", "Patience", "Diagnosis"],
        "subjects": ["Biology", "Physics", "Chemistry"],
        "min_cet_percentile": 95.0, # Placeholder for NEET equivalent high score
        "min_twelfth_percent": 85.0, # PCB
        "average_salary": "₹8 - ₹20 LPA (Start)",
        "demand_outlook": "Always High",
        "is_trending": False,
        "top_colleges": ["AIIMS", "JIPMER", "KEM Mumbai", "BJ Medical"],
        "entrance_exams": ["NEET UG"],
        "career_path": {
            "recommended_degree": "MBBS",
            "after_10th_path": "11th-12th Science (PCB)",
            "alternative_path": "BAMS/BHMS (Ayurveda/Homeopathy)"
        },
        "category_weight": 1.3
    },
    {
        "title": "Pharmacist",
        "category": "Medical",
        "description": "Dispense medications and advise patients on their use.",
        "skills": ["Chemistry", "Accuracy", "Drug Knowledge"],
        "subjects": ["Chemistry", "Biology"],
        "min_cet_percentile": 70.0,
        "min_twelfth_percent": 60.0,
        "average_salary": "₹3 - ₹6 LPA",
        "demand_outlook": "Stable",
        "is_trending": False,
        "top_colleges": ["ICT Mumbai", "Bombay College of Pharmacy"],
        "entrance_exams": ["MHT-CET (Pharmacy)", "NEET"],
        "career_path": {
            "recommended_degree": "B.Pharm",
            "after_10th_path": "11th-12th Science (PCB/PCM)",
            "alternative_path": "D.Pharm (Diploma)"
        },
        "category_weight": 1.0
    },

    # 5. EMERGING
    {
        "title": "Digital Marketing Specialist",
        "category": "Emerging",
        "description": "Promote products/services using digital channels like SEO, Social Media.",
        "skills": ["SEO", "Content Marketing", "Social Media", "Analytics"],
        "subjects": ["Marketing", "English", "Psychology"],
        "min_cet_percentile": 0,
        "min_twelfth_percent": 50.0,
        "average_salary": "₹4 - ₹10 LPA",
        "demand_outlook": "Very High",
        "is_trending": True,
        "top_colleges": ["MICA", "Online Certifications"],
        "entrance_exams": ["None (Portfolio based)"],
        "career_path": {
            "recommended_degree": "BBA / MBA in Marketing",
            "after_10th_path": "Any Stream",
            "alternative_path": "Google/HubSpot Certifications"
        },
        "category_weight": 1.1
    },
    {
        "title": "Ethical Hacker",
        "category": "Technical",
        "description": "Identify vulnerabilities in systems to secure them from malicious hackers.",
        "skills": ["Networking", "Linux", "Scripting", "Cybersecurity"],
        "subjects": ["Computer Science"],
        "min_cet_percentile": 80.0,
        "min_twelfth_percent": 60.0,
        "average_salary": "₹8 - ₹18 LPA",
        "demand_outlook": "Critical Demand",
        "is_trending": True,
        "top_colleges": ["IITs", "Private Cyber Institutes"],
        "entrance_exams": ["CEH Certification", "OSCP"],
        "career_path": {
            "recommended_degree": "B.Tech CS / BCA",
            "after_10th_path": "11th-12th Science",
            "alternative_path": "Self-taught + Certifications"
        },
        "category_weight": 1.2
    }
]

def populate_careers():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        print(f"Populating {len(CAREER_DATA)} careers...")
        
        insert_query = """
        INSERT INTO careers (
            title, category, description, skills, subjects, 
            min_cet_percentile, min_twelfth_percent, 
            average_salary, demand_outlook, is_trending,
            top_colleges, entrance_exams, career_path, category_weight
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        for career in CAREER_DATA:
            val = (
                career["title"],
                career["category"],
                career["description"],
                json.dumps(career["skills"]),
                json.dumps(career["subjects"]),
                career["min_cet_percentile"],
                career["min_twelfth_percent"],
                career["average_salary"],
                career["demand_outlook"],
                career["is_trending"],
                json.dumps(career["top_colleges"]),
                json.dumps(career["entrance_exams"]),
                json.dumps(career["career_path"]),
                career["category_weight"]
            )
            cursor.execute(insert_query, val)
            
        conn.commit()
        print("[SUCCESS] All careers populated successfully!")
        
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    populate_careers()
