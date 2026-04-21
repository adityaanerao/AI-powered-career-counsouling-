import sys
sys.path.append('.')
from database.db import get_db_connection

conn = get_db_connection()
cursor = conn.cursor(dictionary=True)

# Check college_branch_cutoffs table
cursor.execute("SHOW COLUMNS FROM college_branch_cutoffs")
cols = cursor.fetchall()
print("Columns in college_branch_cutoffs table:")
for col in cols:
    print(f"  {col['Field']} ({col['Type']})")

# Check if there are NEET entries
cursor.execute("""
    SELECT DISTINCT b.branch_name, cb.category_code, COUNT(*) as count
    FROM college_branch_cutoffs cb
    INNER JOIN branches b ON cb.branch_id = b.branch_id
    WHERE b.branch_name IN ('MBBS', 'BDS', 'BAMS', 'BHMS', 'BUMS', 'BPT', 'BVSc', 'B.Pharm')
    GROUP BY b.branch_name, cb.category_code
    LIMIT 10
""")
neet_cutoffs = cursor.fetchall()
print(f"\nNEET-related cutoffs in college_branch_cutoffs:")
for row in neet_cutoffs:
    print(f"  {row['branch_name']} - {row['category_code']}: {row['count']} records")

# Check total count
cursor.execute("""
    SELECT COUNT(*) as total FROM college_branch_cutoffs cb
    INNER JOIN branches b ON cb.branch_id = b.branch_id
    WHERE b.branch_name IN ('MBBS', 'BDS', 'BAMS', 'BHMS', 'BUMS', 'BPT', 'BVSc', 'B.Pharm')
""")
total = cursor.fetchone()
print(f"\nTotal NEET cutoff records: {total['total']}")

cursor.close()
conn.close()