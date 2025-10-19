import { Button } from "@cloudscape-design/components";
import { useNavigate } from "react-router-dom";

const HomePage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div style={{ width: "100%", background: "#fff" }}>
      {/* Hero Section */}
      <section
        style={{
          background: "linear-gradient(135deg, #0073bb 0%, #037f0c 100%)",
          color: "white",
          padding: "120px 20px 100px",
          textAlign: "center",
        }}
      >
        <div style={{ maxWidth: "900px", margin: "0 auto" }}>
          <h1
            style={{
              fontSize: "3.5rem",
              fontWeight: "700",
              marginBottom: "24px",
              lineHeight: "1.2",
            }}
          >
            Measure the Real Impact of AI on Development
          </h1>
          <p
            style={{
              fontSize: "1.5rem",
              marginBottom: "40px",
              opacity: 0.95,
              lineHeight: "1.6",
            }}
          >
            Quantify how generative AI tools like GitHub Copilot affect your team's productivity with data-driven insights from real repositories.
          </p>
          <div style={{ display: "flex", gap: "16px", justifyContent: "center" }}>
            <Button
              variant="primary"
              onClick={() => navigate("/user-register")}
              iconAlign="right"
            >
              Get Started Free
            </Button>
            <Button
              variant="normal"
              onClick={() => navigate("/user-login")}
            >
              Sign In
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section style={{ padding: "80px 20px", background: "#f9fafb" }}>
        <div style={{ maxWidth: "1200px", margin: "0 auto" }}>
          <div style={{ textAlign: "center", marginBottom: "60px" }}>
            <h2
              style={{
                fontSize: "2.5rem",
                fontWeight: "600",
                color: "#0073bb",
                marginBottom: "16px",
              }}
            >
              Powerful Analytics for AI-Assisted Development
            </h2>
            <p style={{ fontSize: "1.2rem", color: "#6c757d", maxWidth: "700px", margin: "0 auto" }}>
              Track, measure, and visualize the productivity gains from AI coding assistants
            </p>
          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
              gap: "40px",
            }}
          >
            <div style={{ textAlign: "center", padding: "30px" }}>
              <div
                style={{
                  width: "80px",
                  height: "80px",
                  background: "linear-gradient(135deg, #0073bb, #037f0c)",
                  borderRadius: "50%",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  margin: "0 auto 24px",
                  fontSize: "2rem",
                }}
              >
                📊
              </div>
              <h3 style={{ fontSize: "1.5rem", color: "#111", marginBottom: "12px" }}>
                Repository Analytics
              </h3>
              <p style={{ color: "#6c757d", lineHeight: "1.6" }}>
                Analyze lines of code, commit patterns, and contribution metrics from your Git repositories to understand development velocity.
              </p>
            </div>

            <div style={{ textAlign: "center", padding: "30px" }}>
              <div
                style={{
                  width: "80px",
                  height: "80px",
                  background: "linear-gradient(135deg, #0073bb, #037f0c)",
                  borderRadius: "50%",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  margin: "0 auto 24px",
                  fontSize: "2rem",
                }}
              >
                🤖
              </div>
              <h3 style={{ fontSize: "1.5rem", color: "#111", marginBottom: "12px" }}>
                Copilot Usage Tracking
              </h3>
              <p style={{ color: "#6c757d", lineHeight: "1.6" }}>
                Upload and track GitHub Copilot metrics to correlate AI assistance with productivity improvements across your team.
              </p>
            </div>

            <div style={{ textAlign: "center", padding: "30px" }}>
              <div
                style={{
                  width: "80px",
                  height: "80px",
                  background: "linear-gradient(135deg, #0073bb, #037f0c)",
                  borderRadius: "50%",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  margin: "0 auto 24px",
                  fontSize: "2rem",
                }}
              >
                📈
              </div>
              <h3 style={{ fontSize: "1.5rem", color: "#111", marginBottom: "12px" }}>
                Visual Reports
              </h3>
              <p style={{ color: "#6c757d", lineHeight: "1.6" }}>
                Generate interactive charts and statistical correlations to visualize performance trends over time with and without AI.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section style={{ padding: "80px 20px", background: "#fff" }}>
        <div style={{ maxWidth: "1000px", margin: "0 auto" }}>
          <div style={{ textAlign: "center", marginBottom: "60px" }}>
            <h2
              style={{
                fontSize: "2.5rem",
                fontWeight: "600",
                color: "#0073bb",
                marginBottom: "16px",
              }}
            >
              How It Works
            </h2>
            <p style={{ fontSize: "1.2rem", color: "#6c757d" }}>
              Three simple steps to start measuring AI's impact on your development workflow
            </p>
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: "40px" }}>
            <div style={{ display: "flex", gap: "30px", alignItems: "flex-start" }}>
              <div
                style={{
                  width: "60px",
                  height: "60px",
                  background: "#0073bb",
                  color: "white",
                  borderRadius: "50%",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: "1.5rem",
                  fontWeight: "700",
                  flexShrink: 0,
                }}
              >
                1
              </div>
              <div>
                <h3 style={{ fontSize: "1.8rem", color: "#111", marginBottom: "12px" }}>
                  🔐 Register & Connect
                </h3>
                <p style={{ color: "#6c757d", fontSize: "1.1rem", lineHeight: "1.7" }}>
                  Create your account and prepare your repository data. We provide a Python script to extract commit metrics from your Git repositories.
                </p>
              </div>
            </div>

            <div style={{ display: "flex", gap: "30px", alignItems: "flex-start" }}>
              <div
                style={{
                  width: "60px",
                  height: "60px",
                  background: "#037f0c",
                  color: "white",
                  borderRadius: "50%",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: "1.5rem",
                  fontWeight: "700",
                  flexShrink: 0,
                }}
              >
                2
              </div>
              <div>
                <h3 style={{ fontSize: "1.8rem", color: "#111", marginBottom: "12px" }}>
                  📤 Upload Your Metrics
                </h3>
                <p style={{ color: "#6c757d", fontSize: "1.1rem", lineHeight: "1.7" }}>
                  Navigate to the Upload Metrics tab and submit your Copilot usage data and commit metrics. We'll process the data and prepare it for analysis.
                </p>
              </div>
            </div>

            <div style={{ display: "flex", gap: "30px", alignItems: "flex-start" }}>
              <div
                style={{
                  width: "60px",
                  height: "60px",
                  background: "#0073bb",
                  color: "white",
                  borderRadius: "50%",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: "1.5rem",
                  fontWeight: "700",
                  flexShrink: 0,
                }}
              >
                3
              </div>
              <div>
                <h3 style={{ fontSize: "1.8rem", color: "#111", marginBottom: "12px" }}>
                  🎯 Analyze & Optimize
                </h3>
                <p style={{ color: "#6c757d", fontSize: "1.1rem", lineHeight: "1.7" }}>
                  Explore interactive dashboards showing productivity trends, language analytics, and Copilot impact. Make data-driven decisions about AI tooling.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section style={{ padding: "80px 20px", background: "#f9fafb" }}>
        <div style={{ maxWidth: "1000px", margin: "0 auto" }}>
          <div style={{ textAlign: "center", marginBottom: "40px" }}>
            <h2
              style={{
                fontSize: "2.5rem",
                fontWeight: "600",
                color: "#0073bb",
                marginBottom: "16px",
              }}
            >
              About the Project
            </h2>
          </div>

          <div style={{ background: "white", padding: "40px", borderRadius: "8px", marginBottom: "40px" }}>
            <h3 style={{ fontSize: "1.5rem", color: "#037f0c", marginBottom: "16px" }}>
              🎓 Academic Research
            </h3>
            <p style={{ color: "#6c757d", fontSize: "1.1rem", lineHeight: "1.7", marginBottom: "20px" }}>
              CanAiCode is a final-year research project developed as part of the Computer Engineering program at the <strong>University of São Paulo – Escola Politécnica</strong>, class of 2021.
            </p>
            <p style={{ color: "#6c757d", fontSize: "1.1rem", lineHeight: "1.7" }}>
              Our mission is to provide empirical evidence on how generative AI tools affect software engineering productivity, helping teams make informed decisions about adopting and optimizing AI-assisted development workflows.
            </p>
          </div>

          <div style={{ background: "white", padding: "40px", borderRadius: "8px" }}>
            <h3 style={{ fontSize: "1.5rem", color: "#037f0c", marginBottom: "20px" }}>
              👥 The Team
            </h3>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))", gap: "30px" }}>
              <div>
                <h4 style={{ color: "#111", fontSize: "1.2rem", marginBottom: "8px" }}>Creators</h4>
                <p style={{ color: "#6c757d", lineHeight: "1.6" }}>
                  João<br />
                  Carlos<br />
                  Henrique
                </p>
              </div>
              <div>
                <h4 style={{ color: "#111", fontSize: "1.2rem", marginBottom: "8px" }}>Advisors</h4>
                <p style={{ color: "#6c757d", lineHeight: "1.6" }}>
                  Levy<br />
                  João
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section
        style={{
          background: "linear-gradient(135deg, #037f0c 0%, #0073bb 100%)",
          color: "white",
          padding: "80px 20px",
          textAlign: "center",
        }}
      >
        <div style={{ maxWidth: "800px", margin: "0 auto" }}>
          <h2
            style={{
              fontSize: "2.5rem",
              fontWeight: "600",
              marginBottom: "20px",
            }}
          >
            Ready to Measure AI's Impact?
          </h2>
          <p style={{ fontSize: "1.3rem", marginBottom: "40px", opacity: 0.95 }}>
            Start tracking your development productivity with AI-powered analytics today.
          </p>
          <Button
            variant="primary"
            onClick={() => navigate("/user-register")}
          >
            Create Your Free Account
          </Button>
        </div>
      </section>
    </div>
  );
};

export default HomePage;