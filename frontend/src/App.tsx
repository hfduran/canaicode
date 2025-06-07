import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import TopNavigation from "@cloudscape-design/components/top-navigation";
import Dashboard from "./components/Dashboard";

const Home: React.FC = () => {
  return (
    <div style={{ display: "flex" }}>
      <div style={{ flex: 1 }}>
        <p>Welcome to the Home Page - Column 1</p>
      </div>
      <div style={{ flex: 1 }}>
        <p>Column 2 content here</p>
      </div>
    </div>
  );
};

const GrossMetrics: React.FC = () => {
  return <Dashboard />;
};

const CalculatedMetrics: React.FC = () => {
  return <Dashboard />;
};

const Footer: React.FC = () => {
  return (
    <footer
      style={{
        display: "flex",
        justifyContent: "space-around",
        padding: "20px",
        background: "#eee",
      }}
    >
      <div>Column 1</div>
      <div>Column 2</div>
      <div>Column 3</div>
    </footer>
  );
};

const App: React.FC = () => {
  return (
    <Router>
      <div>
        <TopNavigation
          identity={{
            href: "/",
            title: "Canaicode Dashboard",
          }}
          utilities={[
            {
              type: "button",
              text: "Home",
              href: "/",
            },
            {
              type: "button", 
              text: "Gross Metrics",
              href: "/gross-metrics",
            },
            {
              type: "button",
              text: "Calculated Metrics", 
              href: "/calculated-metrics",
            },
          ]}
        />

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/gross-metrics" element={<GrossMetrics />} />
          <Route path="/calculated-metrics" element={<CalculatedMetrics />} />
        </Routes>

        <Footer />
      </div>
    </Router>
  );
};

export default App;
