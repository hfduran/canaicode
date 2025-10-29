import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, useNavigate, useLocation } from "react-router-dom";
import AppLayout from "@cloudscape-design/components/app-layout";
import SideNavigation from "@cloudscape-design/components/side-navigation";
import ContentLayout from "@cloudscape-design/components/content-layout";
import TopNavigation from "@cloudscape-design/components/top-navigation";
import Dashboard from "./components/Dashboard";
import UploadMetrics from "./pages/UploadMetrics";
import LanguageAnalytics from "./pages/LanguageAnalytics";
import CopilotAnalytics from "./pages/CopilotAnalytics";
import HomePage from "./HomePage";
import UserLogin from "./pages/UserLogin";
import UserRegister from "./pages/UserRegister";
import GitHubApp from "./pages/GitHubApp";
import ApiKeys from "./pages/ApiKeys";
import ProtectedRoute from "./components/ProtectedRoute";
import { isAuthenticated, logout, getUsername } from "./utils/auth";

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

const GitHubAppPage: React.FC = () => {
  return <GitHubApp />;
}

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

const AppContent: React.FC = () => {
  const [userLoggedIn, setUserLoggedIn] = useState(isAuthenticated());
  const [navigationOpen, setNavigationOpen] = useState(true);
  const navigate = useNavigate();
  const location = useLocation();

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

  useEffect(() => {
    // Redirect logged-in users from home to on-demand-metrics
    if (userLoggedIn && location.pathname === '/') {
      navigate('/on-demand-metrics');
    }
  }, [userLoggedIn, location.pathname, navigate]);

  const handleLogout = () => {
    logout();
    setUserLoggedIn(false);
    navigate("/user-login");
  };

  const getNavigationItems = () => {
    if (userLoggedIn) {
      return [
        {
          type: "section" as const,
          text: "Administration",
          items: [
            {
              type: "link" as const,
              text: "Upload Metrics",
              href: "/upload-metrics",
            },
            {
              type: "link" as const,
              text: "API Keys",
              href: "/api-keys",
            },
            {
              type: "link" as const,
              text: "GitHub App",
              href: "/github-app",
            },
            {
              type: "link" as const,
              text: "Reports",
              href: "/reports",
            },
          ],
        },
        {
          type: "section" as const,
          text: "Analytics",
          items: [
            {
              type: "link" as const,
              text: "On Demand Metrics",
              href: "/on-demand-metrics",
            },
            {
              type: "link" as const,
              text: "Language Analytics",
              href: "/language-analytics",
            },
            {
              type: "link" as const,
              text: "Copilot Analytics",
              href: "/copilot-analytics",
            },
          ],
        },
      ];
    } else {
      return [
        {
          type: "link" as const,
          text: "Home",
          href: "/",
        },
        {
          type: "divider" as const,
        },
        {
          type: "link" as const,
          text: "Login",
          href: "/user-login",
        },
        {
          type: "link" as const,
          text: "Register",
          href: "/user-register",
        },
      ];
    }
  };

  const getTopNavigationUtilities = () => {
    if (userLoggedIn) {
      const username = getUsername() || "User";
      return [
        {
          type: "menu-dropdown" as const,
          text: username,
          iconName: "user-profile" as const,
          items: [
            {
              id: "logout",
              text: "Logout",
            },
          ],
          onItemClick: ({ detail }: { detail: { id: string } }) => {
            if (detail.id === "logout") {
              handleLogout();
            }
          },
        },
      ];
    }
    return [];
  };

  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      <div style={{ position: "sticky", top: 0, zIndex: 1000 }}>
        <TopNavigation
          identity={{
            href: userLoggedIn ? "/on-demand-metrics" : "/",
            title: "Canaicode",
          }}
          utilities={getTopNavigationUtilities()}
        />
      </div>

      <AppLayout
        navigation={
          <SideNavigation
            activeHref={location.pathname}
            header={{
              href: userLoggedIn ? "/on-demand-metrics" : "/",
              text: "Navigation",
            }}
            items={getNavigationItems()}
            onFollow={(event) => {
              if (!event.detail.external) {
                event.preventDefault();
                navigate(event.detail.href);
              }
            }}
          />
        }
        navigationOpen={navigationOpen}
        onNavigationChange={({ detail }) => setNavigationOpen(detail.open)}
        content={
          <ContentLayout>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/user-login" element={<UserLoginPage />} />
              <Route path="/user-register" element={<UserRegisterPage />} />
              <Route path="/upload-metrics" element={<ProtectedRoute><UploadMetrics /></ProtectedRoute>} />
              <Route path="/api-keys" element={<ProtectedRoute><ApiKeys /></ProtectedRoute>} />
              <Route path="/on-demand-metrics" element={<ProtectedRoute><OnDemandMetrics /></ProtectedRoute>} />
              <Route path="/github-app" element={<ProtectedRoute><GitHubAppPage /></ProtectedRoute>} />
              <Route path="/reports" element={<ProtectedRoute><Reports /></ProtectedRoute>} />
              <Route path="/language-analytics" element={<ProtectedRoute><LanguageAnalytics /></ProtectedRoute>} />
              <Route path="/copilot-analytics" element={<ProtectedRoute><CopilotAnalytics /></ProtectedRoute>} />
            </Routes>
          </ContentLayout>
        }
        toolsHide
      />
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
