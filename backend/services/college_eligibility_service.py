from database.db import get_db_connection

CAREER_BRANCH_MAP = {
    "Software Engineer": [
        "Computer Engineering",
        "Information Technology",
        "Artificial Intelligence & Data Science",
        "Artificial Intelligence & Machine Learning",
        "Data Science"
    ],
    "Data Scientist": [
        "Data Science",
        "Artificial Intelligence & Data Science",
        "Computer Engineering"
    ],
    "Mechanical Engineer": [
        "Mechanical Engineering",
        "Mechatronics Engineering",
        "Production Engineering"
    ],
    "Civil Engineer": [
        "Civil Engineering"
    ],
    "Electrical Engineer": [
        "Electrical Engineering",
        "Electronics Engineering",
        "Electronics & Telecommunication Engineering"
    ]
}


def get_eligible_colleges_cet(
        career,
        cet_percentile,
        category_code,
        university_id=None,
        city=None,
        preferred_branch=None
):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # If user selected a specific branch, use only that branch
    # Otherwise, use the career-to-branches mapping
    if preferred_branch:
        branches = [preferred_branch]
    else:
        branches = CAREER_BRANCH_MAP.get(career, [])
    
    if not branches:
        cursor.close()
        conn.close()
        return []

    branch_placeholders = ",".join(["%s"] * len(branches))

    # Optimized query with better JOIN order and LIMIT
    # First filter by branch names to get branch_ids, then use those for faster lookups
    query = f"""
        SELECT
            c.college_name,
            u.university_name,
            c.city,
            b.branch_name,
            cb.category_code,
            MAX(cb.cutoff_percentile) as cutoff_percentile,
            MAX(cb.available_seats) as available_seats
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

    params = branches + [category_code, cet_percentile]

    # Optional university filter (only apply if value is provided and not empty)
    if university_id and str(university_id).strip():
        query += " AND c.university_id = %s"
        params.append(university_id)

    # Optional city filter (only apply if value is provided and not empty)
    if city and str(city).strip():
        query += " AND c.city = %s"
        params.append(city)

    # Group by College Name and Branch Name to remove duplicates caused by redundant Branch IDs
    query += " GROUP BY c.college_id, b.branch_name, cb.category_code"

    # Order by cutoff percentile descending and limit results to prevent overwhelming UI
    query += " ORDER BY MAX(cb.cutoff_percentile) DESC LIMIT 100"

    cursor.execute(query, params)
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results

def get_eligible_colleges_flat(
        exam_type,
        cutoff_percentile,
        city=None,
        preferred_branch=None
):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Query flat columns in colleges table
    query = """
        SELECT
            college_name,
            branch as branch_name,
            city,
            cutoff_percentile,
            'N/A' as available_seats
        FROM colleges
        WHERE
            exam = %s
            AND cutoff_percentile <= %s
    """
    params = [exam_type, cutoff_percentile]

    if city and str(city).strip():
        query += " AND city = %s"
        params.append(city)

    if preferred_branch and str(preferred_branch).strip():
        query += " AND branch = %s"
        params.append(preferred_branch)

    query += " ORDER BY cutoff_percentile DESC LIMIT 50"

    cursor.execute(query, params)
    results = cursor.fetchall()
    
    # Process results to match format of centralized service if needed
    # (The frontend expects: college_name, branch_name, cutoff_percentile, city, available_seats)
    
    cursor.close()
    conn.close()
    return results
