import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const PaymentTrendChart = ({ data }) => {
    // Transform data for chart
    const chartData = data || [
        { month: 'Jan', Paid: 45000, Pending: 5000, Overdue: 2000 },
        { month: 'Feb', Paid: 52000, Pending: 3000, Overdue: 1500 },
        { month: 'Mar', Paid: 48000, Pending: 6000, Overdue: 2500 },
        { month: 'Apr', Paid: 61000, Pending: 4000, Overdue: 1000 },
        { month: 'May', Paid: 55000, Pending: 5500, Overdue: 1800 },
        { month: 'Jun', Paid: 67000, Pending: 3500, Overdue: 1200 },
    ];

    return (
        <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-xl font-bold text-gray-800 mb-4">Payment Trends</h3>
            <ResponsiveContainer width="100%" height={300}>
                <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis dataKey="month" stroke="#666" />
                    <YAxis stroke="#666" />
                    <Tooltip
                        contentStyle={{
                            backgroundColor: '#fff',
                            border: '1px solid #e0e0e0',
                            borderRadius: '8px',
                            boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
                        }}
                        formatter={(value) => `$${value.toLocaleString()}`}
                    />
                    <Legend />
                    <Bar dataKey="Paid" fill="#10b981" radius={[8, 8, 0, 0]} />
                    <Bar dataKey="Pending" fill="#f59e0b" radius={[8, 8, 0, 0]} />
                    <Bar dataKey="Overdue" fill="#ef4444" radius={[8, 8, 0, 0]} />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
};

export default PaymentTrendChart;
