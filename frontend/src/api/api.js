import axios from "axios";

const API_BASE = "http://127.0.0.1:8000"; // backend URL

export const runScript = async (scriptName, params = {}) => {
  const res = await axios.post(`${API_BASE}/run/${scriptName}`, params);
  return res.data;
};