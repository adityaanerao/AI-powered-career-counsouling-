import sys
sys.path.append('..')
from database.db import get_db_connection

conn = get_db_connection()
cursor = conn.cursor(dictionary=True)

# Check columns in colleges table
cursor.execute("SHOW COLUMNS FROM colleges")
cols = cursor.fetchall()
print("Columns in colleges table:")
for col in cols:
    print(f"  {col['Field']} ({col['Type']})")

# Check if exam column exists
exam_exists = any(col['Field'] == 'exam' for col in cols)
print(f"\n'exam' column exists: {exam_exists}")

# Check sample NEET data
if exam_exists:
    cursor.execute("SELECT DISTINCT exam FROM colleges WHERE exam IS NOT NULL")
    exams = cursor.fetchall()
    print("\nDistinct exam values:")
    for exam in exams:
        print(f"  {exam['exam']}")
    
    cursor.execute("SELECT * FROM colleges WHERE exam = 'NEET' LIMIT 5")
    neet_colleges = cursor.fetchall()
    print(f"\nSample NEET colleges ({len(neet_colleges)} found):")
    for college in neet_colleges:
        print(f"  {college.get('college_name')} - {college.get('branch')} - cutoff: {college.get('cutoff_percentile')}")
else:
    # Check for cutoff_percentile column
    cutoff_exists = any(col['Field'] == 'cutoff_percentile' for col in cols)
    print(f"\n'cutoff_percentile' column exists: {cutoff_exists}")
    
    # Check all columns
    cursor.execute("SELECT * FROM colleges LIMIT 3")
    sample = cursor.fetchall()
    print("\nSample college rows:")
    for row in sample:
        print(row)

cursor.close()
conn.close()