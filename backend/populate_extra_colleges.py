import mysql.connector
from database.db import get_db_connection

def populate_extra_colleges():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Junior Colleges (11th & 12th) - Schema: college_name, branch, cutoff_percentile, city, exam
    # Note: 'state' is defaulted to 'Maharashtra'
    junior_colleges = [
        # Pune
        ("Fergusson College", "Science", 94.5, "Pune", "SSC"),
        ("Fergusson College", "Arts", 92.0, "Pune", "SSC"),
        ("BMCC Pune", "Commerce", 93.0, "Pune", "SSC"),
        ("Modern College", "Science", 85.0, "Pune", "SSC"),
        ("SP College", "Science", 88.5, "Pune", "SSC"),
        ("SP College", "Arts", 82.0, "Pune", "SSC"),
        # Mumbai
        ("St. Xaviers College", "Science", 92.0, "Mumbai", "SSC"),
        ("St. Xaviers College", "Arts", 94.0, "Mumbai", "SSC"),
        ("Jai Hind College", "Commerce", 90.0, "Mumbai", "SSC"),
        ("Mithibai College", "Science", 89.0, "Mumbai", "SSC"),
        ("Ruparel College", "Science", 86.0, "Mumbai", "SSC")
    ]

    # PG Colleges (MBA, M.Tech, MCA)
    pg_colleges = [
        # MBA (CAT/CET)
        ("IIM Mumbai", "MBA", 98.0, "Mumbai", "CAT"),
        ("JBIMS Mumbai", "MBA", 99.5, "Mumbai", "CET-PG"),
        ("Sydenham Mumbai", "MBA", 96.0, "Mumbai", "CET-PG"),
        ("PUMBA Pune", "MBA", 92.0, "Pune", "CET-PG"),
        ("Indira Institute", "MBA", 85.0, "Pune", "CET-PG"),
        
        # M.Tech (GATE)
        ("COEP Tech University", "M.Tech CSE", 50.0, "Pune", "GATE"), 
        ("VJTI Mumbai", "M.Tech CSE", 55.0, "Mumbai", "GATE"),
        ("SPIT Mumbai", "M.Tech CSE", 45.0, "Mumbai", "GATE"),
        
        # MCA (CET / MCA-CET)
        ("VJTI Mumbai", "MCA", 99.0, "Mumbai", "MCA-CET"),
        ("SPIT Mumbai", "MCA", 98.0, "Mumbai", "MCA-CET"),
        ("Pune University (PUCSD)", "MCA", 95.0, "Pune", "MCA-CET")
    ]

    print("Adding extra colleges...")
    # Schema: college_name, branch, exam, cutoff_percentile, min_12_percent, state, city, university_id
    sql = "INSERT INTO colleges (college_name, branch, cutoff_percentile, city, exam, state) VALUES (%s, %s, %s, %s, %s, 'Maharashtra')"
    
    try:
        cursor.executemany(sql, junior_colleges)
        cursor.executemany(sql, pg_colleges)
        conn.commit()
        print(f"Successfully added {len(junior_colleges) + len(pg_colleges)} new records.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    populate_extra_colleges()

