-- =====================================================
-- Database Performance Optimization Script
-- This script adds indexes to improve college filtering performance
-- =====================================================

-- Index for branch_name lookups (used in WHERE IN clause)
CREATE INDEX IF NOT EXISTS idx_branches_name ON branches(branch_name);

-- Composite index for college_branch_cutoffs table
-- This is the main table being queried, so we need comprehensive indexing
CREATE INDEX IF NOT EXISTS idx_cutoffs_branch_category_percentile 
ON college_branch_cutoffs(branch_id, category_code, cutoff_percentile, available_seats);

-- Index for college filters (university and city)
CREATE INDEX IF NOT EXISTS idx_colleges_university ON colleges(university_id);
CREATE INDEX IF NOT EXISTS idx_colleges_city ON colleges(city);

-- Composite index for common college queries
CREATE INDEX IF NOT EXISTS idx_colleges_university_city ON colleges(university_id, city);

-- Index for college_id foreign key lookups
CREATE INDEX IF NOT EXISTS idx_cutoffs_college ON college_branch_cutoffs(college_id);

-- =====================================================
-- Query Optimization Notes:
-- =====================================================
-- 1. idx_branches_name: Speeds up the IN clause for branch names
-- 2. idx_cutoffs_branch_category_percentile: Composite index for the main WHERE conditions
-- 3. idx_colleges_university and idx_colleges_city: For optional filters
-- 4. idx_colleges_university_city: Composite for when both filters are used
-- 5. idx_cutoffs_college: For JOIN operations
--
-- Expected Performance Improvement: 10-100x faster queries depending on data size
-- =====================================================
