# 🗄️ Quick Database Setup Guide

## What You Need First

Before running these commands, make sure:
1. ✅ MySQL is installed and running
2. ✅ MongoDB is installed and running
3. ✅ You know your MySQL root password

---

## Step 1: Create MySQL Database Schema

This creates the database structure (tables, columns, etc.)

```cmd
cd "c:\Users\hemah\Desktop\APARTMENT SYSTEM\database"
mysql -u root -p < mysql_schema.sql
```

**What happens:**
- You'll be prompted: `Enter password:`
- Type your MySQL root password (the one you set during MySQL installation)
- Press Enter
- If successful, you'll see no errors and return to the command prompt

**Troubleshooting:**
- ❌ `'mysql' is not recognized` → MySQL not in PATH, use full path: `"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p < mysql_schema.sql`
- ❌ `Access denied` → Wrong password, try again
- ❌ `Can't connect to MySQL server` → MySQL service not running, run: `net start MySQL80`

---

## Step 2: Add Demo Users to MySQL

This adds test accounts (admin, owner, tenant, employee)

```cmd
python seed_users.py
```

**What happens:**
- You'll be prompted: `Enter MySQL root password:`
- Type your MySQL root password
- Press Enter
- You'll see progress messages:
  ```
  [1/4] Enter MySQL root password:
  [2/4] Connecting to MySQL database...
  [3/4] Clearing existing demo users...
  [4/4] Inserting demo users...
  ✅ DEMO USERS CREATED SUCCESSFULLY!
  ```

**Troubleshooting:**
- ❌ `No module named 'mysql.connector'` → Run: `pip install mysql-connector-python bcrypt`
- ❌ `Access denied` → Wrong password
- ❌ `Unknown database 'apartment_management'` → Run Step 1 first

---

## Step 3: Initialize MongoDB

This creates MongoDB collections for complaints and data

```cmd
python mongodb_init.py
```

**What happens:**
- MongoDB collections are created
- Indexes are set up for fast queries
- You'll see success messages

**Troubleshooting:**
- ❌ `No module named 'pymongo'` → Run: `pip install pymongo`
- ❌ `Connection refused` → MongoDB service not running, run: `net start MongoDB`

---

## Verify Everything Worked

### Check MySQL:

```cmd
mysql -u root -p
```

Then type:
```sql
USE apartment_management;
SHOW TABLES;
SELECT username, role FROM users;
EXIT;
```

You should see 4 users: admin, owner1, tenant1, employee1

### Check MongoDB:

```cmd
mongosh
```

Then type:
```javascript
use apartment_management
show collections
exit
```

You should see collections like: complaints, ml_predictions, etc.

---

## Summary

Run these 3 commands in order:

```cmd
# 1. Create database structure
mysql -u root -p < mysql_schema.sql

# 2. Add demo users
python seed_users.py

# 3. Setup MongoDB
python mongodb_init.py
```

**Done! ✅** Your databases are now ready for the application.

---

## Next Steps

After database setup, continue with:
1. Training ML models (in `ml_models` folder)
2. Starting the backend server (in `backend` folder)
3. Starting the frontend (in `frontend` folder)

See `BEGINNER_SETUP_GUIDE.md` for complete instructions.
