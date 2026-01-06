# 🚀 Starting the Frontend Server

## Quick Start

**Open a NEW Command Prompt window** and run these commands:

```cmd
cd "c:\Users\hemah\Desktop\APARTMENT SYSTEM\frontend"
npm run dev
```

**Expected Output:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

**⚠️ Keep this window open!** Don't close it or press Ctrl+C.

---

## If You Get Errors

### Error: "npm is not recognized"
**Fix:** Node.js not installed or not in PATH
```cmd
# Check if Node.js is installed
node --version

# If not found, download from: https://nodejs.org/
```

### Error: "Cannot find module"
**Fix:** Dependencies not installed
```cmd
cd "c:\Users\hemah\Desktop\APARTMENT SYSTEM\frontend"
npm install
npm run dev
```

### Error: "Port 5173 already in use"
**Fix:** Another process is using port 5173

**Option 1:** Kill the process using port 5173
```cmd
netstat -ano | findstr :5173
taskkill /PID <PID_NUMBER> /F
```

**Option 2:** Use a different port
Edit `vite.config.js` and change port to 5174:
```javascript
server: {
  port: 5174,  // Changed from 5173
  ...
}
```

Then access: `http://localhost:5174`

### Error: Server starts then crashes
**Fix:** Clear cache and restart
```cmd
# Delete node_modules and reinstall
cd "c:\Users\hemah\Desktop\APARTMENT SYSTEM\frontend"
rmdir /s /q node_modules
del package-lock.json
npm install
npm run dev
```

---

## Verify It's Running

1. **Check the terminal** - You should see "Local: http://localhost:5173/"
2. **Open browser** - Go to `http://localhost:5173`
3. **You should see** - The login page

---

## Login Credentials

Once the page loads, use:
- **Username:** `admin`
- **Password:** `password123`

Or try other roles:
- Owner: `owner1` / `password123`
- Tenant: `tenant1` / `password123`
- Employee: `employee1` / `password123`

---

## Both Servers Must Be Running

For the app to work, you need **TWO** Command Prompt windows:

| Window | Location | Command | Port |
|--------|----------|---------|------|
| **Terminal 1** | `backend/` | `python app.py` | 5000 |
| **Terminal 2** | `frontend/` | `npm run dev` | 5173 |

**Keep both open while using the app!**

---

## Stopping the Server

To stop the frontend server:
1. Go to the terminal running `npm run dev`
2. Press `Ctrl + C`
3. Confirm with `Y` if prompted

---

## Quick Checklist

Before starting frontend, make sure:
- ✅ Node.js is installed (`node --version`)
- ✅ Dependencies installed (`npm install` was run)
- ✅ Backend is running on port 5000
- ✅ MySQL service is running
- ✅ MongoDB service is running
- ✅ Database is initialized with demo users

---

**Ready? Run `npm run dev` now!** 🎉
