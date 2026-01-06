import { useState, useEffect } from 'react';
import { getEmployeePerformance, getPaymentAnalytics } from '../utils/api';
import { FaUserClock, FaChartPie, FaListOl, FaExclamationCircle } from 'react-icons/fa';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const AnalyticsDashboard = () => {
    const [employeeData, setEmployeeData] = useState([]);
    const [paymentData, setPaymentData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [empRes, payRes] = await Promise.all([
                    getEmployeePerformance(),
                    getPaymentAnalytics()
                ]);

                setEmployeeData(empRes.data.employees);
                setPaymentData(payRes.data);
            } catch (error) {
                console.error("Error fetching analytics:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) return <div className="text-center py-10">Loading analytics data...</div>;

    // Chart Data Preparation
    const empChartData = employeeData.map(e => ({
        name: e.full_name.split(' ')[0], // First name only for clearer X-axis
        'Resolved': e.resolved,
        'Pending': e.current_workload,
        fullName: e.full_name
    }));

    const revChartData = paymentData?.revenue_by_building.map(b => ({
        name: b.building,
        value: b.revenue
    })) || [];

    const COLORS = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#C9CBCF', '#7BC225'];

    return (
        <div className="space-y-8">
            {/* Employee Performance Section */}
            <div className="bg-white rounded-xl shadow-lg p-6">
                <div className="flex items-center gap-3 mb-6">
                    <FaUserClock className="text-2xl text-primary-600" />
                    <h2 className="text-xl font-bold text-gray-800">Employee Performance Metrics</h2>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* Performance Chart */}
                    <div className="lg:col-span-2 h-80">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={empChartData}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="name" />
                                <YAxis />
                                <Tooltip content={({ active, payload, label }) => {
                                    if (active && payload && payload.length) {
                                        return (
                                            <div className="bg-white p-2 border border-gray-200 shadow-lg rounded">
                                                <p className="font-bold">{payload[0].payload.fullName}</p>
                                                <p className="text-green-600">Resolved: {payload[0].value}</p>
                                                <p className="text-red-500">Pending: {payload[1].value}</p>
                                            </div>
                                        );
                                    }
                                    return null;
                                }} />
                                <Legend />
                                <Bar dataKey="Resolved" fill="#22c55e" />
                                <Bar dataKey="Pending" fill="#ef4444" />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>

                    {/* Top Performers List */}
                    <div className="space-y-4 overflow-y-auto max-h-80 pr-2">
                        <h3 className="font-semibold text-gray-700 flex items-center gap-2">
                            <FaListOl /> Ranking
                        </h3>
                        {employeeData.map((emp, index) => (
                            <div key={emp.employee_id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition">
                                <div className="flex items-center gap-3">
                                    <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-white ${index === 0 ? 'bg-yellow-400' : index === 1 ? 'bg-gray-400' : index === 2 ? 'bg-amber-600' : 'bg-primary-500'
                                        }`}>
                                        {index + 1}
                                    </div>
                                    <div>
                                        <p className="font-medium text-gray-800">{emp.full_name}</p>
                                        <p className="text-xs text-gray-500">{emp.department}</p>
                                    </div>
                                </div>
                                <div className="text-right">
                                    <p className="font-bold text-green-600">{emp.resolution_rate}%</p>
                                    <p className="text-xs text-gray-500">Resolution Rate</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Payment Analytics Section */}
            <div className="bg-white rounded-xl shadow-lg p-6">
                <div className="flex items-center gap-3 mb-6">
                    <FaChartPie className="text-2xl text-primary-600" />
                    <h2 className="text-xl font-bold text-gray-800">Financial Insights</h2>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    {/* Revenue Chart */}
                    <div className="h-80 flex flex-col items-center">
                        <h3 className="text-sm font-semibold text-gray-600 mb-2">Revenue Distribution</h3>
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={revChartData}
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={60}
                                    outerRadius={100}
                                    fill="#8884d8"
                                    paddingAngle={5}
                                    dataKey="value"
                                >
                                    {revChartData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                    ))}
                                </Pie>
                                <Tooltip formatter={(value) => `₹${value.toLocaleString()}`} />
                                <Legend />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>

                    {/* Top Defaulters Table */}
                    <div>
                        <h3 className="text-sm font-semibold text-gray-600 mb-4 flex items-center gap-2">
                            <FaExclamationCircle className="text-red-500" /> Top Payment Defaulters
                        </h3>
                        <div className="overflow-x-auto">
                            <table className="w-full text-sm">
                                <thead className="bg-gray-50">
                                    <tr>
                                        <th className="px-3 py-2 text-left">Tenant</th>
                                        <th className="px-3 py-2 text-center">Building</th>
                                        <th className="px-3 py-2 text-center">Overdue Count</th>
                                        <th className="px-3 py-2 text-right">Total Amount</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-gray-100">
                                    {paymentData?.top_defaulters.map((defaulter) => (
                                        <tr key={defaulter._id} className="hover:bg-gray-50">
                                            <td className="px-3 py-2 font-medium">{defaulter.tenant_name || defaulter._id}</td>
                                            <td className="px-3 py-2 text-center text-gray-600">{defaulter.block_no} - {defaulter.room_no}</td>
                                            <td className="px-3 py-2 text-center text-red-600">{defaulter.overdue_count}</td>
                                            <td className="px-3 py-2 text-right font-semibold">₹{defaulter.total_overdue_amount}</td>
                                        </tr>
                                    ))}
                                    {(!paymentData?.top_defaulters || paymentData.top_defaulters.length === 0) && (
                                        <tr>
                                            <td colSpan="3" className="text-center py-4 text-gray-500">No overdue payments found</td>
                                        </tr>
                                    )}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8">
                    <div className="bg-green-50 p-4 rounded-lg text-center">
                        <p className="text-sm text-green-600 mb-1">Collection Rate</p>
                        <p className="text-2xl font-bold text-green-700">{paymentData?.collection_rate}%</p>
                    </div>
                    <div className="bg-blue-50 p-4 rounded-lg text-center">
                        <p className="text-sm text-blue-600 mb-1">Paid Invoices</p>
                        <p className="text-2xl font-bold text-blue-700">{paymentData?.paid_payments}</p>
                    </div>
                    <div className="bg-yellow-50 p-4 rounded-lg text-center">
                        <p className="text-sm text-yellow-600 mb-1">Pending Invoices</p>
                        <p className="text-2xl font-bold text-yellow-700">{paymentData?.pending_payments}</p>
                    </div>
                    <div className="bg-red-50 p-4 rounded-lg text-center">
                        <p className="text-sm text-red-600 mb-1">Overdue Invoices</p>
                        <p className="text-2xl font-bold text-red-700">{paymentData?.overdue_payments}</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AnalyticsDashboard;
