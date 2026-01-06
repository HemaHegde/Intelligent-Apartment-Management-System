import { useState, useEffect } from 'react';
import { FaBuilding, FaUserTie, FaExclamationTriangle, FaMoneyBillWave } from 'react-icons/fa';
import { getBuildingsSummary } from '../utils/api';

const BuildingStats = () => {
    const [buildings, setBuildings] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchBuildings();
    }, []);

    const fetchBuildings = async () => {
        try {
            const response = await getBuildingsSummary();
            setBuildings(response.data.buildings);
            setLoading(false);
        } catch (err) {
            setError('Failed to fetch building data');
            setLoading(false);
        }
    };

    if (loading) return <div className="text-center py-10">Loading building statistics...</div>;
    if (error) return <div className="text-center py-10 text-red-500">{error}</div>;

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {buildings.map((building) => (
                <div key={building.building_code} className="bg-white rounded-xl shadow-lg hover:shadow-xl transition-all p-6 relative overflow-hidden group">
                    <div className="absolute top-0 right-0 w-24 h-24 bg-primary-100 rounded-bl-full -mr-4 -mt-4 opacity-50 group-hover:scale-110 transition-transform"></div>

                    <h3 className="text-xl font-bold text-gray-800 mb-1 relative z-10">{building.building_name}</h3>
                    <p className="text-sm text-gray-500 mb-4 relative z-10">{building.building_code}</p>

                    <div className="space-y-3 relative z-10">
                        <div className="flex justify-between items-center text-sm">
                            <span className="text-gray-600 flex items-center gap-2">
                                <FaBuilding className="text-primary-500" /> Apartments
                            </span>
                            <span className="font-semibold">{building.total_apartments}</span>
                        </div>

                        <div className="flex justify-between items-center text-sm">
                            <span className="text-gray-600 flex items-center gap-2">
                                <FaExclamationTriangle className="text-yellow-500" /> Complaints
                            </span>
                            <span className="font-semibold">{building.total_complaints} ({building.pending_complaints} pending)</span>
                        </div>

                        <div className="flex justify-between items-center text-sm">
                            <span className="text-gray-600 flex items-center gap-2">
                                <FaMoneyBillWave className="text-green-500" /> Revenue
                            </span>
                            <span className="font-semibold text-green-600">₹{building.total_revenue.toLocaleString()}</span>
                        </div>

                        <div className="pt-3 border-t border-gray-100 mt-3">
                            <div className="flex justify-between items-center text-sm">
                                <span className="text-gray-600 flex items-center gap-2">
                                    <FaUserTie className="text-purple-500" /> Owner
                                </span>
                                <span className={`font-semibold ${building.owner ? 'text-gray-800' : 'text-red-500 italic'}`}>
                                    {building.owner?.full_name || 'Unassigned'}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default BuildingStats;
