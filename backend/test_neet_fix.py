import sys
sys.path.append('.')
from services.neet_eligibility_service import get_eligible_colleges_neet

print("Testing NEET service fix...")

# Test case 1: Doctor with MBBS, 99 percentile
print("\nTest 1: Doctor career, 99 percentile, OPEN category")
colleges1 = get_eligible_colleges_neet(
    career="Doctor",
    neet_percentile=99.0,
    category_code="OPEN",
    preferred_branch=None,
    city=None
)
print(f"Found {len(colleges1)} colleges")
for i, college in enumerate(colleges1[:3]):  # Show first 3
    print(f"  {i+1}. {college['college_name']} - {college['branch_name']} - cutoff: {college['cutoff_percentile']}")

# Test case 2: Dentist with BDS, 85 percentile
print("\nTest 2: Dentist career, 85 percentile, OBC category")
colleges2 = get_eligible_colleges_neet(
    career="Dentist",
    neet_percentile=85.0,
    category_code="OBC",
    preferred_branch=None,
    city=None
)
print(f"Found {len(colleges2)} colleges")
for i, college in enumerate(colleges2[:3]):
    print(f"  {i+1}. {college['college_name']} - {college['branch_name']} - cutoff: {college['cutoff_percentile']}")

# Test case 3: Specific branch MBBS, 95 percentile, city filter
print("\nTest 3: MBBS branch, 95 percentile, OPEN category, city='Mumbai'")
colleges3 = get_eligible_colleges_neet(
    career="Doctor",  # Will be overridden by preferred_branch
    neet_percentile=95.0,
    category_code="OPEN",
    preferred_branch="MBBS",
    city="Mumbai"
)
print(f"Found {len(colleges3)} colleges")
for i, college in enumerate(colleges3[:5]):
    print(f"  {i+1}. {college['college_name']} - {college['city']} - cutoff: {college['cutoff_percentile']}")

# Test case 4: SC category with adjustment
print("\nTest 4: Doctor career, 88 percentile, SC category (should have -10 adjustment)")
colleges4 = get_eligible_colleges_neet(
    career="Doctor",
    neet_percentile=88.0,
    category_code="SC",
    preferred_branch=None,
    city=None
)
print(f"Found {len(colleges4)} colleges")
if colleges4:
    print(f"  First college effective cutoff used: {colleges4[0].get('effective_cutoff_used')}")
    print(f"  Sample: {colleges4[0]['college_name']} - cutoff: {colleges4[0]['cutoff_percentile']}")

print("\nTest completed!")