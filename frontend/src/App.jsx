import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { isAuthenticated, getUserRole } from './utils/auth';
import Login from './pages/Login';
import Register from './pages/Register';
import AdminDashboard from './pages/AdminDashboard';
import OwnerDashboard from './pages/OwnerDashboard';
import TenantDashboard from './pages/TenantDashboard';
import EmployeeDashboard from './pages/EmployeeDashboard';

// Protected Route Component
const ProtectedRoute = ({ children, allowedRoles }) => {
    if (!isAuthenticated()) {
        return <Navigate to="/login" replace />;
    }

    const userRole = getUserRole();
    if (allowedRoles && !allowedRoles.includes(userRole)) {
        return <Navigate to="/unauthorized" replace />;
    }

    return children;
};

// Role-based Dashboard Redirect
const DashboardRedirect = () => {
    const role = getUserRole();

    switch (role) {
        case 'Admin':
            return <Navigate to="/admin" replace />;
        case 'Owner':
            return <Navigate to="/owner" replace />;
        case 'Tenant':
            return <Navigate to="/tenant" replace />;
        case 'Employee':
            return <Navigate to="/employee" replace />;
        default:
            return <Navigate to="/login" replace />;
    }
};

function App() {
    return (
        <Router>
            <Routes>
                {/* Public Routes */}
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />

                {/* Dashboard Redirect */}
                <Route path="/" element={<DashboardRedirect />} />

                {/* Protected Routes */}
                <Route
                    path="/admin"
                    element={
                        <ProtectedRoute allowedRoles={['Admin']}>
                            <AdminDashboard />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/owner"
                    element={
                        <ProtectedRoute allowedRoles={['Owner']}>
                            <OwnerDashboard />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/tenant"
                    element={
                        <ProtectedRoute allowedRoles={['Tenant']}>
                            <TenantDashboard />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/employee"
                    element={
                        <ProtectedRoute allowedRoles={['Employee']}>
                            <EmployeeDashboard />
                        </ProtectedRoute>
                    }
                />

                {/* Fallback */}
                <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
        </Router>
    );
}

export default App;
