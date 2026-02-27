import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export async function assessCreditRisk(applicationData, onProgress) {
  try {
    const response = await api.post('/assess', {
      application: applicationData,
      fast_mode: false,
      include_detailed_report: true,
    });

    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data?.detail?.error || 'Assessment failed');
    }
    throw new Error('Network error. Please check your connection.');
  }
}

export async function validateApplication(applicationData) {
  try {
    const response = await api.post('/validate', applicationData);
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data?.detail?.error || 'Validation failed');
    }
    throw new Error('Network error');
  }
}

export async function getHealthStatus() {
  try {
    const response = await axios.get('/health');
    return response.data;
  } catch (error) {
    return { status: 'unhealthy' };
  }
}

export default api;
