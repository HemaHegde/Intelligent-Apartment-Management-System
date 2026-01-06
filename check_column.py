import mysql.connector

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='apartment_management'
    )
    
    cursor = conn.cursor()
    cursor.execute("SHOW COLUMNS FROM users LIKE 'managed_building'")
    result = cursor.fetchone()
    
    if result:
        print("✓ Column 'managed_building' EXISTS")
        print(f"  Details: {result}")
    else:
        print("✗ Column 'managed_building' NOT FOUND")
        print("\nAll columns in users table:")
        cursor.execute("DESCRIBE users")
        for col in cursor.fetchall():
            print(f"  - {col[0]}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
