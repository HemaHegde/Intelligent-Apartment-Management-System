import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaUser, FaLock, FaEnvelope, FaBuilding, FaHome } from 'react-icons/fa';
import PasswordStrengthIndicator from '../components/PasswordStrengthIndicator';

const Register = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        fullName: '',
        email: '',
        username: '',
        password: '',
        confirmPassword: '',
        role: 'Tenant', // Default role
        // Role-specific fields
        roomNo: '',
        apartmentName: '',
        apartmentNo: '',
        department: '',
        managedBuilding: '', // For Owner role
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
        setError('');
    };

    const validatePassword = (password) => {
        const requirements = [
            { test: (pwd) => pwd.length >= 8, message: 'At least 8 characters' },
            { test: (pwd) => /[A-Z]/.test(pwd), message: 'One uppercase letter' },
            { test: (pwd) => /[0-9]/.test(pwd), message: 'One number' },
            { test: (pwd) => /[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]/.test(pwd), message: 'One special character' },
        ];

        const unmetRequirements = requirements.filter(req => !req.test(password));
        return unmetRequirements.length === 0;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setSuccess('');

        // Validation
        if (formData.password !== formData.confirmPassword) {
            setError('Passwords do not match');
            setLoading(false);
            return;
        }

        if (!validatePassword(formData.password)) {
            setError('Password does not meet security requirements');
            setLoading(false);
            return;
        }

        try {
            // Build request body based on role
            const requestBody = {
                username: formData.username,
                email: formData.email,
                password: formData.password,
                full_name: formData.fullName,
                role: formData.role,
            };

            // Add role-specific fields
            if (formData.role === 'Tenant') {
                requestBody.room_no = formData.roomNo;
                requestBody.apartment_name = formData.apartmentName;
            } else if (formData.role === 'Owner') {
                requestBody.apartment_name = formData.apartmentName;
                requestBody.apartment_no = formData.apartmentNo;
                requestBody.managed_building = formData.managedBuilding;
            } else if (formData.role === 'Employee') {
                requestBody.department = formData.department;
            }
            // Admin doesn't need additional fields

            const response = await fetch('http://localhost:5000/api/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody),
            });

            const data = await response.json();

            if (response.ok) {
                setSuccess('Account created successfully! Redirecting to login...');
                setTimeout(() => {
                    navigate('/');
                }, 2000);
            } else {
                setError(data.message || 'Registration failed. Please try again.');
            }
        } catch (err) {
            setError('Network error. Please check your connection and try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center p-4 py-8">
            {/* Background gradient */}
            <div className="absolute inset-0 bg-gradient-to-br from-primary-600 via-secondary-600 to-primary-800"></div>

            {/* RV Logo in top-right corner */}
            <div className="absolute top-8 right-8 z-10 animate-fade-in">
                <div className="glass rounded-2xl p-3 backdrop-blur-xl hover:scale-110 transition-transform duration-300">
                    <img
                        src="/RV LOGO.jpg"
                        alt="RV Logo"
                        className="w-16 h-16 object-contain opacity-90"
                    />
                </div>
            </div>

            {/* Animated background shapes */}
            <div className="absolute inset-0 overflow-hidden">
                <div className="absolute -top-40 -right-40 w-80 h-80 bg-white opacity-10 rounded-full blur-3xl animate-pulse"></div>
                <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-white opacity-10 rounded-full blur-3xl animate-pulse delay-1000"></div>
            </div>

            {/* Registration Card */}
            <div className="relative w-full max-w-sm animate-fade-in my-2">
                {/* Logo/Title Section */}
                <div className="text-center mb-3">
                    <div className="inline-flex items-center justify-center w-14 h-14 bg-white rounded-full shadow-2xl mb-2">
                        <FaBuilding className="text-2xl text-primary-600" />
                    </div>
                    <h1 className="text-2xl font-bold text-white mb-1">
                        Create Account
                    </h1>
                    <p className="text-white/80 text-sm">
                        Join our community
                    </p>
                </div>

                {/* Registration Form Card */}
                <div className="glass rounded-xl shadow-2xl p-4 backdrop-blur-xl max-h-[65vh] overflow-y-auto scrollbar-thin scrollbar-thumb-white/20 scrollbar-track-transparent">
                    <h2 className="text-lg font-bold text-white mb-3 text-center">
                        Register as {formData.role}
                    </h2>

                    {error && (
                        <div className="mb-4 p-3 bg-red-500/20 border border-red-500/50 rounded-lg text-white text-sm animate-slide-up">
                            {error}
                        </div>
                    )}

                    {success && (
                        <div className="mb-4 p-3 bg-green-500/20 border border-green-500/50 rounded-lg text-white text-sm animate-slide-up">
                            {success}
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-2.5">
                        {/* Role Selection */}
                        <div>
                            <label className="block text-white/90 text-sm font-medium mb-1.5">
                                Select Role
                            </label>
                            <div className="relative">
                                <select
                                    name="role"
                                    value={formData.role}
                                    onChange={handleChange}
                                    className="w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all appearance-none cursor-pointer"
                                    required
                                >
                                    <option value="Tenant" className="bg-primary-700 text-white">Tenant</option>
                                    <option value="Owner" className="bg-primary-700 text-white">Owner</option>
                                    <option value="Employee" className="bg-primary-700 text-white">Employee</option>
                                    <option value="Admin" className="bg-primary-700 text-white">Admin</option>
                                </select>
                                <div className="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none">
                                    <svg className="w-5 h-5 text-white/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                                    </svg>
                                </div>
                            </div>
                        </div>

                        {/* Full Name */}
                        <div>
                            <label className="block text-white/90 text-sm font-medium mb-1.5">
                                Full Name
                            </label>
                            <div className="relative">
                                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                    <FaUser className="text-white/50" />
                                </div>
                                <input
                                    type="text"
                                    name="fullName"
                                    value={formData.fullName}
                                    onChange={handleChange}
                                    className="w-full pl-10 pr-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all"
                                    placeholder="Enter your full name"
                                    required
                                />
                            </div>
                        </div>

                        {/* Email */}
                        <div>
                            <label className="block text-white/90 text-sm font-medium mb-1.5">
                                Email
                            </label>
                            <div className="relative">
                                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                    <FaEnvelope className="text-white/50" />
                                </div>
                                <input
                                    type="email"
                                    name="email"
                                    value={formData.email}
                                    onChange={handleChange}
                                    className="w-full pl-10 pr-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all"
                                    placeholder="Enter your email"
                                    required
                                />
                            </div>
                        </div>

                        {/* Username */}
                        <div>
                            <label className="block text-white/90 text-sm font-medium mb-1.5">
                                Username
                            </label>
                            <div className="relative">
                                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                    <FaUser className="text-white/50" />
                                </div>
                                <input
                                    type="text"
                                    name="username"
                                    value={formData.username}
                                    onChange={handleChange}
                                    className="w-full pl-10 pr-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all"
                                    placeholder="Choose a username"
                                    required
                                />
                            </div>
                        </div>

                        {/* Role-Specific Fields */}
                        {formData.role === 'Tenant' && (
                            <>
                                <div>
                                    <label className="block text-white/90 text-sm font-medium mb-1.5">
                                        Apartment Name
                                    </label>
                                    <div className="relative">
                                        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                            <FaBuilding className="text-white/50" />
                                        </div>
                                        <input
                                            type="text"
                                            name="apartmentName"
                                            value={formData.apartmentName}
                                            onChange={handleChange}
                                            className="w-full pl-10 pr-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all"
                                            placeholder="e.g., Sunrise Apartments"
                                            required
                                        />
                                    </div>
                                </div>
                                <div>
                                    <label className="block text-white/90 text-sm font-medium mb-1.5">
                                        Room Number
                                    </label>
                                    <div className="relative">
                                        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                            <FaHome className="text-white/50" />
                                        </div>
                                        <input
                                            type="text"
                                            name="roomNo"
                                            value={formData.roomNo}
                                            onChange={handleChange}
                                            className="w-full pl-10 pr-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all"
                                            placeholder="e.g., 101, 202"
                                            required
                                        />
                                    </div>
                                </div>
                            </>
                        )}

                        {formData.role === 'Owner' && (
                            <>
                                <div>
                                    <label className="block text-white/90 text-sm font-medium mb-1.5">
                                        Managed Building
                                    </label>
                                    <div className="relative">
                                        <select
                                            name="managedBuilding"
                                            value={formData.managedBuilding}
                                            onChange={handleChange}
                                            className="w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all appearance-none cursor-pointer"
                                            required
                                        >
                                            <option value="" className="bg-primary-700 text-white">Select Building</option>
                                            <option value="B1" className="bg-primary-700 text-white">B1 - Maple Heights</option>
                                            <option value="B2" className="bg-primary-700 text-white">B2 - Harmony Residency</option>
                                            <option value="B3" className="bg-primary-700 text-white">B3 - Sunrise Enclave</option>
                                            <option value="B4" className="bg-primary-700 text-white">B4 - Lakeview Towers</option>
                                            <option value="B5" className="bg-primary-700 text-white">B5 - Green Meadows</option>
                                            <option value="B6" className="bg-primary-700 text-white">B6 - Silver Oaks</option>
                                            <option value="B7" className="bg-primary-700 text-white">B7 - Crystal View</option>
                                            <option value="B8" className="bg-primary-700 text-white">B8 - Riverside Park</option>
                                        </select>
                                        <div className="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none">
                                            <svg className="w-5 h-5 text-white/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                                            </svg>
                                        </div>
                                    </div>
                                </div>
                                <div>
                                    <label className="block text-white/90 text-sm font-medium mb-1.5">
                                        Apartment Name
                                    </label>
                                    <div className="relative">
                                        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                            <FaBuilding className="text-white/50" />
                                        </div>
                                        <input
                                            type="text"
                                            name="apartmentName"
                                            value={formData.apartmentName}
                                            onChange={handleChange}
                                            className="w-full pl-10 pr-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all"
                                            placeholder="e.g., Sunrise Apartments"
                                            required
                                        />
                                    </div>
                                </div>
                                <div>
                                    <label className="block text-white/90 text-sm font-medium mb-1.5">
                                        Apartment Number
                                    </label>
                                    <div className="relative">
                                        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                            <FaHome className="text-white/50" />
                                        </div>
                                        <input
                                            type="text"
                                            name="apartmentNo"
                                            value={formData.apartmentNo}
                                            onChange={handleChange}
                                            className="w-full pl-10 pr-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all"
                                            placeholder="e.g., 101, A-202"
                                            required
                                        />
                                    </div>
                                </div>
                            </>
                        )}

                        {formData.role === 'Employee' && (
                            <div>
                                <label className="block text-white/90 text-sm font-medium mb-1.5">
                                    Department
                                </label>
                                <div className="relative">
                                    <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                        <FaBuilding className="text-white/50" />
                                    </div>
                                    <input
                                        type="text"
                                        name="department"
                                        value={formData.department}
                                        onChange={handleChange}
                                        className="w-full pl-10 pr-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all"
                                        placeholder="e.g., Maintenance, Security"
                                        required
                                    />
                                </div>
                            </div>
                        )}

                        {/* Admin doesn't need additional fields */}

                        {/* Password */}
                        <div>
                            <label className="block text-white/90 text-sm font-medium mb-1.5">
                                Password
                            </label>
                            <div className="relative">
                                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                    <FaLock className="text-white/50" />
                                </div>
                                <input
                                    type="password"
                                    name="password"
                                    value={formData.password}
                                    onChange={handleChange}
                                    className="w-full pl-10 pr-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all"
                                    placeholder="Create a strong password"
                                    required
                                />
                            </div>
                            <PasswordStrengthIndicator password={formData.password} />
                        </div>

                        {/* Confirm Password */}
                        <div>
                            <label className="block text-white/90 text-sm font-medium mb-1.5">
                                Confirm Password
                            </label>
                            <div className="relative">
                                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                    <FaLock className="text-white/50" />
                                </div>
                                <input
                                    type="password"
                                    name="confirmPassword"
                                    value={formData.confirmPassword}
                                    onChange={handleChange}
                                    className="w-full pl-10 pr-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all"
                                    placeholder="Confirm your password"
                                    required
                                />
                            </div>
                            {formData.confirmPassword && formData.password !== formData.confirmPassword && (
                                <p className="mt-2 text-red-400 text-xs">Passwords do not match</p>
                            )}
                        </div>

                        {/* Submit Button */}
                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full py-2 px-4 bg-white text-primary-700 font-semibold rounded-lg shadow-lg hover:shadow-xl hover:scale-105 focus:outline-none focus:ring-2 focus:ring-white/50 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
                        >
                            {loading ? (
                                <span className="flex items-center justify-center">
                                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-primary-700" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                    Creating Account...
                                </span>
                            ) : (
                                'Create Account'
                            )}
                        </button>
                    </form>

                    {/* Back to Login Link */}
                    <div className="mt-4 text-center">
                        <p className="text-white/70 text-sm">
                            Already have an account?{' '}
                            <a
                                href="/"
                                className="text-white font-semibold hover:underline transition-all"
                            >
                                Sign In
                            </a>
                        </p>
                    </div>
                </div>

                {/* Footer */}
                <p className="text-center text-white/60 text-xs mt-6">
                    © 2025 Apartment Management System. All rights reserved.
                </p>
            </div>
        </div>
    );
};

export default Register;
