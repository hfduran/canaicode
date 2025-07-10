import React, { useState } from "react";
import { BarChart, Bar, CartesianGrid, XAxis, YAxis, Tooltip, Legend } from "recharts";
import RequestParamsForm from "./RequestParamsForm";
import { FlattenedDataEntry, FormattedDataEntry } from "../types/ui";
import {
  Button,
  SpaceBetween,
  Container,
  Header,
  ContentLayout,
  Box,
  Alert,
  Badge,
  Grid,
} from "@cloudscape-design/components";
import { DashboardFiltersModal } from "./DashboardFiltersModal";
import { formatDate } from "../utils/date/formatDate";
import { useCalculatedMetrics } from "../hooks";

const CalculatedMetricsDashboard: React.FC = () => {
  const [timeRange, setTimeRange] = useState<string>("");
  const [team, setTeam] = useState<string>("");
  const [metric, setMetric] = useState<string>("");
  const [initialDate, setInitialDate] = useState<string>("");
  const [finalDate, setFinalDate] = useState<string>("");
  const [programmingLanguages, setProgrammingLanguages] = useState<string[]>([]);
  const [filteredData, setFilteredData] = useState<FlattenedDataEntry[]>([]);
  const [isFiltersModalVisible, setIsFiltersModalVisible] = useState<boolean>(false);

  const { requestData, isLoading, error, handleRequestData } = useCalculatedMetrics();

  const formattedData: FormattedDataEntry[] = filteredData.map((entry) => ({
    ...entry,
    initial_date: formatDate(entry.initial_date),
    final_date: formatDate(entry.final_date),
    net_changed_lines_without_copilot: entry.net_changed_lines - entry.net_changed_lines_by_copilot,
  }));

  const isFormValid = timeRange && team && metric && initialDate && finalDate; // programmingLanguages is optional

  const handleSubmitRequest = async () => {
    if (!isFormValid) {
      return;
    }

    await handleRequestData({
      timeRange,
      team,
      metric,
      initialDate,
      finalDate,
      programmingLanguages,
    });
  };

  const handleOpenFiltersModal = () => {
    setIsFiltersModalVisible(true);
  };

  // Calculate summary metrics
  const totalLines = formattedData.reduce((acc, entry) => acc + (entry.net_changed_lines || 0), 0);
  const totalCopilotLines = formattedData.reduce(
    (acc, entry) => acc + (entry.net_changed_lines_by_copilot || 0),
    0
  );
  const copilotPercentage =
    totalLines > 0 ? ((totalCopilotLines / totalLines) * 100).toFixed(1) : "0";

  // Responsive chart dimensions
  const getChartDimensions = () => {
    const width = Math.min(window.innerWidth - 100, 800);
    const height = Math.max(width * 0.5, 340);
    return { width, height };
  };

  const [chartDimensions, setChartDimensions] = React.useState(getChartDimensions());

  React.useEffect(() => {
    const handleResize = () => {
      setChartDimensions(getChartDimensions());
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return (
    <ContentLayout
      header={
        <Header
          variant="h1"
          description="Analyze GitHub Copilot productivity metrics for your development teams"
        >
          GitHub Copilot Analytics Dashboard
        </Header>
      }
      defaultPadding={true}
    >
      <SpaceBetween size="l">
        {/* Configuration Section */}
        <Container
          header={
            <Header variant="h2" description="Configure your analysis parameters">
              Data Configuration
            </Header>
          }
        >
          <SpaceBetween size="m">
            <RequestParamsForm
              timeRange={timeRange}
              setTimeRange={setTimeRange}
              team={team}
              setTeam={setTeam}
              metric={metric}
              setMetric={setMetric}
              initialDate={initialDate}
              setInitialDate={setInitialDate}
              finalDate={finalDate}
              setFinalDate={setFinalDate}
              programmingLanguages={programmingLanguages}
              setProgrammingLanguages={setProgrammingLanguages}
            />

            <Box>
              <Button
                variant="primary"
                onClick={handleSubmitRequest}
                loading={isLoading}
                disabled={!isFormValid}
              >
                {isLoading ? "Loading Data..." : "Generate Analytics"}
              </Button>
            </Box>

            {error && (
              <Alert statusIconAriaLabel="Error" type="error" header="Data Loading Error">
                {error}
              </Alert>
            )}

            {!isFormValid && (
              <Alert statusIconAriaLabel="Info" type="info" header="Configuration Required">
                Please fill in all required fields to generate analytics.
              </Alert>
            )}
          </SpaceBetween>
        </Container>

        {/* Summary Cards */}
        {formattedData.length > 0 && (
          <Grid gridDefinition={[{ colspan: 4 }, { colspan: 4 }, { colspan: 4 }]}>
            <Container variant="stacked">
              <Box textAlign="center" padding="l">
                <SpaceBetween direction="vertical" size="xs">
                  <Box variant="h1">{totalLines.toLocaleString()}</Box>
                  <Box variant="strong">Total Lines Added</Box>
                  <Box variant="small">Across all analyzed period</Box>
                </SpaceBetween>
              </Box>
            </Container>

            <Container>
              <Box textAlign="center" padding="l">
                <SpaceBetween direction="vertical" size="xs">
                  <Box variant="h1">{totalCopilotLines.toLocaleString()}</Box>
                  <Box variant="strong">Copilot Generated Lines</Box>
                  <Box variant="small">AI-assisted code contributions</Box>
                </SpaceBetween>
              </Box>
            </Container>

            <Container>
              <Box textAlign="center" padding="l">
                <SpaceBetween direction="vertical" size="xs">
                  <Box variant="h1">{copilotPercentage}%</Box>
                  <Box variant="strong">Copilot Contribution Rate</Box>
                  <Box variant="small">Percentage of AI-generated code</Box>
                </SpaceBetween>
              </Box>
            </Container>
          </Grid>
        )}

        {/* Charts Section */}
        {formattedData.length > 0 && (
          <div style={{ display: "flex", justifyContent: "center", alignItems: "stretch", flexGrow: 1 }}>
            <Container
              header={
                <Header
                  variant="h2"
                  description="Visual representation of code contribution metrics over time"
                  actions={<Badge color="blue">{formattedData.length} data points</Badge>}
                >
                  Code Contribution Analytics
                </Header>
              }
            >
              <BarChart
                width={chartDimensions.width}
                height={chartDimensions.height}
                data={formattedData}
                margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#e9ecef" opacity={0.7} />
                <XAxis
                  dataKey="initial_date"
                  tick={{ fontSize: 12, fill: "#6c757d" }}
                  stroke="#6c757d"
                  tickLine={{ stroke: "#6c757d" }}
                />
                <YAxis
                  tick={{ fontSize: 12, fill: "#6c757d" }}
                  stroke="#6c757d"
                  tickLine={{ stroke: "#6c757d" }}
                />
                <Tooltip
                  formatter={(value: any, name: string, props: any) => {
                    if (name === "copilot") {
                      const percentage = props.payload.percentage_changed_lines_by_copilot;
                      return [`${value} lines (${(percentage * 100).toFixed(1)}%)`, "Copilot Changed Lines"];
                    }
                    if (name === "without_copilot") {
                      const total = props.payload.net_changed_lines;
                      return [`${total} lines`, "Total Changed Lines"];
                    }
                    return [`${value} lines`, name];
                  }}
                  contentStyle={{
                    backgroundColor: "#ffffff",
                    border: "1px solid #e9ecef",
                    borderRadius: "8px",
                    boxShadow: "0 4px 12px rgba(0,0,0,0.15)",
                    fontSize: "14px",
                  }}
                  labelStyle={{ color: "#232f3e", fontWeight: "bold" }}
                />
                <Legend wrapperStyle={{ paddingTop: "20px" }} />
                <Bar
                  dataKey="net_changed_lines_without_copilot"
                  fill="#0073bb"
                  name="without_copilot"
                  stackId={"a"}
                  radius={[4, 4, 0, 0]}
                />
                <Bar
                  dataKey="net_changed_lines_by_copilot"
                  fill="#037f0c"
                  name="copilot"
                  stackId={"a"}
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </Container>
          </div>
        )}

        {/* Loading State */}
        {isLoading && (
          <Container>
            <Box textAlign="center" padding="xxl">
              <SpaceBetween size="m">
                <Box variant="h3">🔄 Loading Analytics...</Box>
                <Box variant="p">
                  Fetching and processing your GitHub Copilot data. This may take a few moments.
                </Box>
              </SpaceBetween>
            </Box>
          </Container>
        )}

        {/* Empty State */}
        {formattedData.length === 0 && !isLoading && (
          <Container>
            <Box textAlign="center" padding="xxl">
              <SpaceBetween size="m">
                <Box variant="h2">📊 Ready to Analyze</Box>
                <Box variant="p">
                  Configure your parameters above and click "Generate Analytics" to view your GitHub
                  Copilot productivity metrics.
                </Box>
                <Box variant="small">
                  You'll see detailed charts and insights about code contributions and AI
                  assistance.
                </Box>
              </SpaceBetween>
            </Box>
          </Container>
        )}

        <DashboardFiltersModal
          data={requestData}
          setFilteredData={setFilteredData}
          visible={isFiltersModalVisible}
          setVisible={setIsFiltersModalVisible}
        />
      </SpaceBetween>
    </ContentLayout>
  );
};

export default CalculatedMetricsDashboard;
