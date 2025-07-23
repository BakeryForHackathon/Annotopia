import axios from 'axios';

/**
 * Creates a configured instance of Axios.
 * The baseURL is set to the absolute path of the backend API for development.
 */
const api = axios.create({
  baseURL: 'http://127.0.0.1:5001/api', // FIX: Reverted to absolute path for development
  withCredentials: true,
});

// Interceptor to add the auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

export default api;