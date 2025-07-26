import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import TopNavigation from "@cloudscape-design/components/top-navigation";
import Dashboard from "./components/Dashboard";
import LanguageAnalytics from "./pages/LanguageAnalytics";
import HomePage from "./HomePage";

const Home: React.FC = () => {
  return (
    <HomePage />
  );
};

const OnDemandMetrics: React.FC = () => {
  return <Dashboard />;
};

const Reports: React.FC = () => {
  return (
    <div style={{ flex: 1 }}>
      <p>TO BE DONE</p>
    </div>
  );
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
      <span style={{fontWeight: "bold", color: "#6c757d"}}>
        2025
      </span>
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
              text: "On Demand Metrics",
              href: "/on-demand-metrics",
            },
            {
              type: "button",
              text: "Reports",
              href: "/reports",
            },
            {
              type: "button",
              text: "Language Analytics",
              href: "/language-analytics",
            },
          ]}
        />

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/on-demand-metrics" element={<OnDemandMetrics />} />
          <Route path="/reports" element={<Reports />} />
          <Route path="/language-analytics" element={<LanguageAnalytics />} />
        </Routes>

        <Footer />
      </div>
    </Router>
  );
};

export default App;
