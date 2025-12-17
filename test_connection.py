"""Test MySQL connection to find the correct password"""
import pymysql
import sys

# Test different password formats
passwords_to_test = [
    "Trideep@2003",           # Original
    "Trideep%402003",         # URL encoded (shouldn't work in pymysql)
    "",                       # Empty (if no password)
]

print("Testing MySQL connection with different password formats...\n")

for i, password in enumerate(passwords_to_test, 1):
    print(f"Test {i}: Password = '{password}'")
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password=password,
            port=3306
        )
        print(f"✓ SUCCESS! Password '{password}' works!\n")
        
        # Check databases
        cursor = conn.cursor()
        cursor.execute('SHOW DATABASES;')
        databases = cursor.fetchall()
        print(f"Found {len(databases)} databases:")
        for db in databases:
            print(f"  - {db[0]}")
        
        # Check if user_management exists
        db_exists = any('user_management' in str(db) for db in databases)
        if db_exists:
            print("\n✓ Database 'user_management' exists!")
        else:
            print("\n✗ Database 'user_management' NOT found - need to create it")
            print("Run in MySQL: CREATE DATABASE user_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        
        conn.close()
        sys.exit(0)
        
    except pymysql.err.OperationalError as e:
        print(f"✗ FAILED: {e}\n")
    except Exception as e:
        print(f"✗ ERROR: {e}\n")

print("=" * 60)
print("All password tests failed!")
print("\nPossible solutions:")
print("1. Reset MySQL root password")
print("2. Check if you're using a different MySQL user")
print("3. Run MySQL as administrator")
print("\nTo reset MySQL password, run this in MySQL:")
print("  ALTER USER 'root'@'localhost' IDENTIFIED BY 'Trideep@2003';")
print("  FLUSH PRIVILEGES;")
