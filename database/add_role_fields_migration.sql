-- Migration Script: Add Role-Specific Fields to Users Table
-- Run this to add columns for storing role-specific registration data

USE apartment_management;

-- Add new columns for role-specific information
ALTER TABLE users 
ADD COLUMN room_no VARCHAR(10) NULL COMMENT 'For Tenants - Room Number',
ADD COLUMN apartment_name VARCHAR(100) NULL COMMENT 'For Owners - Apartment Name',
ADD COLUMN apartment_no VARCHAR(10) NULL COMMENT 'For Owners - Apartment Number',
ADD COLUMN department VARCHAR(100) NULL COMMENT 'For Employees - Department';

-- Add indexes for better query performance
CREATE INDEX idx_room_no ON users(room_no);
CREATE INDEX idx_apartment_no ON users(apartment_no);
CREATE INDEX idx_department ON users(department);

-- Display success message
SELECT 'Migration completed successfully! Role-specific fields added to users table.' AS Status;
