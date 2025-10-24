import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

export const runScript = async (scriptName, params = {}) => {
  // Send params directly as the POST body
  const res = await axios.post(`${API_BASE}/run/${scriptName}`, params);
  return res.data;
};