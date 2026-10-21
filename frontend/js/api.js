const API_BASE = '/api';

async function fetchAPI(endpoint, options = {}) {
    const defaultHeaders = {
        'Content-Type': 'application/json',
    };

    const config = {
        ...options,
        headers: {
            ...defaultHeaders,
            ...options.headers,
        },
    };

    try {
        const response = await fetch(`${API_BASE}${endpoint}`, config);
        
        if (response.status === 401) {
            // Handle unauthorized - e.g., redirect to login
            if (window.location.pathname !== '/login.html' && window.location.pathname !== '/') {
                window.location.href = '/login.html';
            }
        }
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || data.message || 'API request failed');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Global user state check
async function checkAuth() {
    try {
        const user = await fetchAPI('/auth/me');
        return user;
    } catch (e) {
        return null;
    }
}
