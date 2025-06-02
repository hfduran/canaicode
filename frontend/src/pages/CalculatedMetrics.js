// CalculatedMetrics.js

import { useState } from "react";
import CalculatedMetricsDashboard from "../components/Dashboard";
import Filters from "../components/Filters";
import mockDashboardData from "../data/mockData";

function CalculatedMetrics() {
  const [filters, setFilters] = useState({
    languages: [],
    teams: [],
    initialDate: "",
    finalDate: "",
    period: "",
    numberOfAuthors: "",
  });

  // remover abaixo, vai vir do back
  const availableLanguages = Array.from(
    new Set(mockDashboardData.flatMap((item) => item.languages ?? []))
  );

  // remover abaixo, vai vir do back
  const availableTeams = Array.from(new Set(mockDashboardData.map((item) => item.team)));

  return (
    <div>
      <p>This dashboard shows calculated metrics of the system...</p>
      <div style={{ display: "flex", gap: "20px", margin: "0 50px" }}>
        <div style={{ flex: 7 }}>
          <CalculatedMetricsDashboard filters={filters} />
        </div>
        <div style={{ flex: 3 }}>
          <Filters
            filters={filters}
            setFilters={setFilters}
            availableLanguages={availableLanguages}
            availableTeams={availableTeams}
          />
        </div>
      </div>
    </div>
  );
}

export default CalculatedMetrics;