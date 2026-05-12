import sys
sys.path.append('..')
from database.db import get_db_connection

conn = get_db_connection()
cursor = conn.cursor(dictionary=True)

# Check what NEET branches exist
cursor.execute("SELECT DISTINCT branch FROM colleges WHERE exam = 'NEET' ORDER BY branch")
branches = cursor.fetchall()
print("NEET branches in database:")
for b in branches:
    print(f"  {b['branch']}")

# Check BDS colleges
cursor.execute("SELECT college_name, city, cutoff_percentile FROM colleges WHERE exam = 'NEET' AND branch = 'BDS'")
bds_colleges = cursor.fetchall()
print(f"\nBDS colleges ({len(bds_colleges)}):")
for c in bds_colleges:
    print(f"  {c['college_name']} - {c['city']} - cutoff: {c['cutoff_percentile']}")

# Check Mumbai MBBS colleges
cursor.execute("SELECT college_name, branch, cutoff_percentile FROM colleges WHERE exam = 'NEET' AND city = 'Mumbai'")
mumbai_colleges = cursor.fetchall()
print(f"\nMumbai NEET colleges ({len(mumbai_colleges)}):")
for c in mumbai_colleges:
    print(f"  {c['college_name']} - {c['branch']} - cutoff: {c['cutoff_percentile']}")

# Check all NEET colleges count
cursor.execute("SELECT COUNT(*) as total FROM colleges WHERE exam = 'NEET'")
total = cursor.fetchone()
print(f"\nTotal NEET colleges in database: {total['total']}")

cursor.close()
conn.close()