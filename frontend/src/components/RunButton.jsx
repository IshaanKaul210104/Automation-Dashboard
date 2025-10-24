import React, { useState } from "react";
import { runScript } from "../api/api";

export default function RunButton({ scriptName, label, hasInput = false }) {
  const [status, setStatus] = useState("");
  const [inputValue, setInputValue] = useState("");

  const handleClick = async () => {
    setStatus("Running...");
    try {
      const res = await runScript(
        scriptName,
        hasInput && inputValue ? { url: inputValue } : {}
      );

      // Safely extract count (fallbacks if not present)
      const count =
        res?.output?.count ??
        (Array.isArray(res?.output) ? res.output.length : 0);

      // Show log file link
      const logLink = res.log ? ` | Log: ${res.log}` : "";

      setStatus(`✅ ${label} completed — Items: ${count}${logLink}`);
    } catch (err) {
      console.error(err);
      setStatus(`❌ ${label} failed`);
    }
  };

  return (
    <div className="flex flex-col items-center">
      {hasInput && (
        <input
          type="text"
          placeholder="Enter URL to scrape..."
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          className="border border-gray-300 rounded-md px-3 py-2 mb-2 w-64 text-sm"
        />
      )}
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