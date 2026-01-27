-- =====================================================
-- NEET Sample Data for Demonstration
-- =====================================================
-- This file contains sample medical colleges and NEET cutoff data
-- Run this ONLY if you don't have NEET data in your database yet
-- =====================================================

USE career_guidance_db;

-- Step 1: Add Medical Branches (if they don't exist)
-- =====================================================
INSERT IGNORE INTO branches (branch_name) VALUES
('MBBS'),
('BDS'),
('BAMS'),
('BHMS'),
('BUMS'),
('BPT'),
('B.Sc Nursing'),
('B.Pharm'),
('BVSc');

-- Step 2: Add Sample Medical Colleges (if they don't exist)
-- =====================================================
-- Note: Adjust university_id values based on your existing universities table

INSERT IGNORE INTO colleges (college_name, university_id, city) VALUES
('Grant Medical College', 2, 'Mumbai'),
('Seth GS Medical College', 2, 'Mumbai'),
('BJ Medical College', 1, 'Pune'),
('Government Medical College Nagpur', 5, 'Nagpur'),
('Government Medical College Aurangabad', 3, 'Aurangabad'),
('Government Dental College Mumbai', 2, 'Mumbai'),
('Nair Hospital Dental College', 2, 'Mumbai'),
('Bharati Vidyapeeth Dental College', 1, 'Pune'),
('Tilak Ayurved Mahavidyalaya', 2, 'Mumbai'),
('DY Patil Ayurved College', 2, 'Mumbai');

-- Step 3: Add Sample NEET Cutoffs
-- =====================================================
-- This is SAMPLE DATA - Replace with actual NEET cutoff data

-- Get branch IDs
SET @mbbs_id = (SELECT branch_id FROM branches WHERE branch_name = 'MBBS' LIMIT 1);
SET @bds_id = (SELECT branch_id FROM branches WHERE branch_name = 'BDS' LIMIT 1);
SET @bams_id = (SELECT branch_id FROM branches WHERE branch_name = 'BAMS' LIMIT 1);

-- Grant Medical College - MBBS
INSERT IGNORE INTO college_branch_cutoffs 
(college_id, branch_id, category_code, cutoff_percentile, available_seats)
SELECT college_id, @mbbs_id, 'OPEN', 99.5, 150
FROM colleges WHERE college_name = 'Grant Medical College' LIMIT 1;

INSERT IGNORE INTO college_branch_cutoffs 
(college_id, branch_id, category_code, cutoff_percentile, available_seats)
SELECT college_id, @mbbs_id, 'OBC', 98.8, 50
FROM colleges WHERE college_name = 'Grant Medical College' LIMIT 1;

INSERT IGNORE INTO college_branch_cutoffs 
(college_id, branch_id, category_code, cutoff_percentile, available_seats)
SELECT college_id, @mbbs_id, 'SC', 96.5, 30
FROM colleges WHERE college_name = 'Grant Medical College' LIMIT 1;

-- Seth GS Medical College - MBBS
INSERT IGNORE INTO college_branch_cutoffs 
(college_id, branch_id, category_code, cutoff_percentile, available_seats)
SELECT college_id, @mbbs_id, 'OPEN', 99.3, 140
FROM colleges WHERE college_name = 'Seth GS Medical College' LIMIT 1;

INSERT IGNORE INTO college_branch_cutoffs 
(college_id, branch_id, category_code, cutoff_percentile, available_seats)
SELECT college_id, @mbbs_id, 'OBC', 98.5, 45
FROM colleges WHERE college_name = 'Seth GS Medical College' LIMIT 1;

-- BJ Medical College Pune - MBBS
INSERT IGNORE INTO college_branch_cutoffs 
(college_id, branch_id, category_code, cutoff_percentile, available_seats)
SELECT college_id, @mbbs_id, 'OPEN', 99.0, 160
FROM colleges WHERE college_name = 'BJ Medical College' LIMIT 1;

INSERT IGNORE INTO college_branch_cutoffs 
(college_id, branch_id, category_code, cutoff_percentile, available_seats)
SELECT college_id, @mbbs_id, 'OBC', 98.2, 55
FROM colleges WHERE college_name = 'BJ Medical College' LIMIT 1;

-- Government Medical College Nagpur - MBBS
INSERT IGNORE INTO college_branch_cutoffs 
(college_id, branch_id, category_code, cutoff_percentile, available_seats)
SELECT college_id, @mbbs_id, 'OPEN', 97.5, 120
FROM colleges WHERE college_name = 'Government Medical College Nagpur' LIMIT 1;

INSERT IGNORE INTO college_branch_cutoffs 
(college_id, branch_id, category_code, cutoff_percentile, available_seats)
SELECT college_id, @mbbs_id, 'OBC', 96.0, 40
FROM colleges WHERE college_name = 'Government Medical College Nagpur' LIMIT 1;

-- Government Dental College Mumbai - BDS
INSERT IGNORE INTO college_branch_cutoffs 
(college_id, branch_id, category_code, cutoff_percentile, available_seats)
SELECT college_id, @bds_id, 'OPEN', 96.5, 80
FROM colleges WHERE college_name = 'Government Dental College Mumbai' LIMIT 1;

INSERT IGNORE INTO college_branch_cutoffs 
(college_id, branch_id, category_code, cutoff_percentile, available_seats)
SELECT college_id, @bds_id, 'OBC', 94.8, 30
FROM colleges WHERE college_name = 'Government Dental College Mumbai' LIMIT 1;

-- Nair Hospital Dental College - BDS
INSERT IGNORE INTO college_branch_cutoffs 
(college_id, branch_id, category_code, cutoff_percentile, available_seats)
SELECT college_id, @bds_id, 'OPEN', 95.2, 60
FROM colleges WHERE college_name = 'Nair Hospital Dental College' LIMIT 1;

-- Tilak Ayurved Mahavidyalaya - BAMS
INSERT IGNORE INTO college_branch_cutoffs 
(college_id, branch_id, category_code, cutoff_percentile, available_seats)
SELECT college_id, @bams_id, 'OPEN', 92.0, 100
FROM colleges WHERE college_name = 'Tilak Ayurved Mahavidyalaya' LIMIT 1;

INSERT IGNORE INTO college_branch_cutoffs 
(college_id, branch_id, category_code, cutoff_percentile, available_seats)
SELECT college_id, @bams_id, 'OBC', 89.5, 35
FROM colleges WHERE college_name = 'Tilak Ayurved Mahavidyalaya' LIMIT 1;

-- =====================================================
-- Verify Data Was Inserted
-- =====================================================
SELECT 'Medical Branches Added:' as Info;
SELECT * FROM branches WHERE branch_name IN ('MBBS', 'BDS', 'BAMS', 'BHMS', 'BUMS');

SELECT 'Medical Colleges Added:' as Info;
SELECT college_name, city FROM colleges WHERE college_name LIKE '%Medical%' OR college_name LIKE '%Dental%' OR college_name LIKE '%Ayurved%';

SELECT 'NEET Cutoffs Added:' as Info;
SELECT 
    c.college_name,
    b.branch_name,
    cb.category_code,
    cb.cutoff_percentile,
    cb.available_seats
FROM college_branch_cutoffs cb
JOIN colleges c ON cb.college_id = c.college_id
JOIN branches b ON cb.branch_id = b.branch_id
WHERE b.branch_name IN ('MBBS', 'BDS', 'BAMS')
ORDER BY b.branch_name, cb.cutoff_percentile DESC;

-- =====================================================
-- SUCCESS! NEET sample data has been added
-- =====================================================
