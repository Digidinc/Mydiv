import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Handle token refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/auth/refresh`, {
          refresh_token: refreshToken,
        });
        const { token } = response.data;
        localStorage.setItem('auth_token', token);
        originalRequest.headers.Authorization = `Bearer ${token}`;
        return api(originalRequest);
      } catch (error) {
        // Handle refresh token failure
        localStorage.removeItem('auth_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(error);
      }
    }

    return Promise.reject(error);
  }
);

// Birth Chart API
export const birthChartApi = {
  calculate: async (data: {
    date: string;
    time: string;
    latitude: number;
    longitude: number;
    timezone: string;
  }) => {
    const response = await api.post('/birth-chart/calculate', data);
    return response.data;
  },
  getById: async (id: string) => {
    const response = await api.get(`/birth-chart/${id}`);
    return response.data;
  },
  getTransits: async (chartId: string, date: string) => {
    const response = await api.get(`/birth-chart/${chartId}/transits`, {
      params: { date },
    });
    return response.data;
  },
};

// Path of Symbols API
export const symbolsApi = {
  getJourney: async () => {
    const response = await api.get('/symbols/journey');
    return response.data;
  },
  getSymbol: async (id: string) => {
    const response = await api.get(`/symbols/${id}`);
    return response.data;
  },
  saveProgress: async (data: { symbolId: string; response: string }) => {
    const response = await api.post('/symbols/progress', data);
    return response.data;
  },
};

// User Profile API
export const userApi = {
  getProfile: async () => {
    const response = await api.get('/user/profile');
    return response.data;
  },
  updateProfile: async (data: {
    name?: string;
    email?: string;
    birthDate?: string;
    birthTime?: string;
    birthPlace?: string;
  }) => {
    const response = await api.put('/user/profile', data);
    return response.data;
  },
  getCharts: async () => {
    const response = await api.get('/user/charts');
    return response.data;
  },
};

export default api;