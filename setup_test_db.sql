-- SQL script to create test database and user
CREATE DATABASE IF NOT EXISTS test_user_management;
CREATE USER IF NOT EXISTS 'test'@'localhost' IDENTIFIED BY 'test';
GRANT ALL PRIVILEGES ON test_user_management.* TO 'test'@'localhost';
FLUSH PRIVILEGES;

-- Verify setup
SELECT user, host FROM mysql.user WHERE user = 'test';
SHOW DATABASES LIKE 'test_user_management';
