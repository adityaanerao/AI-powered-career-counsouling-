-- =====================================================
-- QUICK PERFORMANCE FIX - RUN THIS IN MySQL WORKBENCH
-- =====================================================
-- Copy and paste this entire file into MySQL Workbench and execute it
-- This will dramatically speed up college filtering queries
-- =====================================================

USE career_guidance_db;

-- Index 1: Speed up branch name lookups
CREATE INDEX IF NOT EXISTS idx_branches_name 
ON branches(branch_name);

-- Index 2: Main composite index for cutoffs table (MOST IMPORTANT)
CREATE INDEX IF NOT EXISTS idx_cutoffs_branch_category_percentile 
ON college_branch_cutoffs(branch_id, category_code, cutoff_percentile, available_seats);

-- Index 3: University filter optimization
CREATE INDEX IF NOT EXISTS idx_colleges_university 
ON colleges(university_id);

-- Index 4: City filter optimization
CREATE INDEX IF NOT EXISTS idx_colleges_city 
ON colleges(city);

-- Index 5: Combined university + city filter
CREATE INDEX IF NOT EXISTS idx_colleges_university_city 
ON colleges(university_id, city);

-- Index 6: College ID for JOIN operations
CREATE INDEX IF NOT EXISTS idx_cutoffs_college 
ON college_branch_cutoffs(college_id);

-- =====================================================
-- Verify indexes were created
-- =====================================================
SHOW INDEX FROM branches WHERE Key_name LIKE 'idx_%';
SHOW INDEX FROM college_branch_cutoffs WHERE Key_name LIKE 'idx_%';
SHOW INDEX FROM colleges WHERE Key_name LIKE 'idx_%';

-- =====================================================
-- SUCCESS! Your queries should now be 10-100x faster!
-- =====================================================
