# 🔍 How to Check Your Databases

## Check MySQL Data

### Option 1: Using Command Line

```cmd
# Login to MySQL
mysql -u root -p

# Enter your password when prompted

# Then run these commands:
USE apartment_management;

# See all tables
SHOW TABLES;

# Check users
SELECT user_id, username, email, role FROM users;

# Check if your demo users exist
SELECT * FROM users WHERE username IN ('admin', 'tenant1', 'owner1', 'employee1');

# Exit
EXIT;
```

### Option 2: Using MySQL Workbench (If Installed)

1. Open MySQL Workbench
2. Connect to `localhost:3306`
3. Enter root password
4. Click on `apartment_management` database
5. Browse tables

**Expected Data:**
- `users` table should have 4 demo users (admin, owner1, tenant1, employee1)

---

## Check MongoDB Data

### Option 1: Using mongosh (Command Line)

```cmd
# Start mongosh
mongosh

# Switch to your database
use apartment_management

# See all collections
show collections

# Check complaints
db.complaints.find().pretty()

# Count complaints
db.complaints.countDocuments()

# Check payments
db.payments.find().pretty()

# Count payments
db.payments.countDocuments()

# Check apartments
db.apartments.find().pretty()

# Exit
exit
```

### Option 2: Using MongoDB Compass (If Installed)

1. Open MongoDB Compass
2. Connect to `mongodb://localhost:27017`
3. Click on `apartment_management` database
4. Browse collections:
   - `complaints`
   - `payments`
   - `apartments`
   - `prediction_logs`

**Expected Data:**
- If you ran `mongodb_init.py`, you should see data from the CSV file
- `complaints` collection should have 300 records
- `payments` collection should have 300 records
- `apartments` collection should have apartment data

---

## Quick Check Commands

### Check if MongoDB has data:
```cmd
mongosh --eval "use apartment_management; db.complaints.countDocuments()"
```

**Expected:** A number (like 300 if you imported CSV data)

### Check if MySQL has users:
```cmd
mysql -u root -p -e "USE apartment_management; SELECT COUNT(*) FROM users;"
```

**Expected:** At least 4 (the demo users)

---

## If Databases Are Empty

### Reinitialize MySQL:
```cmd
cd "c:\Users\hemah\Desktop\APARTMENT SYSTEM\database"
mysql -u root -p < mysql_schema.sql
python seed_users.py
```

### Reinitialize MongoDB:
```cmd
cd "c:\Users\hemah\Desktop\APARTMENT SYSTEM\database"
python mongodb_init.py
```

This will import data from `apartment_management_dataset_300.csv`

---

## Verify Data After Import

### MySQL:
```sql
mysql -u root -p
USE apartment_management;
SELECT username, role FROM users;
```

Should show:
```
+----------+----------+
| username | role     |
+----------+----------+
| admin    | Admin    |
| owner1   | Owner    |
| tenant1  | Tenant   |
| employee1| Employee |
+----------+----------+
```

### MongoDB:
```javascript
mongosh
use apartment_management
db.complaints.countDocuments()  // Should be > 0
db.payments.countDocuments()    // Should be > 0
```

---

## Install Database GUI Tools (Optional)

### MySQL Workbench:
- Download: https://dev.mysql.com/downloads/workbench/
- Visual interface for MySQL

### MongoDB Compass:
- Download: https://www.mongodb.com/try/download/compass
- Visual interface for MongoDB

These make it easier to browse and query your data!
