from database.db import get_db_connection

# Medical Career to Branch Mapping for NEET
NEET_CAREER_BRANCH_MAP = {
    "Doctor": [
        "MBBS"
    ],
    "Dentist": [
        "BDS"
    ],
    "Ayurvedic Doctor": [
        "BAMS"
    ],
    "Homeopathic Doctor": [
        "BHMS"
    ],
    "Unani Medicine Doctor": [
        "BUMS"
    ],
    "Physiotherapist": [
        "BPT",
        "Bachelor of Physiotherapy"
    ],
    "Veterinary Doctor": [
        "BVSc",
        "Bachelor of Veterinary Science"
    ],
    "Nurse": [
        "B.Sc Nursing",
        "BSc Nursing"
    ],
    "Pharmacist": [
        "B.Pharm",
        "Bachelor of Pharmacy"
    ]
}


def get_eligible_colleges_neet(
        career,
        neet_percentile,
        category_code,
        university_id=None,
        city=None,
        preferred_branch=None
):
    """
    Get eligible medical colleges based on NEET percentile and filters.
    
    Args:
        career: Medical career name (e.g., "Doctor", "Dentist")
        neet_percentile: NEET percentile score (0-100)
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
        branches = NEET_CAREER_BRANCH_MAP.get(career, [])
    
    if not branches:
        cursor.close()
        conn.close()
        return []

    branch_placeholders = ",".join(["%s"] * len(branches))

    # Optimized query with better JOIN order and LIMIT
    # Same structure as CET query for consistency
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

    params = branches + [category_code, neet_percentile]

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
