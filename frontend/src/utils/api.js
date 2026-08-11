import axios from 'axios';

const api = axios.create({
  baseURL: '',
});

export const fetchPlayers = async (params) => {
  const cleanParams = {};
  for (const [key, value] of Object.entries(params || {})) {
    if (value !== null && value !== undefined && value !== '') {
      cleanParams[key] = value;
    }
  }
  const response = await api.get('/api/players', { params: cleanParams });
  return response.data;
};

export const fetchFilters = async () => {
  const response = await api.get('/api/players/filters');
  return response.data;
};

export const fetchSummary = async (params) => {
  const cleanParams = {};
  for (const [key, value] of Object.entries(params || {})) {
    if (value !== null && value !== undefined && value !== '') {
      cleanParams[key] = value;
    }
  }
  const response = await api.get('/api/players/summary', { params: cleanParams });
  return response.data;
};

export const fetchPlayerHistory = async (playerId) => {
  const response = await api.get(`/api/players/${playerId}`);
  return response.data;
};
