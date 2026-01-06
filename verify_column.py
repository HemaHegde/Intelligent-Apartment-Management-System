import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='apartment_management'
)

cursor = conn.cursor()
cursor.execute("DESCRIBE users")
columns = cursor.fetchall()

print("Users table columns:")
print("-" * 60)
for col in columns:
    print(f"{col[0]:20} {col[1]:20} {col[2]:10}")

# Check if managed_building exists
has_managed_building = any(col[0] == 'managed_building' for col in columns)
print("\n" + "=" * 60)
if has_managed_building:
    print("✓ SUCCESS: managed_building column exists!")
    print("You can now register as Tenant without errors.")
else:
    print("✗ ERROR: managed_building column not found!")

cursor.close()
conn.close()
