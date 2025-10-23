import React, { useState } from "react";
import { runScript } from "../api/api";

export default function RunButton({ scriptName, label }) {
  const [status, setStatus] = useState("");

  const handleClick = async () => {
    setStatus("Running...");
    try {
        const res = await runScript(scriptName);
        setStatus(`✅ ${label} started: ${res.data.status}`);
    } catch (err) {
        setStatus(`❌ ${label} failed`);
        console.error(err);
    }
    };

  return (
    <div className="flex flex-col items-center">
      <button
        onClick={handleClick}
        className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
      >
        {label}
      </button>
      {status && <p className="mt-2 text-sm text-gray-700">{status}</p>}
    </div>
  );
}