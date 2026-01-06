# 🏢 Apartment Management System - Complete Beginner Setup Guide

Welcome! This guide assumes this is your **first project** and will walk you through **everything** step-by-step.

---

## 📋 Table of Contents

1. [What You're Building](#what-youre-building)
2. [Prerequisites - What to Install](#prerequisites---what-to-install)
3. [Step-by-Step Setup](#step-by-step-setup)
4. [Running the Application](#running-the-application)
5. [Testing the System](#testing-the-system)
6. [Troubleshooting](#troubleshooting)

---

## 🎯 What You're Building

You're building a **complete Apartment Management System** with:

- **Frontend**: A beautiful web interface (React + Tailwind CSS)
- **Backend**: A server that handles requests (Flask/Python)
- **Databases**: 
  - MySQL (stores user accounts)
  - MongoDB (stores complaints and data)
- **AI/ML Models**: Smart predictions for complaints and payments

---

## 📦 Prerequisites - What to Install

### 1. **Python** (Programming Language for Backend & ML)

**What is it?** Python runs your backend server and AI models.

**How to Install:**
1. Go to: https://www.python.org/downloads/
2. Download **Python 3.10 or 3.11** (recommended)
3. **IMPORTANT**: During installation, check ✅ **"Add Python to PATH"**
4. Click "Install Now"

**Verify Installation:**
```powershell
python --version
```
You should see: `Python 3.10.x` or `Python 3.11.x`

---

### 2. **Node.js** (JavaScript Runtime for Frontend)

**What is it?** Node.js runs your React frontend and npm (package manager).

**How to Install:**
1. Go to: https://nodejs.org/
2. Download **LTS version** (e.g., 20.x)
3. Run installer with default settings

**Verify Installation:**
```powershell
node --version
npm --version
```
net startnet start mongod
```

**Start MySQL Service:**
```powershell
net start MySQL80
```
(You may need to run PowerShell as Administrator)

---

### 4. **MongoDB** (Database for Complaints & Data)

**What is it?** MongoDB stores complaint descriptions, attachments, and ML data.

**How to Install:**
1. Go to: https://www.mongodb.com/try/download/community
2. Download **MongoDB Community Server** for Windows
3. Run installer:
   - Choose **"Complete"** installation
   - Install as **Windows Service** (check this option)
   - Keep default port: **27017**

**Verify Installation:**
```powershell
mongod --version
```

**Start MongoDB Service:**
```powershell
net start MongoDB
```
(You may need to run PowerShell as Administrator)

---

### 5. **Git** (Version Control - Optional but Recommended)

**What is it?** Git helps manage code versions.

**How to Install:**
1. Go to: https://git-scm.com/download/win
2. Download and install with default settings

---

## 🚀 Step-by-Step Setup

### **STEP 1: Open PowerShell**

1. Press `Windows Key + X`
2. Select **"Windows PowerShell"** or **"Terminal"**
3. Navigate to your project folder:

```powershell
cd "c:\Users\hemah\Desktop\APARTMENT SYSTEM"
```

---

### **STEP 2: Start Database Services**

**Why?** Your application needs databases running to store data.

```powershell
# Start MySQL (you may need Administrator privileges)
net start MySQL80

# Start MongoDB
net start MongoDB
```

**Troubleshooting:**
- If you get "Access Denied", right-click PowerShell → "Run as Administrator"
- If service names are different, check Windows Services (Win + R → `services.msc`)

---

### **STEP 3: Initialize MySQL Database**

**Why?** This creates the database structure and adds demo users.

```powershell
# Navigate to database folder
cd "c:\Users\hemah\Desktop\APARTMENT SYSTEM\database"

# Create database schema
mysql -u root -p < mysql_schema.sql
```

**What happens:**
- You'll be prompted for your MySQL **root password** (the one you set during installation)
- This creates tables for users, apartments, etc.

**Next, add demo users:**

```powershell
# Install Python dependencies for this script
pip install mysql-connector-python

# Run the seed script
python seed_users.py
```

**What this does:** Adds demo accounts (admin, owner, tenant, employee)

---

### **STEP 4: Initialize MongoDB Database**

**Why?** This sets up MongoDB collections for complaints and data.

```powershell
# Still in the database folder
python mongodb_init.py
```

**What this does:** Creates MongoDB collections and indexes.

---

### **STEP 5: Train Machine Learning Models**

**Why?** The AI models need to be trained before they can make predictions.

```powershell
# Navigate to ML models folder
cd "c:\Users\hemah\Desktop\APARTMENT SYSTEM\ml_models"

# Install ML dependencies
pip install -r requirements.txt
```

**This will install:** scikit-learn, pandas, numpy, etc. (may take a few minutes)

**Train the models:**

```powershell
# Train complaint priority classifier
python train_complaint_classifier.py

# Train payment delay predictor
python train_payment_predictor.py
```

**What this does:** Creates `.pkl` files (trained models) that the backend will use.

**Expected output:** You'll see training progress and accuracy scores.

---

### **STEP 6: Start the Backend Server**

**Why?** The backend handles API requests from the frontend.

```powershell
# Navigate to backend folder
cd "c:\Users\hemah\Desktop\APARTMENT SYSTEM\backend"

# Install backend dependencies
pip install -r requirements.txt
```

**This installs:** Flask, PyJWT, pymongo, etc.

**Start the server:**

```powershell
python app.py
```

**Expected output:**
```
 * Running on http://127.0.0.1:5000
 * Running on http://localhost:5000
```

**⚠️ IMPORTANT: Keep this PowerShell window OPEN!** The backend is now running.

---

### **STEP 7: Start the Frontend (New Terminal)**

**Why?** The frontend is the web interface users interact with.

**Open a NEW PowerShell window** (don't close the backend one!)

```powershell
# Navigate to frontend folder
cd "c:\Users\hemah\Desktop\APARTMENT SYSTEM\frontend"

# Install frontend dependencies
npm install
```

**This installs:** React, Vite, Tailwind CSS, etc. (may take a few minutes)

**Start the development server:**

```powershell
npm run dev
```

**Expected output:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

**⚠️ IMPORTANT: Keep this PowerShell window OPEN too!**

---

## 🎉 Running the Application

### **Access the Application**

1. Open your web browser (Chrome, Edge, Firefox)
2. Go to: **http://localhost:5173**

You should see the **Login Page**!

---

### **Demo Accounts**

Try logging in with these accounts:

| Role | Username | Password |
|------|----------|----------|
| **Admin** | `admin` | `password123` |
| **Owner** | `owner1` | `password123` |
| **Tenant** | `tenant1` | `password123` |
| **Employee** | `employee1` | `password123` |

---

## 🧪 Testing the System

### **Test 1: Submit a Complaint (as Tenant)**

1. Login as **tenant1** / **password123**
2. Navigate to "Submit Complaint"
3. Enter a complaint description
4. Submit → See AI priority prediction!

### **Test 2: View Complaints (as Employee)**

1. Logout → Login as **employee1** / **password123**
2. View complaints submitted by tenants
3. Update complaint status

### **Test 3: Admin Dashboard**

1. Logout → Login as **admin** / **password123**
2. View analytics and system overview
3. Run batch ML predictions

---

## 🔧 Troubleshooting

### **Problem: "Python is not recognized"**

**Solution:** Python not added to PATH during installation.
1. Reinstall Python
2. Check ✅ "Add Python to PATH"

---

### **Problem: "npm is not recognized"**

**Solution:** Node.js not installed properly.
1. Reinstall Node.js from https://nodejs.org/

---

### **Problem: "Access denied" for MySQL**

**Solution:** Wrong password or user.
1. Reset MySQL root password:
   - Open MySQL Workbench
   - Or use: `mysql -u root -p`

---

### **Problem: "Port 5000 already in use"**

**Solution:** Another app is using port 5000.
1. Stop other apps
2. Or change port in `backend/app.py`:
   ```python
   app.run(debug=True, port=5001)  # Change to 5001
   ```

---

### **Problem: "Port 5173 already in use"**

**Solution:** Another app is using port 5173.
1. Stop other apps
2. Or change port in `frontend/vite.config.js`

---

### **Problem: Backend crashes with "Module not found"**

**Solution:** Missing Python packages.
```powershell
cd backend
pip install -r requirements.txt
```

---

### **Problem: Frontend shows blank page**

**Solution:** Check browser console (F12) for errors.
1. Ensure backend is running on `http://localhost:5000`
2. Check `frontend/src/config.js` for correct API URL

---

## 📝 Summary of Running Commands

**Every time you want to run the app:**

1. **Start databases** (if not already running):
   ```powershell
   net start MySQL80
   net start MongoDB
   ```

2. **Terminal 1 - Backend:**
   ```powershell
   cd "c:\Users\hemah\Desktop\APARTMENT SYSTEM\backend"
   python app.py
   ```

3. **Terminal 2 - Frontend:**
   ```powershell
   cd "c:\Users\hemah\Desktop\APARTMENT SYSTEM\frontend"
   npm run dev
   ```

4. **Open browser:** http://localhost:5173

---

## 🎓 Understanding the Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     YOUR BROWSER                        │
│              http://localhost:5173                      │
│                  (React Frontend)                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ API Requests
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  BACKEND SERVER                         │
│              http://localhost:5000                      │
│                  (Flask/Python)                         │
└───────┬─────────────────────────┬───────────────────────┘
        │                         │
        │                         │
        ▼                         ▼
┌───────────────┐         ┌──────────────────┐
│     MySQL     │         │     MongoDB      │
│  (Port 3306)  │         │   (Port 27017)   │
│               │         │                  │
│  - Users      │         │  - Complaints    │
│  - Roles      │         │  - ML Data       │
└───────────────┘         └──────────────────┘
```

---

## 🎯 Next Steps

Once everything is running:

1. **Explore the code** - Check `backend/app.py` and `frontend/src/`
2. **Customize** - Change colors, add features
3. **Learn** - Understand how React, Flask, and databases work together
4. **Deploy** - Host on cloud platforms (AWS, Heroku, Vercel)

---

## 💡 Tips for Beginners

- **Don't panic if you see errors** - Read them carefully, they usually tell you what's wrong
- **Google is your friend** - Search error messages
- **Keep terminals open** - Both backend and frontend need to run simultaneously
- **Use Ctrl+C** - To stop servers in PowerShell
- **Check ports** - Make sure 5000 and 5173 are free

---

## 📞 Need Help?

If you're stuck:
1. Check the error message carefully
2. Look in the Troubleshooting section above
3. Search the error on Google/Stack Overflow
4. Check if all services are running (MySQL, MongoDB, Backend, Frontend)

---

**Good luck! 🚀 You've got this!**
