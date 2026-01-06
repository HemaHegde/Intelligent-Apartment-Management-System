-- Run this in MySQL Workbench to verify the column exists
USE apartment_management;

-- Check if column exists
SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'apartment_management'
  AND TABLE_NAME = 'users'
  AND COLUMN_NAME = 'managed_building';

-- If no results, the column doesn't exist
-- If you see a row, the column exists

-- Also show all columns
SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'apartment_management'
  AND TABLE_NAME = 'users'
ORDER BY ORDINAL_POSITION;
