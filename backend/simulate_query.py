import mysql.connector
from database.db import get_db_connection

CAREER_BRANCH_MAP = {
    "Software Engineer": [
        "Computer Engineering",
        "Information Technology",
        "Artificial Intelligence & Data Science",
        "Artificial Intelligence & Machine Learning",
        "Data Science"
    ]
}

def simulate_query():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    career = "Software Engineer"
    category_code = "OPEN"
    cet_percentile = 88.0 # From screenshot
    city = "Aurangabad"
    
    branches = CAREER_BRANCH_MAP.get(career, [])
    branch_placeholders = ",".join(["%s"] * len(branches))
    
    query = f"""
        SELECT
            c.college_name,
            u.university_name,
            c.city,
            c.college_id,
            b.branch_name,
            b.branch_id,
            cb.cutoff_id,
            cb.category_code,
            cb.cutoff_percentile,
            cb.available_seats
        FROM college_branch_cutoffs cb
        INNER JOIN branches b ON cb.branch_id = b.branch_id
        INNER JOIN colleges c ON cb.college_id = c.college_id
        INNER JOIN universities u ON c.university_id = u.university_id
        WHERE
            b.branch_name IN ({branch_placeholders})
            AND cb.category_code = %s
            AND cb.cutoff_percentile <= %s
            AND cb.available_seats > 0
            AND c.city = %s
        ORDER BY cb.cutoff_percentile DESC
    """
    
    params = branches + [category_code, cet_percentile, city]
    
    print("Executing query...")
    cursor.execute(query, params)
    results = cursor.fetchall()
    
    print(f"Found {len(results)} rows.")
    for r in results:
        print(f"ID: {r.get('college_id')}, BranchID: {r.get('branch_id')}, Branch: {r.get('branch_name')}, CutoffID: {r.get('cutoff_id')}")
        
    conn.close()

if __name__ == "__main__":
    simulate_query()
