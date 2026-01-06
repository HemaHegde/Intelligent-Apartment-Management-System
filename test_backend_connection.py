# Test script to verify backend can see the managed_building column
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from models.mysql_models import get_mysql_connection

conn = get_mysql_connection()
cursor = conn.cursor()

# Check what columns the backend sees
cursor.execute("DESCRIBE users")
columns = cursor.fetchall()

print("Columns visible to backend:")
print("-" * 60)
for col in columns:
    print(f"{col[0]:20} {col[1]:20}")

# Check specifically for managed_building
has_managed_building = any(col[0] == 'managed_building' for col in columns)
print("\n" + "=" * 60)
if has_managed_building:
    print("✓ Backend CAN see managed_building column")
else:
    print("✗ Backend CANNOT see managed_building column")
    print("This is the problem!")

cursor.close()
conn.close()
