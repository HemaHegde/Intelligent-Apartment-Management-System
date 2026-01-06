-- Migration: Add managed_building field for Owner role
-- This allows Owners to be assigned to specific buildings

USE apartment_management;

-- Add managed_building column to users table
ALTER TABLE users 
ADD COLUMN managed_building VARCHAR(10) NULL COMMENT 'Building code (B1-B8) for Owner role';

-- Add index for faster queries
CREATE INDEX idx_managed_building ON users(managed_building);

-- Update existing Owner users with random building assignments
-- This is a one-time migration for existing data
UPDATE users 
SET managed_building = CASE 
    WHEN user_id LIKE 'O%' THEN 
        CASE (CAST(SUBSTRING(user_id, 2) AS UNSIGNED) % 8)
            WHEN 0 THEN 'B1'
            WHEN 1 THEN 'B2'
            WHEN 2 THEN 'B3'
            WHEN 3 THEN 'B4'
            WHEN 4 THEN 'B5'
            WHEN 5 THEN 'B6'
            WHEN 6 THEN 'B7'
            WHEN 7 THEN 'B8'
        END
    ELSE NULL
END
WHERE role = 'Owner';

-- Verify the migration
SELECT user_id, username, role, managed_building 
FROM users 
WHERE role = 'Owner'
ORDER BY managed_building, user_id;
