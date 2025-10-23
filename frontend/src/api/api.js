import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000"; // FastAPI backend

export const testBackend = async () => {
  return await axios.get(`${BASE_URL}/`);
};

export const runScript = async (scriptName, params = {}) => {
  return await axios.post(`${BASE_URL}/run/${scriptName}`, params);
};

export const getJobs = async () => {
  return await axios.get(`${BASE_URL}/jobs`);
};