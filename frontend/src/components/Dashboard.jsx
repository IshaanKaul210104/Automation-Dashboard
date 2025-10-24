import React from "react";
import RunButton from "./RunButton";

export default function Dashboard() {
  return (
    <div className="p-6 space-y-6 text-center">
      <h1 className="text-3xl font-bold mb-6">Automation Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Enable input for scraper */}
        <RunButton scriptName="scraper" label="Run Web Scraper" hasInput={true} />
        <RunButton scriptName="organizer" label="Organize Files" />
        <RunButton scriptName="github_fetcher" label="Fetch GitHub Stats" />
      </div>
    </div>
  );
}