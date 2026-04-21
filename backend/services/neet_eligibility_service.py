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

# Category adjustment factors for NEET cutoffs (simplified)
# These values adjust the effective cutoff percentile needed for different categories
CATEGORY_ADJUSTMENT = {
    "OPEN": 0.0,    # No adjustment
    "EWS": -2.0,    # 2 percentile points easier
    "OBC": -5.0,    # 5 percentile points easier
    "SC": -10.0,    # 10 percentile points easier
    "ST": -15.0,    # 15 percentile points easier
    "PWD": -20.0,   # 20 percentile points easier for persons with disabilities
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

    # Apply category adjustment to percentile
    # If category is not in adjustment map, use OPEN as default
    adjustment = CATEGORY_ADJUSTMENT.get(category_code, 0.0)
    effective_percentile = neet_percentile - adjustment
    
    # Build query for colleges table (direct query, no joins needed for basic data)
    query = """
        SELECT 
            college_name,
            branch AS branch_name,
            cutoff_percentile,
            100 AS available_seats,  # Default value since not in table
            city,
            state,
            tier,
            college_type,
            fees_per_year,
            placement_percentage,
            average_package
        FROM colleges
        WHERE exam = 'NEET'
    """

    params = []

    # Filter by branch
    if branches:
        branch_placeholders = ",".join(["%s"] * len(branches))
        query += f" AND branch IN ({branch_placeholders})"
        params.extend(branches)

    # Filter by city
    if city and str(city).strip():
        query += " AND city = %s"
        params.append(city)

    # Filter by university_id
    if university_id and str(university_id).strip():
        query += " AND university_id = %s"
        params.append(university_id)

    # IMPORTANT: Cutoff filter (with margin)
    # Use effective percentile after category adjustment
    query += " AND cutoff_percentile <= %s"
    params.append(effective_percentile + 1)  # +1 margin as suggested

    # Order by best colleges (highest cutoff first)
    query += " ORDER BY cutoff_percentile DESC LIMIT 100"

    cursor.execute(query, params)
    results = cursor.fetchall()

    # Add category information to results
    for result in results:
        result["category_code"] = category_code
        result["effective_cutoff_used"] = effective_percentile

    cursor.close()
    conn.close()

    return results
