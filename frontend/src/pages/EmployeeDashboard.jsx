import { useState, useEffect } from 'react';
import { FaTasks, FaCheckCircle, FaClock, FaExclamationTriangle } from 'react-icons/fa';
import Navbar from '../components/Navbar';
import SummaryCard from '../components/SummaryCard';
import PriorityTag from '../components/PriorityTag';
import { getComplaints, updateComplaint } from '../utils/api';

const EmployeeDashboard = () => {
    const [complaints, setComplaints] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState('all');

    useEffect(() => {
        fetchComplaints();
    }, []);

    const fetchComplaints = async () => {
        try {
            const response = await getComplaints({ limit: 50 });
            setComplaints(response.data.complaints);
        } catch (error) {
            console.error('Error fetching complaints:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleStatusUpdate = async (complaintId, newStatus) => {
        try {
            await updateComplaint(complaintId, { complaint_status: newStatus });
            alert('Status updated successfully!');
            fetchComplaints();
        } catch (error) {
            alert('Failed to update status: ' + error.message);
        }
    };

    const getFilteredComplaints = () => {
        if (filter === 'all') return complaints;
        if (filter === 'high') return complaints.filter(c => c.priority === 'High');
        if (filter === 'medium') return complaints.filter(c => c.priority === 'Medium');
        if (filter === 'low') return complaints.filter(c => c.priority === 'Low');
        if (filter === 'pending') return complaints.filter(c => c.complaint_status === 'Pending');
        if (filter === 'in-progress') return complaints.filter(c => c.complaint_status === 'In Progress');
        return complaints;
    };

    const filteredComplaints = getFilteredComplaints();

    const pendingCount = complaints.filter(c => c.complaint_status === 'Pending').length;
    const inProgressCount = complaints.filter(c => c.complaint_status === 'In Progress').length;
    const resolvedCount = complaints.filter(c => c.complaint_status === 'Resolved').length;
    const highPriorityCount = complaints.filter(c => c.priority === 'High').length;
    const mediumPriorityCount = complaints.filter(c => c.priority === 'Medium').length;
    const lowPriorityCount = complaints.filter(c => c.priority === 'Low').length;

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
                <Navbar title="Employee Dashboard" />

                {/* Employee Info Banner */}
                <div className="bg-gradient-to-r from-blue-500 to-blue-600 rounded-xl shadow-lg p-6 mb-6 text-white">
                    <div className="flex items-center justify-between">
                        <div>
                            <h2 className="text-2xl font-bold">Work Queue</h2>
                            <p className="text-sm mt-1 opacity-90">Showing complaints assigned to you only</p>
                        </div>
                        <FaTasks className="text-5xl opacity-20" />
                    </div>
                </div>

                {/* Summary Cards */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
                    <SummaryCard
                        icon={FaTasks}
                        title="Pending Tasks"
                        value={pendingCount}
                        color="warning"
                    />
                    <SummaryCard
                        icon={FaClock}
                        title="In Progress"
                        value={inProgressCount}
                        color="info"
                    />
                    <SummaryCard
                        icon={FaCheckCircle}
                        title="Resolved"
                        value={resolvedCount}
                        color="success"
                    />
                    <SummaryCard
                        icon={FaExclamationTriangle}
                        title="High Priority"
                        value={highPriorityCount}
                        color="danger"
                    />
                </div>

                {/* Filters */}
                <div className="bg-white rounded-xl shadow-lg p-4 mb-6">
                    <div className="space-y-3">
                        {/* Status Filters */}
                        <div className="flex items-center space-x-3">
                            <span className="text-sm font-semibold text-gray-700 w-24">Status:</span>
                            <button
                                onClick={() => setFilter('all')}
                                className={`px-4 py-2 rounded-lg font-medium transition-colors ${filter === 'all' ? 'bg-primary-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                                    }`}
                            >
                                All ({complaints.length})
                            </button>
                            <button
                                onClick={() => setFilter('pending')}
                                className={`px-4 py-2 rounded-lg font-medium transition-colors ${filter === 'pending' ? 'bg-yellow-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                                    }`}
                            >
                                Pending ({pendingCount})
                            </button>
                            <button
                                onClick={() => setFilter('in-progress')}
                                className={`px-4 py-2 rounded-lg font-medium transition-colors ${filter === 'in-progress' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                                    }`}
                            >
                                In Progress ({inProgressCount})
                            </button>
                        </div>

                        {/* Priority Filters */}
                        <div className="flex items-center space-x-3">
                            <span className="text-sm font-semibold text-gray-700 w-24">Priority:</span>
                            <button
                                onClick={() => setFilter('high')}
                                className={`px-4 py-2 rounded-lg font-medium transition-colors ${filter === 'high' ? 'bg-red-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                                    }`}
                            >
                                🔴 High ({highPriorityCount})
                            </button>
                            <button
                                onClick={() => setFilter('medium')}
                                className={`px-4 py-2 rounded-lg font-medium transition-colors ${filter === 'medium' ? 'bg-orange-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                                    }`}
                            >
                                🟠 Medium ({mediumPriorityCount})
                            </button>
                            <button
                                onClick={() => setFilter('low')}
                                className={`px-4 py-2 rounded-lg font-medium transition-colors ${filter === 'low' ? 'bg-green-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                                    }`}
                            >
                                🟢 Low ({lowPriorityCount})
                            </button>
                        </div>
                    </div>
                </div>

                {/* Complaints List */}
                <div className="bg-white rounded-xl shadow-lg p-6">
                    <h3 className="text-xl font-bold text-gray-800 mb-4">Assigned Complaints</h3>
                    <div className="space-y-4">
                        {filteredComplaints.map((complaint) => (
                            <div key={complaint.complaint_id} className="border border-gray-200 rounded-lg p-5 hover:shadow-md transition-shadow">
                                <div className="flex items-start justify-between mb-3">
                                    <div className="flex-1">
                                        <div className="flex items-center space-x-3 mb-2">
                                            <span className="text-sm font-semibold text-gray-500">{complaint.complaint_id}</span>
                                            <PriorityTag priority={complaint.priority} />
                                            <span className="text-sm text-gray-500">Room {complaint.room_no}</span>
                                        </div>
                                        <p className="font-semibold text-gray-800 text-lg">{complaint.complaint_text}</p>
                                        <p className="text-sm text-gray-600 mt-1">
                                            <span className="font-medium">Category:</span> {complaint.complaint_category} |
                                            <span className="font-medium ml-2">Tenant:</span> {complaint.tenant_name}
                                        </p>
                                    </div>
                                </div>

                                <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-200">
                                    <div className="flex items-center space-x-2">
                                        <span className="text-sm text-gray-600">Status:</span>
                                        <span className={`px-3 py-1 rounded text-xs font-semibold ${complaint.complaint_status === 'Resolved' ? 'bg-green-100 text-green-700' :
                                            complaint.complaint_status === 'In Progress' ? 'bg-blue-100 text-blue-700' :
                                                'bg-gray-100 text-gray-700'
                                            }`}>
                                            {complaint.complaint_status}
                                        </span>
                                    </div>

                                    <div className="flex space-x-2">
                                        {complaint.complaint_status === 'Pending' && (
                                            <button
                                                onClick={() => handleStatusUpdate(complaint.complaint_id, 'In Progress')}
                                                className="px-4 py-2 bg-blue-500 text-white text-sm font-semibold rounded-lg hover:bg-blue-600 transition-colors"
                                            >
                                                Start Work
                                            </button>
                                        )}
                                        {complaint.complaint_status === 'In Progress' && (
                                            <button
                                                onClick={() => handleStatusUpdate(complaint.complaint_id, 'Resolved')}
                                                className="px-4 py-2 bg-green-500 text-white text-sm font-semibold rounded-lg hover:bg-green-600 transition-colors"
                                            >
                                                Mark Resolved
                                            </button>
                                        )}
                                        {complaint.complaint_status === 'Resolved' && (
                                            <span className="px-4 py-2 bg-green-100 text-green-700 text-sm font-semibold rounded-lg">
                                                ✓ Completed
                                            </span>
                                        )}
                                    </div>
                                </div>
                            </div>
                        ))}

                        {filteredComplaints.length === 0 && (
                            <div className="text-center py-12 text-gray-500">
                                <p className="text-lg">No complaints found for this filter.</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default EmployeeDashboard;
