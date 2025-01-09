import axios from 'axios';
import { SystemMetrics } from '../types/types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_URL,
});

export const simulatorApi = {
  startSimulation: () => api.post('/simulation/start'),
  stopSimulation: () => api.post('/simulation/stop'),
  getMetrics: () => api.get<SystemMetrics>('/metrics'),
  generateReport: () => api.post('/report/generate'),
  getLogs: () => api.get<string[]>('/logs'),
};