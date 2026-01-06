# Apartment Management System

A comprehensive full-stack web application for managing apartment complexes with AI-powered complaint prioritization and payment risk prediction.

## Features

### 🤖 AI/ML Capabilities
- **Complaint Priority Classification**: Automatically categorizes complaints (High/Medium/Low) using NLP
- **Payment Delay Prediction**: Predicts tenant payment risks using machine learning models

### 👥 Role-Based Dashboards
- **Admin**: Complete system oversight, user management, analytics, and building assignments
- **Owner**: Building-specific management, complaint tracking, and revenue monitoring
- **Tenant**: Submit complaints, view payment history, and track apartment details
- **Employee**: Manage assigned complaints and track resolution status

### 📊 Analytics & Insights
- Real-time payment analytics with defaulter tracking
- Complaint trend visualization
- Building-wise revenue and occupancy statistics
- Employee performance metrics

## Tech Stack

**Frontend:**
- React.js with Tailwind CSS
- Recharts for data visualization
- Axios for API communication

**Backend:**
- Flask (Python)
- JWT authentication
- RESTful API architecture

**Databases:**
- MySQL: User authentication and management
- MongoDB: Complaints, payments, and ML prediction logs

**Machine Learning:**
- Scikit-learn for model training
- NLP-based text classification
- Payment risk prediction models

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- MySQL Server
- MongoDB Server

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Database Configuration
1. Create MySQL database: `apartment_management`
2. Update `.env` file with your database credentials
3. Run data seeding scripts in `database/` folder

## Default Credentials

**Admin:**
- Username: `admin`
- Password: `Admin@123`

## Project Structure
```
├── backend/           # Flask API server
├── frontend/          # React application
├── ml_models/         # Trained ML models
├── database/          # Database schemas and seed scripts
└── README.md
```

## License
MIT License
