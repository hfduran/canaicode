// CalculatedMetrics.tsx

import React from "react";
import CalculatedMetricsDashboard from "../components/Dashboard";

const CalculatedMetrics: React.FC = () => {
  return (
    <div>
      <p>This dashboard shows calculated metrics of the system...</p>
      <div style={{ margin: "0 50px" }}>
        <CalculatedMetricsDashboard />
      </div>
    </div>
  );
};

export default CalculatedMetrics;
