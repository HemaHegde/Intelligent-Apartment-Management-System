import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Password@123',  # Update if needed
    database='apartment_management'
)

cursor = conn.cursor()
cursor.execute("SELECT user_id, username, role, managed_building FROM users WHERE role = 'Owner' LIMIT 10")
owners = cursor.fetchall()

print("Owner users:")
for owner in owners:
    print(f"  ID: {owner[0]}, Username: {owner[1]}, Role: {owner[2]}, Building: {owner[3]}")

cursor.close()
conn.close()
