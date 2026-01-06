import { FaArrowUp, FaArrowDown } from 'react-icons/fa';

const SummaryCard = ({ icon: Icon, title, value, trend, trendValue, color = 'primary' }) => {
    const colorClasses = {
        primary: 'from-primary-500 to-primary-700',
        secondary: 'from-secondary-500 to-secondary-700',
        success: 'from-green-500 to-green-700',
        warning: 'from-yellow-500 to-yellow-700',
        danger: 'from-red-500 to-red-700',
        info: 'from-blue-500 to-blue-700',
    };

    return (
        <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-all duration-300 hover:scale-105">
            <div className="flex items-center justify-between">
                <div className="flex-1">
                    <p className="text-gray-500 text-sm font-medium mb-1">{title}</p>
                    <h3 className="text-3xl font-bold text-gray-800">{value}</h3>

                    {trend && (
                        <div className="flex items-center mt-2">
                            {trend === 'up' ? (
                                <FaArrowUp className="text-green-500 text-sm mr-1" />
                            ) : (
                                <FaArrowDown className="text-red-500 text-sm mr-1" />
                            )}
                            <span className={`text-sm font-medium ${trend === 'up' ? 'text-green-500' : 'text-red-500'}`}>
                                {trendValue}
                            </span>
                        </div>
                    )}
                </div>

                <div className={`w-16 h-16 rounded-full bg-gradient-to-br ${colorClasses[color]} flex items-center justify-center shadow-lg`}>
                    <Icon className="text-white text-2xl" />
                </div>
            </div>
        </div>
    );
};

export default SummaryCard;
