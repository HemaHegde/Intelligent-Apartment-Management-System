import { useState, useEffect } from 'react';
import { getUsers, updateUser, deleteUser } from '../utils/api';
import { FaUserEdit, FaTrash, FaUserPlus, FaSearch, FaFilter } from 'react-icons/fa';

const UserManagement = () => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const [roleFilter, setRoleFilter] = useState('All');

    // Modal states
    const [editingUser, setEditingUser] = useState(null);
    const [isEditModalOpen, setIsEditModalOpen] = useState(false);
    const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
    const [userToDelete, setUserToDelete] = useState(null);

    useEffect(() => {
        fetchUsers();
    }, []);

    const fetchUsers = async () => {
        try {
            const response = await getUsers();
            setUsers(response.data.users);
            setLoading(false);
        } catch (error) {
            console.error("Error fetching users:", error);
            setLoading(false);
        }
    };

    const handleUpdateUser = async (e) => {
        e.preventDefault();
        try {
            await updateUser(editingUser.user_id, editingUser);
            setIsEditModalOpen(false);
            fetchUsers(); // Refresh list
            alert('User updated successfully');
        } catch (error) {
            alert('Failed to update user: ' + error.message);
        }
    };

    const handleDeleteUser = async () => {
        try {
            await deleteUser(userToDelete.user_id);
            setIsDeleteModalOpen(false);
            fetchUsers(); // Refresh list
            alert('User deleted successfully');
        } catch (error) {
            alert('Failed to delete user: ' + error.message);
        }
    };

    const openEditModal = (user) => {
        setEditingUser({ ...user });
        setIsEditModalOpen(true);
    };

    const openDeleteModal = (user) => {
        setUserToDelete(user);
        setIsDeleteModalOpen(true);
    };

    // Filtering logic
    const filteredUsers = users.filter(user => {
        const matchesSearch =
            user.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
            user.full_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            user.email.toLowerCase().includes(searchTerm.toLowerCase());

        const matchesRole = roleFilter === 'All' || user.role === roleFilter;

        return matchesSearch && matchesRole;
    });

    if (loading) return <div className="text-center py-10">Loading users...</div>;

    return (
        <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex flex-col md:flex-row justify-between items-center mb-6 gap-4">
                <h2 className="text-xl font-bold text-gray-800">User Directory</h2>

                <div className="flex gap-4 w-full md:w-auto">
                    <a
                        href="/register"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-2 bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition shadow-md"
                    >
                        <FaUserPlus /> Add User
                    </a>

                    <div className="relative flex-1 md:w-64">
                        <FaSearch className="absolute left-3 top-3 text-gray-400" />
                        <input
                            type="text"
                            placeholder="Search users..."
                            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>

                    <div className="relative">
                        <FaFilter className="absolute left-3 top-3 text-gray-400" />
                        <select
                            className="pl-10 pr-8 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 appearance-none bg-white"
                            value={roleFilter}
                            onChange={(e) => setRoleFilter(e.target.value)}
                        >
                            <option value="All">All Roles</option>
                            <option value="Owner">Owners</option>
                            <option value="Tenant">Tenants</option>
                            <option value="Employee">Employees</option>
                            <option value="Admin">Admins</option>
                        </select>
                    </div>
                </div>
            </div>

            <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                    <thead>
                        <tr className="bg-gray-50 border-b border-gray-200 text-gray-600 text-sm">
                            <th className="py-3 px-4 font-semibold">User</th>
                            <th className="py-3 px-4 font-semibold">Role</th>
                            <th className="py-3 px-4 font-semibold">Assignment</th>
                            <th className="py-3 px-4 font-semibold">Contact</th>
                            <th className="py-3 px-4 font-semibold text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                        {filteredUsers.map((user) => (
                            <tr key={user.user_id} className="hover:bg-gray-50">
                                <td className="py-3 px-4">
                                    <div className="flex items-center gap-3">
                                        <div className="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center text-primary-600 font-bold">
                                            {user.full_name?.charAt(0) || 'U'}
                                        </div>
                                        <div>
                                            <p className="font-medium text-gray-800">{user.full_name}</p>
                                            <p className="text-xs text-gray-500">@{user.username}</p>
                                        </div>
                                    </div>
                                </td>
                                <td className="py-3 px-4">
                                    <span className={`px-2 py-1 rounded text-xs font-semibold ${user.role === 'Admin' ? 'bg-purple-100 text-purple-700' :
                                        user.role === 'Owner' ? 'bg-blue-100 text-blue-700' :
                                            user.role === 'Tenant' ? 'bg-green-100 text-green-700' :
                                                'bg-orange-100 text-orange-700'
                                        }`}>
                                        {user.role}
                                    </span>
                                </td>
                                <td className="py-3 px-4 text-sm text-gray-600">
                                    {user.role === 'Owner' && (user.managed_building ? `Building ${user.managed_building}` : 'Unassigned')}
                                    {user.role === 'Tenant' && `Room ${user.room_no}`}
                                    {user.role === 'Employee' && user.department}
                                </td>
                                <td className="py-3 px-4 text-sm text-gray-600">
                                    {user.email}
                                </td>
                                <td className="py-3 px-4 text-right">
                                    <div className="flex items-center justify-end gap-2">
                                        <button
                                            onClick={() => openEditModal(user)}
                                            className="p-1.5 text-blue-600 hover:bg-blue-50 rounded transition"
                                            title="Edit User"
                                        >
                                            <FaUserEdit />
                                        </button>
                                        <button
                                            onClick={() => openDeleteModal(user)}
                                            className="p-1.5 text-red-600 hover:bg-red-50 rounded transition"
                                            title="Delete User"
                                        >
                                            <FaTrash />
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* Edit User Modal */}
            {isEditModalOpen && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
                    <div className="bg-white rounded-xl shadow-2xl w-full max-w-md p-6 animate-fade-in">
                        <h3 className="text-xl font-bold mb-4">Edit User</h3>
                        <form onSubmit={handleUpdateUser}>
                            <div className="space-y-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
                                    <input
                                        type="text"
                                        className="w-full border rounded px-3 py-2"
                                        value={editingUser.full_name || ''}
                                        onChange={e => setEditingUser({ ...editingUser, full_name: e.target.value })}
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                                    <input
                                        type="email"
                                        className="w-full border rounded px-3 py-2"
                                        value={editingUser.email || ''}
                                        onChange={e => setEditingUser({ ...editingUser, email: e.target.value })}
                                    />
                                </div>

                                {editingUser.role === 'Owner' && (
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">Managed Building</label>
                                        <select
                                            className="w-full border rounded px-3 py-2"
                                            value={editingUser.managed_building || ''}
                                            onChange={e => setEditingUser({ ...editingUser, managed_building: e.target.value })}
                                        >
                                            <option value="">Select Building</option>
                                            <option value="B1">B1 - Maple Heights</option>
                                            <option value="B2">B2 - Harmony Residency</option>
                                            <option value="B3">B3 - Sunrise Enclave</option>
                                            <option value="B4">B4 - Lakeview Towers</option>
                                            <option value="B5">B5 - Green Meadows</option>
                                            <option value="B6">B6 - Silver Oaks</option>
                                            <option value="B7">B7 - Crystal View</option>
                                            <option value="B8">B8 - Riverside Park</option>
                                        </select>
                                    </div>
                                )}

                                {editingUser.role === 'Employee' && (
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">Department</label>
                                        <input
                                            type="text"
                                            className="w-full border rounded px-3 py-2"
                                            value={editingUser.department || ''}
                                            onChange={e => setEditingUser({ ...editingUser, department: e.target.value })}
                                        />
                                    </div>
                                )}
                            </div>
                            <div className="flex justify-end gap-3 mt-6">
                                <button
                                    type="button"
                                    onClick={() => setIsEditModalOpen(false)}
                                    className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded"
                                >
                                    Cancel
                                </button>
                                <button
                                    type="submit"
                                    className="px-4 py-2 bg-primary-600 text-white rounded hover:bg-primary-700"
                                >
                                    Save Changes
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* Delete Confirmation Modal */}
            {isDeleteModalOpen && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
                    <div className="bg-white rounded-xl shadow-2xl w-full max-w-sm p-6 animate-fade-in text-center">
                        <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                            <FaTrash className="text-red-600 text-xl" />
                        </div>
                        <h3 className="text-xl font-bold mb-2">Delete User?</h3>
                        <p className="text-gray-600 mb-6">
                            Are you sure you want to delete <strong>{userToDelete?.full_name}</strong>? This action cannot be undone.
                        </p>
                        <div className="flex justify-center gap-3">
                            <button
                                onClick={() => setIsDeleteModalOpen(false)}
                                className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded"
                            >
                                Cancel
                            </button>
                            <button
                                onClick={handleDeleteUser}
                                className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
                            >
                                Delete User
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default UserManagement;
