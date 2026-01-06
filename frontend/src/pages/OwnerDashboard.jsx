import { useState, useEffect } from 'react';
import { FaBuilding, FaUsers, FaDollarSign, FaExclamationTriangle } from 'react-icons/fa';
import Navbar from '../components/Navbar';
import SummaryCard from '../components/SummaryCard';
import PriorityTag from '../components/PriorityTag';
import PaymentTrendChart from '../components/PaymentTrendChart';
import { getApartmentSummary, getComplaints, getPayments, getEmployees, updateComplaint } from '../utils/api';

const OwnerDashboard = () => {
    const [summary, setSummary] = useState(null);
    const [complaints, setComplaints] = useState([]);
    const [payments, setPayments] = useState([]);
    const [employees, setEmployees] = useState([]);
    const [loading, setLoading] = useState(true);
    const [user, setUser] = useState(null);

    useEffect(() => {
        // Get user info from localStorage
        const userData = JSON.parse(localStorage.getItem('user'));
        setUser(userData);
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const [summaryRes, complaintsRes, paymentsRes, employeesRes] = await Promise.all([
                getApartmentSummary(),
                getComplaints({ limit: 10 }),
                getPayments({ limit: 10 }),
                getEmployees()
            ]);

            setSummary(summaryRes.data);
            setComplaints(complaintsRes.data.complaints);
            setPayments(paymentsRes.data.payments);
            setEmployees(employeesRes.data.employees);
        } catch (error) {
            console.error('Error fetching data:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleAssignEmployee = async (complaintId, employeeId) => {
        try {
            await updateComplaint(complaintId, { employee_id: employeeId });
            alert('Complaint assigned successfully!');
            fetchData(); // Refresh data
        } catch (error) {
            alert('Failed to assign complaint: ' + error.message);
        }
    };

    // Building name mapping
    const buildingNames = {
        'B1': 'Maple Heights',
        'B2': 'Harmony Residency',
        'B3': 'Sunrise Enclave',
        'B4': 'Lakeview Towers',
        'B5': 'Green Meadows',
        'B6': 'Silver Oaks',
        'B7': 'Crystal View',
        'B8': 'Riverside Park'
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-6">
                <div className="flex items-center justify-center h-screen">
                    <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-primary-600"></div>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-6">
            <div className="max-w-7xl mx-auto">
                <Navbar title="Owner Dashboard" />

                {/* Building Info Banner */}
                {user?.managed_building && (
                    <div className="bg-gradient-to-r from-primary-500 to-primary-600 rounded-xl shadow-lg p-6 mb-6 text-white">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm opacity-90">Managing Building</p>
                                <h2 className="text-3xl font-bold">{buildingNames[user.managed_building] || user.managed_building}</h2>
                                <p className="text-sm mt-1 opacity-90">Building Code: {user.managed_building}</p>
                            </div>
                            <FaBuilding className="text-6xl opacity-20" />
                        </div>
                    </div>
                )}

                {/* Summary Cards */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
                    <SummaryCard
                        icon={FaBuilding}
                        title="Apartments in Building"
                        value={summary?.total_apartments || 0}
                        color="primary"
                    />
                    <SummaryCard
                        icon={FaUsers}
                        title="Active Tenants"
                        value={summary?.total_apartments || 0}
                        color="info"
                    />
                    <SummaryCard
                        icon={FaDollarSign}
                        title="Building Revenue"
                        value={`₹${(summary?.total_revenue || 0).toLocaleString()}`}
                        color="success"
                    />
                    <SummaryCard
                        icon={FaExclamationTriangle}
                        title="Pending Complaints"
                        value={summary?.pending_complaints || 0}
                        color="warning"
                    />
                </div>

                {/* Payment Trends */}
                <div className="mb-6">
                    <PaymentTrendChart />
                </div>

                {/* Property Complaints */}
                <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
                    <h3 className="text-xl font-bold text-gray-800 mb-4">Property Complaints</h3>
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead>
                                <tr className="border-b border-gray-200">
                                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Room</th>
                                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Tenant</th>
                                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Issue</th>
                                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Priority</th>
                                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Status</th>
                                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Assign To</th>
                                </tr>
                            </thead>
                            <tbody>
                                {complaints.slice(0, 8).map((complaint) => (
                                    <tr key={complaint.complaint_id} className="border-b border-gray-100 hover:bg-gray-50">
                                        <td className="py-3 px-4 text-sm font-semibold">{complaint.room_no}</td>
                                        <td className="py-3 px-4 text-sm">{complaint.tenant_name}</td>
                                        <td className="py-3 px-4 text-sm">{complaint.complaint_text}</td>
                                        <td className="py-3 px-4"><PriorityTag priority={complaint.priority} /></td>
                                        <td className="py-3 px-4 text-sm">
                                            <span className={`px-2 py-1 rounded text-xs ${complaint.complaint_status === 'Resolved' ? 'bg-green-100 text-green-700' :
                                                complaint.complaint_status === 'In Progress' ? 'bg-blue-100 text-blue-700' :
                                                    'bg-gray-100 text-gray-700'
                                                }`}>
                                                {complaint.complaint_status}
                                            </span>
                                        </td>
                                        <td className="py-3 px-4">
                                            {complaint.employee_id ? (
                                                <span className="text-sm text-gray-600">
                                                    {employees.find(e => e.user_id === complaint.employee_id)?.full_name || complaint.employee_id}
                                                </span>
                                            ) : (
                                                <select
                                                    className="text-sm border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-primary-500"
                                                    onChange={(e) => handleAssignEmployee(complaint.complaint_id, e.target.value)}
                                                    defaultValue=""
                                                >
                                                    <option value="" disabled>Select Employee</option>
                                                    {employees.map(emp => (
                                                        <option key={emp.user_id} value={emp.user_id}>
                                                            {emp.full_name} ({emp.department})
                                                        </option>
                                                    ))}
                                                </select>
                                            )}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>

                {/* Recent Payments */}
                <div className="bg-white rounded-xl shadow-lg p-6">
                    <h3 className="text-xl font-bold text-gray-800 mb-4">Recent Payments</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {payments.slice(0, 6).map((payment) => (
                            <div key={payment.payment_id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                                <div className="flex items-center justify-between mb-2">
                                    <p className="font-semibold text-gray-800">{payment.tenant_name}</p>
                                    <span className={`px-2 py-1 rounded text-xs font-semibold ${payment.payment_status === 'Paid' ? 'bg-green-100 text-green-700' :
                                        payment.payment_status === 'Overdue' ? 'bg-red-100 text-red-700' :
                                            'bg-yellow-100 text-yellow-700'
                                        }`}>
                                        {payment.payment_status}
                                    </span>
                                </div>
                                <p className="text-sm text-gray-600">Room {payment.room_no}</p>
                                <p className="text-lg font-bold text-primary-600 mt-2">${payment.payment_amount.toLocaleString()}</p>
                                <p className="text-xs text-gray-500">{payment.payment_date}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default OwnerDashboard;
