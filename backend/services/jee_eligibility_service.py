from database.db import get_db_connection

# Engineering Career to Branch Mapping for JEE
# JEE is for premier engineering institutions (IITs, NITs, IIITs, GFTIs)
JEE_CAREER_BRANCH_MAP = {
    "Software Engineer": [
        "Computer Science and Engineering",
        "Information Technology",
        "Computer Engineering"
    ],
    "Data Scientist": [
        "Computer Science and Engineering",
        "Data Science and Engineering",
        "Artificial Intelligence"
    ],
    "AI/ML Engineer": [
        "Artificial Intelligence",
        "Computer Science and Engineering",
        "Data Science and Engineering"
    ],
    "Mechanical Engineer": [
        "Mechanical Engineering",
        "Production and Industrial Engineering",
        "Mechatronics Engineering"
    ],
    "Civil Engineer": [
        "Civil Engineering",
        "Environmental Engineering"
    ],
    "Electrical Engineer": [
        "Electrical Engineering",
        "Electrical and Electronics Engineering",
        "Power Engineering"
    ],
    "Electronics Engineer": [
        "Electronics and Communication Engineering",
        "Electronics Engineering",
        "VLSI Design"
    ],
    "Chemical Engineer": [
        "Chemical Engineering",
        "Biochemical Engineering"
    ],
    "Aerospace Engineer": [
        "Aerospace Engineering",
        "Aeronautical Engineering"
    ]
}


def get_eligible_colleges_jee(
        career,
        jee_percentile,
        category_code,
        university_id=None,
        city=None,
        preferred_branch=None
):
    """
    Get eligible engineering colleges based on JEE percentile and filters.
    JEE is for premier institutions like IITs, NITs, IIITs, and GFTIs.
    
    Args:
        career: Engineering career name (e.g., "Software Engineer", "Mechanical Engineer")
        jee_percentile: JEE percentile score (0-100)
        category_code: Reservation category (OPEN, EWS, OBC, SC, ST, etc.)
        university_id: Optional university filter
        city: Optional city filter
        preferred_branch: Optional specific branch (overrides career mapping)
    
    Returns:
        List of eligible colleges with details
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # If user selected a specific branch, use only that branch
    # Otherwise, use the career-to-branches mapping
    if preferred_branch:
        branches = [preferred_branch]
    else:
        branches = JEE_CAREER_BRANCH_MAP.get(career, [])
    
    if not branches:
        cursor.close()
        conn.close()
        return []

    branch_placeholders = ",".join(["%s"] * len(branches))

    # Optimized query with better JOIN order and LIMIT
    # Same structure as CET and NEET queries for consistency
    query = f"""
        SELECT
            c.college_name,
            u.university_name,
            c.city,
            b.branch_name,
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
    """

    params = branches + [category_code, jee_percentile]

    # Optional university filter (only apply if value is provided and not empty)
    if university_id and str(university_id).strip():
        query += " AND c.university_id = %s"
        params.append(university_id)

    # Optional city filter (only apply if value is provided and not empty)
    if city and str(city).strip():
        query += " AND c.city = %s"
        params.append(city)

    # Order by cutoff percentile descending and limit results to prevent overwhelming UI
    query += " ORDER BY cb.cutoff_percentile DESC LIMIT 100"

    cursor.execute(query, params)
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results
