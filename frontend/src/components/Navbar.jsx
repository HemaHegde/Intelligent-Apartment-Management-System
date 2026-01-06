import { FaSignOutAlt } from 'react-icons/fa';
import { logoutUser, getUserInfo } from '../utils/auth';

const Navbar = ({ title }) => {
    const user = getUserInfo();

    const handleLogout = () => {
        if (window.confirm('Are you sure you want to logout?')) {
            logoutUser();
        }
    };

    return (
        <nav className="bg-white shadow-md px-6 py-4 mb-6 rounded-xl">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold text-gray-800">{title}</h1>
                    <p className="text-sm text-gray-500">Welcome back, {user?.full_name || user?.username}!</p>
                </div>

                <div className="flex items-center space-x-4">
                    <div className="text-right">
                        <p className="text-sm font-medium text-gray-700">{user?.full_name}</p>
                        <p className="text-xs text-gray-500">{user?.role}</p>
                    </div>

                    <button
                        onClick={handleLogout}
                        className="flex items-center space-x-2 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
                    >
                        <FaSignOutAlt />
                        <span>Logout</span>
                    </button>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
