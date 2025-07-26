import { Grid, Container, Header } from "@cloudscape-design/components";

const HomePage: React.FC = () => {
  return (
    <div style={{ width: "80%", margin: "0 auto", padding: "20px" }}>
      <Header variant="h1">
        <span style={{ color: "#0073bb" }}>Welcome to Canaicode</span>
      </Header>
      <p style={{ color: "#6c757d", marginBottom: "40px" }}>
        CanAiCode is a research project focused on understanding the impact of generative AI tools on software development productivity.
        It investigates whether developers become more efficient when assisted by tools like GitHub Copilot — and by how much.
      </p>

      <Grid gridDefinition={[{ colspan: 4 }, { colspan: 4 }, { colspan: 4 }]} disableGutters={false}>
        <Container
          header={
            <Header variant="h2" description="Institutional and academic background">
              <span style={{ color: "#037f0c" }}>About the Project</span>
            </Header>
          }
        >
          <p style={{ color: "#6c757d" }}>
            This is a final-year research project (TCC – <i>Trabalho de Conclusão de Curso</i>) developed as part of the Computer Engineering program
            at the <strong>University of São Paulo – Escola Politécnica</strong>, class of 2021.
          </p>
        </Container>

        <Container
          header={
            <Header variant="h2" description="Primary research objective and motivation">
              <span style={{ color: "#037f0c" }}>Main Goal</span>
            </Header>
          }
        >
          <p style={{ color: "#6c757d" }}>
            To quantify and analyze how generative AI tools influence software engineering productivity by tracking key metrics from real-world repositories.
          </p>
        </Container>

        <Container
          header={
            <Header variant="h2" description="Approach and methodology used to measure impact">
              <span style={{ color: "#037f0c" }}>How It Works</span>
            </Header>
          }
        >
          <p style={{ color: "#6c757d" }}>
            We collect contribution data (such as lines of code, authorship, and Copilot usage) from Git repositories and compute analytics — including
            charts and statistical correlations — to evaluate developer performance over time with and without AI assistance.
          </p>
        </Container>
      </Grid>

      <Header variant="h3">
        <span style={{ color: "#0073bb" }}>Team</span>
      </Header>
      <p style={{ color: "#6c757d", marginBottom: "40px" }}>
        <strong>Creators:</strong> João, Carlos, Henrique
        <br />
        <strong>Advisors:</strong> Levy and João
      </p>

    </div>
  );
};

export default HomePage;