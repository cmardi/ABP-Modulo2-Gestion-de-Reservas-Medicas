import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/', // Ajusta si usas otro path
});

export default api;
