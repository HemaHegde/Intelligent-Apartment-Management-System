import { useState, useEffect } from 'react';
import { FaBuilding, FaExclamationTriangle, FaDollarSign, FaChartLine, FaRobot, FaUsers, FaChartPie, FaList } from 'react-icons/fa';
import Navbar from '../components/Navbar';
import SummaryCard from '../components/SummaryCard';
import PriorityTag from '../components/PriorityTag';
import ComplaintTrendChart from '../components/ComplaintTrendChart';
import PaymentTrendChart from '../components/PaymentTrendChart';
import BuildingStats from '../components/BuildingStats';
import UserManagement from '../components/UserManagement';
import AnalyticsDashboard from '../components/AnalyticsDashboard';
import { getApartmentSummary, getComplaints, getPaymentRiskAlerts, batchPredictComplaints, getEmployees, updateComplaint } from '../utils/api';

const AdminDashboard = () => {
    const [activeTab, setActiveTab] = useState('overview');
    const [summary, setSummary] = useState(null);
    const [complaints, setComplaints] = useState([]);
    const [riskAlerts, setRiskAlerts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [employees, setEmployees] = useState([]);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const [summaryRes, complaintsRes, riskRes, empRes] = await Promise.all([
                getApartmentSummary(),
                getComplaints({ limit: 10 }),
                getPaymentRiskAlerts(0.5),
                getEmployees()
            ]);

            setSummary(summaryRes.data);
            setComplaints(complaintsRes.data.complaints);
            setRiskAlerts(riskRes.data.at_risk_payments);
            setEmployees(empRes.data.employees);
        } catch (error) {
            console.error('Error fetching data:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleBatchPredict = async () => {
        try {
            await batchPredictComplaints();
            alert('Batch prediction completed! Refreshing data...');
            fetchData();
        } catch (error) {
            alert('Batch prediction failed: ' + error.message);
        }
    };

    const handleAssignEmployee = async (complaintId, employeeId) => {
        try {
            await updateComplaint(complaintId, { employee_id: employeeId });
            alert('Complaint assigned successfully!');
            fetchData();
        } catch (error) {
            alert('Failed to assign complaint: ' + error.message);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-6 flex items-center justify-center">
                <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-primary-600"></div>
            </div>
        );
    }

    const tabs = [
        { id: 'overview', label: 'Overview', icon: FaChartLine },
        { id: 'buildings', label: 'Building Status', icon: FaBuilding },
        { id: 'users', label: 'User Directory', icon: FaUsers },
        { id: 'analytics', label: 'Analytics', icon: FaChartPie },
    ];

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-6">
            <div className="max-w-7xl mx-auto">
                <Navbar title="Admin Dashboard" />

                {/* Tab Navigation */}
                <div className="flex flex-wrap gap-4 mb-8 bg-white p-2 rounded-xl shadow-sm overflow-x-auto">
                    {tabs.map(tab => (
                        <button
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            className={`flex items-center gap-2 px-6 py-3 rounded-lg font-semibold transition-all whitespace-nowrap ${activeTab === tab.id
                                ? 'bg-primary-600 text-white shadow-md'
                                : 'bg-transparent text-gray-600 hover:bg-gray-100'
                                }`}
                        >
                            <tab.icon /> {tab.label}
                        </button>
                    ))}
                </div>

                {/* Tab Content */}
                <div className="animate-fade-in">
                    {activeTab === 'overview' && (
                        <>
                            {/* Summary Cards */}
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
                                <SummaryCard icon={FaBuilding} title="Total Apartments" value={summary?.total_apartments || 0} color="primary" />
                                <SummaryCard icon={FaExclamationTriangle} title="Total Complaints" value={summary?.total_complaints || 0} color="warning" />
                                <SummaryCard icon={FaDollarSign} title="Total Revenue" value={`₹${(summary?.total_revenue || 0).toLocaleString()}`} color="success" />
                                <SummaryCard icon={FaChartLine} title="Overdue Payments" value={summary?.overdue_payments || 0} color="danger" />
                            </div>

                            {/* Priority Distribution */}
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                                <div className="bg-white rounded-xl shadow-lg p-6 border-t-4 border-red-500">
                                    <h3 className="text-lg font-semibold text-gray-700 mb-2">High Priority Issues</h3>
                                    <p className="text-3xl font-bold text-red-600">{summary?.high_priority_complaints || 0}</p>
                                </div>
                                <div className="bg-white rounded-xl shadow-lg p-6 border-t-4 border-yellow-500">
                                    <h3 className="text-lg font-semibold text-gray-700 mb-2">Medium Priority Issues</h3>
                                    <p className="text-3xl font-bold text-yellow-600">{summary?.medium_priority_complaints || 0}</p>
                                </div>
                                <div className="bg-white rounded-xl shadow-lg p-6 border-t-4 border-green-500">
                                    <h3 className="text-lg font-semibold text-gray-700 mb-2">Low Priority Issues</h3>
                                    <p className="text-3xl font-bold text-green-600">{summary?.low_priority_complaints || 0}</p>
                                </div>
                            </div>

                            {/* ML Actions */}
                            <div className="bg-gradient-to-r from-purple-600 to-indigo-600 rounded-xl shadow-lg p-6 mb-6 text-white flex items-center justify-between">
                                <div className="flex items-center space-x-4">
                                    <div className="p-3 bg-white/20 rounded-full">
                                        <FaRobot className="text-2xl" />
                                    </div>
                                    <div>
                                        <h3 className="text-xl font-bold">AI Assistant</h3>
                                        <p className="text-sm opacity-90">Auto-classify complaint priorities & predict risks</p>
                                    </div>
                                </div>
                                <button
                                    onClick={handleBatchPredict}
                                    className="px-6 py-2 bg-white text-purple-600 font-bold rounded-lg hover:bg-purple-50 transition shadow-lg"
                                >
                                    Run AI Analysis
                                </button>
                            </div>

                            {/* Charts */}
                            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                                <ComplaintTrendChart />
                                <PaymentTrendChart />
                            </div>

                            {/* Recent Complaints with Assignment */}
                            <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
                                <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                                    <FaList /> Recent Complaints
                                </h3>
                                <div className="overflow-x-auto">
                                    <table className="w-full">
                                        <thead>
                                            <tr className="bg-gray-50 border-b border-gray-200">
                                                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">ID</th>
                                                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Complaint</th>
                                                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Category</th>
                                                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Priority</th>
                                                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Status</th>
                                                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Assigned To</th>
                                            </tr>
                                        </thead>
                                        <tbody className="divide-y divide-gray-100">
                                            {complaints.slice(0, 10).map((complaint) => (
                                                <tr key={complaint.complaint_id} className="hover:bg-gray-50 transition">
                                                    <td className="py-3 px-4 text-sm font-medium text-gray-900">{complaint.complaint_id}</td>
                                                    <td className="py-3 px-4 text-sm text-gray-600 max-w-xs truncate" title={complaint.complaint_text}>{complaint.complaint_text}</td>
                                                    <td className="py-3 px-4 text-sm text-gray-600">{complaint.complaint_category}</td>
                                                    <td className="py-3 px-4"><PriorityTag priority={complaint.priority} /></td>
                                                    <td className="py-3 px-4">
                                                        <span className={`px-2 py-1 rounded-full text-xs font-semibold ${complaint.complaint_status === 'Resolved' ? 'bg-green-100 text-green-700' :
                                                            complaint.complaint_status === 'In Progress' ? 'bg-blue-100 text-blue-700' :
                                                                'bg-gray-100 text-gray-700'
                                                            }`}>
                                                            {complaint.complaint_status}
                                                        </span>
                                                    </td>
                                                    <td className="py-3 px-4">
                                                        {complaint.employee_id ? (
                                                            <span className="text-sm font-medium text-gray-700">
                                                                {employees.find(e => e.user_id === complaint.employee_id)?.full_name || complaint.employee_id}
                                                            </span>
                                                        ) : (
                                                            <select
                                                                className="text-sm border border-gray-300 rounded px-2 py-1 focus:ring-2 focus:ring-primary-500 bg-white"
                                                                onChange={(e) => handleAssignEmployee(complaint.complaint_id, e.target.value)}
                                                                defaultValue=""
                                                            >
                                                                <option value="" disabled>Assign</option>
                                                                {employees.map(emp => (
                                                                    <option key={emp.user_id} value={emp.user_id}>{emp.full_name}</option>
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

                            {/* Risk Alerts */}
                            {riskAlerts.length > 0 && (
                                <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-red-500">
                                    <h3 className="text-xl font-bold text-red-600 mb-4 flex items-center gap-2">
                                        <FaExclamationTriangle /> High Risk Payment Alerts
                                    </h3>
                                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                                        {riskAlerts.slice(0, 6).map((alert) => (
                                            <div key={alert.payment_id} className="bg-red-50 p-4 rounded-lg flex items-center justify-between hover:shadow-md transition">
                                                <div>
                                                    <p className="font-bold text-gray-800">{alert.tenant_name}</p>
                                                    <p className="text-sm text-gray-600">Room {alert.room_no}</p>
                                                    <p className="text-xs text-red-500 mt-1">Due: ₹{alert.payment_amount}</p>
                                                </div>
                                                <div className="text-right">
                                                    <div className="text-2xl font-bold text-red-600">{(alert.risk_score * 100).toFixed(0)}%</div>
                                                    <div className="text-xs text-red-400 font-semibold uppercase">Risk Score</div>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </>
                    )}

                    {activeTab === 'buildings' && <BuildingStats />}
                    {activeTab === 'users' && <UserManagement />}
                    {activeTab === 'analytics' && <AnalyticsDashboard />}
                </div>
            </div>
        </div>
    );
};

export default AdminDashboard;
