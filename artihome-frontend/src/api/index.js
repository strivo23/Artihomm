import axios from 'axios';

const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const API = axios.create({
  baseURL
});

API.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

API.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refresh = localStorage.getItem('refresh_token');
        if (!refresh) throw new Error('No refresh token');
        
        const res = await axios.post(`${baseURL}/accounts/token/refresh/`, { refresh });
        localStorage.setItem('access_token', res.data.access);
        
        // Retry original request
        originalRequest.headers.Authorization = `Bearer ${res.data.access}`;
        return axios(originalRequest);
      } catch (err) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
        return Promise.reject(err);
      }
    }
    return Promise.reject(error);
  }
);

export const register      = (data)       => API.post('/accounts/register/', data);
export const login         = (data)       => API.post('/accounts/login/', data);
export const logout        = ()           => API.post('/accounts/logout/');
export const getProducts   = (category)   => API.get('/products/', { params: category && category !== 'All' ? { category } : {} });
export const getProduct    = (id)         => API.get(`/products/${id}/`);
export const joinWaitlist  = (productId, data) => API.post(`/waitlist/join/${productId}/`, data);
export const togglePledge  = (productId)       => API.post(`/waitlist/pledge/${productId}/`);
export const getMyWaitlist = ()                => API.get('/waitlist/my/');
export const getPledgeCount= (productId)       => API.get(`/waitlist/count/${productId}/`);

export default API;
