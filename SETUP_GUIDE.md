# Quick Start Guide

## Step-by-Step Setup

### 1. Start Databases

```powershell
# Start MySQL (Windows Service)
net start MySQL80

# Start MongoDB (Windows Service)
net start MongoDB
```

### 2. Initialize Databases

```powershell
# MySQL
cd "c:\Users\hemah\Desktop\APARTMENT SYSTEM\database"
mysql -u root -p < mysql_schema.sql
python seed_users.py

# MongoDB
python mongodb_init.py
```

### 3. Train ML Models

```powershell
cd "c:\Users\hemah\Desktop\APARTMENT SYSTEM\ml_models"
pip install -r requirements.txt
python train_complaint_classifier.py
python train_payment_predictor.py
```

### 4. Start Backend

```powershell
cd "c:\Users\hemah\Desktop\APARTMENT SYSTEM\backend"
pip install -r requirements.txt
python app.py
```

Keep this terminal open. Backend runs on `http://localhost:5000`

### 5. Start Frontend (New Terminal)

```powershell
cd "c:\Users\hemah\Desktop\APARTMENT SYSTEM\frontend"
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`

### 6. Login

Open browser: `http://localhost:5173`

**Demo Accounts:**
- Admin: `admin` / `password123`
- Owner: `owner1` / `password123`
- Tenant: `tenant1` / `password123`
- Employee: `employee1` / `password123`

## Troubleshooting

### MySQL Connection Error
- Ensure MySQL is running: `net start MySQL80`
- Check credentials in `backend/config.py`
- Verify database exists: `mysql -u root -p -e "SHOW DATABASES;"`

### MongoDB Connection Error
- Ensure MongoDB is running: `net start MongoDB`
- Check connection string in `backend/config.py`

### ML Model Not Found
- Train models first: `cd ml_models && python train_complaint_classifier.py`
- Verify .pkl files exist in `ml_models/` directory

### Frontend Build Error
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Clear cache: `npm cache clean --force`

### Port Already in Use
- Backend (5000): Change port in `backend/app.py`
- Frontend (5173): Change port in `frontend/vite.config.js`

## Testing the System

1. **Login as Tenant** → Submit a complaint → See AI priority prediction
2. **Login as Employee** → View complaints → Update status
3. **Login as Admin** → Run batch ML prediction → View analytics
4. **Login as Owner** → View properties → Check revenue

## Production Deployment

### Environment Variables

Create `.env` file in `backend/`:

```env
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
MYSQL_HOST=your-mysql-host
MYSQL_USER=your-mysql-user
MYSQL_PASSWORD=your-mysql-password
MONGO_URI=your-mongodb-uri
```

### Build Frontend

```powershell
cd frontend
npm run build
```

Serve `dist/` folder with nginx or Apache.

### Deploy Backend

Use gunicorn for production:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Next Steps

- Customize ML models with your own data
- Add more dashboard features
- Implement email notifications
- Add file upload for complaint attachments
- Create mobile app using React Native
