import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import TopNavigation from "@cloudscape-design/components/top-navigation";
import Dashboard from "./components/Dashboard";
import UploadMetrics from "./pages/UploadMetrics";
import LanguageAnalytics from "./pages/LanguageAnalytics";
import CopilotAnalytics from "./pages/CopilotAnalytics";
import HomePage from "./HomePage";
import UserLogin from "./pages/UserLogin";
import UserRegister from "./pages/UserRegister";
import ApiKeys from "./pages/ApiKeys";
import ProtectedRoute from "./components/ProtectedRoute";
import { isAuthenticated, logout } from "./utils/auth";

const Home: React.FC = () => {
  return (
    <HomePage />
  );
};

const UserLoginPage: React.FC = () => {
  return <UserLogin />;
};

const UserRegisterPage: React.FC = () => {
  return <UserRegister />;
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

const AppContent: React.FC = () => {
  const [userLoggedIn, setUserLoggedIn] = useState(isAuthenticated());
  const navigate = useNavigate();

  useEffect(() => {
    const checkAuth = () => {
      setUserLoggedIn(isAuthenticated());
    };
    
    // Check auth status on mount and when localStorage changes
    checkAuth();
    window.addEventListener('storage', checkAuth);
    
    return () => {
      window.removeEventListener('storage', checkAuth);
    };
  }, []);

  const handleLogout = () => {
    logout();
    setUserLoggedIn(false);
    navigate("/user-login");
  };

  const getNavigationUtilities = () => {
    const baseUtilities = [
      {
        type: "button" as const,
        text: "Home",
        href: "/",
      },
    ];

    if (userLoggedIn) {
      return [
        ...baseUtilities,
        {
          type: "button" as const,
          text: "Upload Metrics",
          href: "/upload-metrics",
        },
        {
          type: "button" as const,
          text: "API Keys",
          href: "/api-keys",
        },
        {
          type: "button" as const,
          text: "On Demand Metrics",
          href: "/on-demand-metrics",
        },
        {
          type: "button" as const,
          text: "Reports",
          href: "/reports",
        },
        {
          type: "button" as const,
          text: "Language Analytics",
          href: "/language-analytics",
        },
        {
          type: "button" as const,
          text: "Copilot Analytics",
          href: "/copilot-analytics",
        },
        {
          type: "button" as const,
          text: "Logout",
          onClick: handleLogout,
        },
      ];
    } else {
      return [
        ...baseUtilities,
        {
          type: "button" as const,
          text: "Login",
          href: "/user-login",
        },
        {
          type: "button" as const,
          text: "Register",
          href: "/user-register",
        },
      ];
    }
  };

  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      <div style={{ position: "sticky", top: 0, zIndex: 1000 }}>
        <TopNavigation
          identity={{
            href: "/",
            title: "Canaicode Dashboard",
          }}
          utilities={getNavigationUtilities()}
        />
      </div>

      <div style={{ flex: 1 }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/user-login" element={<UserLoginPage />} />
          <Route path="/user-register" element={<UserRegisterPage />} />
          <Route path="/upload-metrics" element={<ProtectedRoute><UploadMetrics /></ProtectedRoute>} />
          <Route path="/api-keys" element={<ProtectedRoute><ApiKeys /></ProtectedRoute>} />
          <Route path="/on-demand-metrics" element={<ProtectedRoute><OnDemandMetrics /></ProtectedRoute>} />
          <Route path="/reports" element={<ProtectedRoute><Reports /></ProtectedRoute>} />
          <Route path="/language-analytics" element={<ProtectedRoute><LanguageAnalytics /></ProtectedRoute>} />
          <Route path="/copilot-analytics" element={<ProtectedRoute><CopilotAnalytics /></ProtectedRoute>} />
        </Routes>
      </div>

      <Footer />
    </div>
  );
};

const App: React.FC = () => {
  return (
    <Router>
      <AppContent />
    </Router>
  );
};

export default App;
