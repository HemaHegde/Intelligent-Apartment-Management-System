/**
 * API Utility Functions
 * Axios instance and API endpoint functions
 */

import axios from 'axios';
import { getToken, removeToken } from './auth';

// Create axios instance
const api = axios.create({
    baseURL: 'http://localhost:5000/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add JWT token
api.interceptors.request.use(
    (config) => {
        const token = getToken();
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor for error handling
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Token expired or invalid
            removeToken();
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

// Auth endpoints
export const login = (credentials) => api.post('/auth/login', credentials);
export const verifyToken = () => api.get('/auth/verify');
export const logout = () => api.post('/auth/logout');
export const getEmployees = () => api.get('/auth/employees');

// Apartment endpoints
export const getApartments = (params) => api.get('/apartments', { params });
export const getApartmentSummary = () => api.get('/apartments/summary');
export const getApartmentDetails = (roomNo) => api.get(`/apartments/${roomNo}`);

// Complaint endpoints
export const getComplaints = (params) => api.get('/complaints', { params });
export const createComplaint = (data) => api.post('/complaints', data);
export const updateComplaint = (id, data) => api.put(`/complaints/${id}`, data);
export const getComplaintTrends = () => api.get('/complaints/trends');

// Payment endpoints
export const getPayments = (params) => api.get('/payments', { params });
export const getPaymentRiskAlerts = (threshold) => api.get('/payments/risk-alerts', { params: { threshold } });
export const getPaymentTrends = () => api.get('/payments/trends');
export const getTenantPayments = (tenantId) => api.get(`/payments/tenant/${tenantId}`);

// ML Prediction endpoints
export const predictComplaintPriority = (complaintText) =>
    api.post('/predict-complaint-priority', { complaint_text: complaintText });

export const predictPaymentDelay = (features) =>
    api.post('/predict-payment-delay', features);

export const batchPredictComplaints = () =>
    api.post('/batch-predict-complaints');

export const getPredictionLogs = (params) =>
    api.get('/prediction-logs', { params });

// Admin Dashboard endpoints
export const getUsers = () => api.get('/auth/users');
export const updateUser = (userId, data) => api.put(`/auth/users/${userId}`, data);
export const deleteUser = (userId) => api.delete(`/auth/users/${userId}`);

export const getBuildingsSummary = () => api.get('/apartments/buildings/summary');
export const getEmployeePerformance = () => api.get('/analytics/employee-performance');
export const getPaymentAnalytics = () => api.get('/analytics/payment-analytics');

export default api;
