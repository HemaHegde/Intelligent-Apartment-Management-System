import { useState, useEffect } from 'react';
import { FaHome, FaExclamationCircle, FaDollarSign, FaPlus } from 'react-icons/fa';
import Navbar from '../components/Navbar';
import SummaryCard from '../components/SummaryCard';
import PriorityTag from '../components/PriorityTag';
import { getApartmentSummary, getComplaints, getPayments, createComplaint } from '../utils/api';
import { getUserInfo } from '../utils/auth';

const TenantDashboard = () => {
    const [summary, setSummary] = useState(null);
    const [complaints, setComplaints] = useState([]);
    const [payments, setPayments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showComplaintForm, setShowComplaintForm] = useState(false);
    const [newComplaint, setNewComplaint] = useState({
        complaint_text: '',
        complaint_category: 'Electricity',
        room_no: ''
    });

    const user = getUserInfo();

    // Extract room number from user_id (format: T126 -> 126)
    const roomNumber = user?.room_no || (user?.user_id ? user.user_id.substring(1) : '126');
    const apartmentName = user?.apartment_name || 'My Apartment';

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const [summaryRes, complaintsRes, paymentsRes] = await Promise.all([
                getApartmentSummary(),
                getComplaints({ limit: 20 }),
                getPayments({ limit: 10 })
            ]);

            setSummary(summaryRes.data);
            setComplaints(complaintsRes.data.complaints);
            setPayments(paymentsRes.data.payments);
        } catch (error) {
            console.error('Error fetching data:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmitComplaint = async (e) => {
        e.preventDefault();

        try {
            // Add room number to complaint before submitting
            const complaintData = {
                ...newComplaint,
                room_no: roomNumber
            };

            await createComplaint(complaintData);
            alert('Complaint submitted successfully! Priority has been automatically assigned by our AI system.');
            setShowComplaintForm(false);
            setNewComplaint({ complaint_text: '', complaint_category: 'Electricity', room_no: '' });
            fetchData();
        } catch (error) {
            alert('Failed to submit complaint: ' + (error.response?.data?.message || error.message));
        }
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
                <Navbar title="Tenant Dashboard" />

                {/* Tenant Info Banner */}
                <div className="bg-gradient-to-r from-green-500 to-green-600 rounded-xl shadow-lg p-6 mb-6 text-white">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm opacity-90">{apartmentName}</p>
                            <h2 className="text-3xl font-bold">Room {roomNumber}</h2>
                            <p className="text-sm mt-1 opacity-90">Viewing your personal data only</p>
                        </div>
                        <FaHome className="text-6xl opacity-20" />
                    </div>
                </div>

                {/* Summary Cards */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                    <SummaryCard
                        icon={FaHome}
                        title={apartmentName}
                        value={`Room ${roomNumber}`}
                        color="primary"
                    />
                    <SummaryCard
                        icon={FaExclamationCircle}
                        title="My Complaints"
                        value={summary?.total_complaints || 0}
                        color="warning"
                    />
                    <SummaryCard
                        icon={FaDollarSign}
                        title="Pending Payments"
                        value={summary?.pending_payments || 0}
                        color="danger"
                    />
                </div>

                {/* Submit Complaint Button */}
                <div className="mb-6">
                    <button
                        onClick={() => setShowComplaintForm(!showComplaintForm)}
                        className="flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-primary-500 to-primary-700 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transition-all"
                    >
                        <FaPlus />
                        <span>Submit New Complaint</span>
                    </button>
                </div>

                {/* Complaint Form */}
                {showComplaintForm && (
                    <div className="bg-white rounded-xl shadow-lg p-6 mb-6 animate-slide-up">
                        <h3 className="text-xl font-bold text-gray-800 mb-4">Submit New Complaint</h3>
                        <form onSubmit={handleSubmitComplaint} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">Category</label>
                                <select
                                    value={newComplaint.complaint_category}
                                    onChange={(e) => setNewComplaint({ ...newComplaint, complaint_category: e.target.value })}
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                                >
                                    <option value="Electricity">Electricity</option>
                                    <option value="Plumbing">Plumbing</option>
                                    <option value="Housekeeping">Housekeeping</option>
                                    <option value="Water">Water</option>
                                    <option value="Other">Other</option>
                                </select>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">Complaint Description</label>
                                <textarea
                                    value={newComplaint.complaint_text}
                                    onChange={(e) => setNewComplaint({ ...newComplaint, complaint_text: e.target.value })}
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                                    rows="4"
                                    placeholder="Describe your issue in detail..."
                                    required
                                />
                            </div>

                            <div className="flex space-x-4">
                                <button
                                    type="submit"
                                    className="px-6 py-2 bg-primary-600 text-white font-semibold rounded-lg hover:bg-primary-700 transition-colors"
                                >
                                    Submit Complaint
                                </button>
                                <button
                                    type="button"
                                    onClick={() => setShowComplaintForm(false)}
                                    className="px-6 py-2 bg-gray-300 text-gray-700 font-semibold rounded-lg hover:bg-gray-400 transition-colors"
                                >
                                    Cancel
                                </button>
                            </div>
                        </form>
                    </div>
                )}

                {/* My Complaints */}
                <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
                    <h3 className="text-xl font-bold text-gray-800 mb-4">My Complaints</h3>
                    <div className="space-y-4">
                        {complaints.map((complaint) => (
                            <div key={complaint.complaint_id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                                <div className="flex items-start justify-between mb-2">
                                    <div className="flex-1">
                                        <p className="font-semibold text-gray-800">{complaint.complaint_text}</p>
                                        <p className="text-sm text-gray-500 mt-1">{complaint.complaint_category}</p>
                                    </div>
                                    <PriorityTag priority={complaint.priority} />
                                </div>
                                <div className="flex items-center justify-between mt-3">
                                    <span className={`px-3 py-1 rounded text-xs font-semibold ${complaint.complaint_status === 'Resolved' ? 'bg-green-100 text-green-700' :
                                        complaint.complaint_status === 'In Progress' ? 'bg-blue-100 text-blue-700' :
                                            'bg-gray-100 text-gray-700'
                                        }`}>
                                        {complaint.complaint_status}
                                    </span>
                                    <span className="text-xs text-gray-500">{complaint.complaint_id}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Payment History */}
                <div className="bg-white rounded-xl shadow-lg p-6">
                    <h3 className="text-xl font-bold text-gray-800 mb-4">Payment History</h3>
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead>
                                <tr className="border-b border-gray-200">
                                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Payment ID</th>
                                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Amount</th>
                                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Date</th>
                                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                {payments.map((payment) => (
                                    <tr key={payment.payment_id} className="border-b border-gray-100 hover:bg-gray-50">
                                        <td className="py-3 px-4 text-sm">{payment.payment_id}</td>
                                        <td className="py-3 px-4 text-sm font-semibold">₹{payment.payment_amount.toLocaleString()}</td>
                                        <td className="py-3 px-4 text-sm">{payment.payment_date}</td>
                                        <td className="py-3 px-4">
                                            <span className={`px-2 py-1 rounded text-xs font-semibold ${payment.payment_status === 'Paid' ? 'bg-green-100 text-green-700' :
                                                payment.payment_status === 'Overdue' ? 'bg-red-100 text-red-700' :
                                                    'bg-yellow-100 text-yellow-700'
                                                }`}>
                                                {payment.payment_status}
                                            </span>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default TenantDashboard;
