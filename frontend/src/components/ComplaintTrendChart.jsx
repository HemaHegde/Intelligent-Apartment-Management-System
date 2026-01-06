import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const ComplaintTrendChart = ({ data }) => {
    // Transform data for chart
    const chartData = data || [
        { name: 'Week 1', Electricity: 12, Plumbing: 8, Housekeeping: 15, Water: 5 },
        { name: 'Week 2', Electricity: 15, Plumbing: 10, Housekeeping: 12, Water: 7 },
        { name: 'Week 3', Electricity: 10, Plumbing: 12, Housekeeping: 18, Water: 6 },
        { name: 'Week 4', Electricity: 18, Plumbing: 9, Housekeeping: 14, Water: 8 },
    ];

    return (
        <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-xl font-bold text-gray-800 mb-4">Complaint Trends</h3>
            <ResponsiveContainer width="100%" height={300}>
                <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis dataKey="name" stroke="#666" />
                    <YAxis stroke="#666" />
                    <Tooltip
                        contentStyle={{
                            backgroundColor: '#fff',
                            border: '1px solid #e0e0e0',
                            borderRadius: '8px',
                            boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
                        }}
                    />
                    <Legend />
                    <Line type="monotone" dataKey="Electricity" stroke="#ef4444" strokeWidth={2} dot={{ r: 4 }} activeDot={{ r: 6 }} />
                    <Line type="monotone" dataKey="Plumbing" stroke="#3b82f6" strokeWidth={2} dot={{ r: 4 }} activeDot={{ r: 6 }} />
                    <Line type="monotone" dataKey="Housekeeping" stroke="#10b981" strokeWidth={2} dot={{ r: 4 }} activeDot={{ r: 6 }} />
                    <Line type="monotone" dataKey="Water" stroke="#8b5cf6" strokeWidth={2} dot={{ r: 4 }} activeDot={{ r: 6 }} />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
};

export default ComplaintTrendChart;
