import React, { useState } from "react";
// import GrossMetricsDashboard from '../components/Dashboard';
import Filters from "../components/Filters";
import mockDashboardData from "../data/mockData";
import { Filters as FiltersType } from "../types/ui";

const GrossMetrics: React.FC = () => {
  const [filters, setFilters] = useState<FiltersType>({
    languages: [],
    teams: [],
    initialDate: "",
    finalDate: "",
    period: "",
    numberOfAuthors: "",
  });

  // Mock data for available options
  const availableLanguages: string[] = Array.from(
    new Set(mockDashboardData.flatMap((item) => item.languages ?? []))
  );
  const availableTeams: string[] = Array.from(new Set(mockDashboardData.map((item) => item.team)));

  return (
    <div>
      <p>This dashboard shows gross metrics of the system...</p>
      <div style={{ display: "flex", gap: "20px", margin: "0 50px" }}>
        {/* <div style={{ flex: 7 }}>
          <Dashboard />
        </div> */}
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
};

export default GrossMetrics;
