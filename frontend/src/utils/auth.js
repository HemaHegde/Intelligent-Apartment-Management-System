/**
 * Authentication Utility Functions
 * Token management and user info storage
 */

const TOKEN_KEY = 'apartment_auth_token';
const USER_KEY = 'apartment_user_info';

// Token management
export const getToken = () => {
    return localStorage.getItem(TOKEN_KEY);
};

export const setToken = (token) => {
    localStorage.setItem(TOKEN_KEY, token);
};

export const removeToken = () => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
};

// User info management
export const getUserInfo = () => {
    const userStr = localStorage.getItem(USER_KEY);
    return userStr ? JSON.parse(userStr) : null;
};

export const setUserInfo = (user) => {
    localStorage.setItem(USER_KEY, JSON.stringify(user));
};

export const getUserRole = () => {
    const user = getUserInfo();
    return user?.role || null;
};

export const isAuthenticated = () => {
    return !!getToken();
};

export const logoutUser = () => {
    removeToken();
    window.location.href = '/login';
};
