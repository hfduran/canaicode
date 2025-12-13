import React, { useState } from "react";
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
import { pearsonCorrCalculator } from "../tools/pearsonCorrelationCalculator";
import CommitMetricsChart from "./charts/CommitMetricsChart";
import CodeLinesChart from "./charts/CodeLinesChart";
import PearsonCorrelationDisplay from "./PearsonCorrelationDisplay";

const CalculatedMetricsDashboard: React.FC = () => {
  // Initialize dates with 6 months ago to today
  const getDefaultDates = () => {
    const today = new Date();
    const sixMonthsAgo = new Date();
    sixMonthsAgo.setMonth(today.getMonth() - 6);

    return {
      initial: sixMonthsAgo.toISOString().split('T')[0],
      final: today.toISOString().split('T')[0]
    };
  };

  const defaultDates = getDefaultDates();
  const [timeRange, setTimeRange] = useState<string>("");
  const [metric, setMetric] = useState<string>("");
  const [initialDate, setInitialDate] = useState<string>(defaultDates.initial);
  const [finalDate, setFinalDate] = useState<string>(defaultDates.final);
  const [programmingLanguages, setProgrammingLanguages] = useState<string[]>([]);
  const [filteredData, setFilteredData] = useState<FlattenedDataEntry[]>([]);
  const [isFiltersModalVisible, setIsFiltersModalVisible] = useState<boolean>(false);

  const { requestData, isLoading, error, handleRequestData } = useCalculatedMetrics();

  const formattedData: FormattedDataEntry[] = filteredData.map((entry) => ({
    ...entry,
    initial_date: formatDate(entry.initial_date),
    final_date: formatDate(entry.final_date),
    net_changed_lines_without_copilot: (entry.net_changed_lines || 0) - (entry.net_changed_lines_by_copilot || 0),
  }));

  // Debug logging
  if (formattedData.length > 0) {
    console.log("formattedData sample:", formattedData[0]);
    console.log("Has total_commits?", 'total_commits' in formattedData[0]);
    console.log("percentage_changed_lines_by_copilot:", formattedData[0].percentage_changed_lines_by_copilot);
  }

  const pearsonCorr = pearsonCorrCalculator(formattedData);

  const isFormValid = timeRange && metric && initialDate && finalDate; // programmingLanguages is optional

  const handleSubmitRequest = async () => {
    if (!isFormValid) {
      return;
    }

    await handleRequestData({
      timeRange,
      metric,
      initialDate,
      finalDate,
      programmingLanguages,
    });
  };

  // Calculate summary metrics
  const isCommitsMetric = formattedData.length > 0 && 'total_commits' in formattedData[0];

  const totalLines = formattedData.reduce((acc, entry) => acc + (entry.net_changed_lines || 0), 0);
  const totalCopilotLines = formattedData.reduce(
    (acc, entry) => acc + (entry.net_changed_lines_by_copilot || 0),
    0
  );
  const copilotPercentage =
    totalLines > 0 ? ((totalCopilotLines / totalLines) * 100).toFixed(1) : "0";

  // For Commits metric
  const totalCommits = formattedData.reduce((acc, entry) => acc + ((entry as any).total_commits || 0), 0);
  const avgCopilotIntensityValue = formattedData.length > 0
    ? formattedData.reduce((acc, entry) => {
        const value = entry.percentage_changed_lines_by_copilot;
        return acc + (typeof value === 'number' && !isNaN(value) ? value : 0);
      }, 0) / formattedData.length * 100
    : 0;
  const avgCopilotIntensity = !isNaN(avgCopilotIntensityValue) ? avgCopilotIntensityValue.toFixed(1) : "0";

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
    <div style={{ marginBottom: '25px' }}>
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
                    <Box variant="h1">
                      {isCommitsMetric ? totalCommits.toLocaleString() : totalLines.toLocaleString()}
                    </Box>
                    <Box variant="strong">
                      {isCommitsMetric ? "Total Commits" : "Total Lines Added"}
                    </Box>
                    <Box variant="small">Across all analyzed period</Box>
                  </SpaceBetween>
                </Box>
              </Container>

              <Container>
                <Box textAlign="center" padding="l">
                  <SpaceBetween direction="vertical" size="xs">
                    <Box variant="h1">
                      {isCommitsMetric ? totalLines.toLocaleString() : totalCopilotLines.toLocaleString()}
                    </Box>
                    <Box variant="strong">
                      {isCommitsMetric ? "Total Lines Changed" : "Copilot Generated Lines"}
                    </Box>
                    <Box variant="small">
                      {isCommitsMetric ? "Across all commits" : "AI-assisted code contributions"}
                    </Box>
                  </SpaceBetween>
                </Box>
              </Container>

              <Container>
                <Box textAlign="center" padding="l">
                  <SpaceBetween direction="vertical" size="xs">
                    <Box variant="h1">
                      {isCommitsMetric ? `${avgCopilotIntensity}%` : `${copilotPercentage}%`}
                    </Box>
                    <Box variant="strong">
                      {isCommitsMetric ? "Avg Copilot Intensity" : "Copilot Contribution Rate"}
                    </Box>
                    <Box variant="small">
                      {isCommitsMetric ? "Average intensity across periods" : "Percentage of AI-generated code"}
                    </Box>
                  </SpaceBetween>
                </Box>
              </Container>
            </Grid>
          )}

          {/* Data showing Section */}
          {formattedData.length > 0 && (
            <div style={{ display: "flex", justifyContent: "center", alignItems: "stretch", flexGrow: 1 }}>
              <Grid gridDefinition={[{ colspan: 8 }, { colspan: 4 }]}>
                {/* Bar Charts Section */}
                <Container
                  header={
                    <Header
                      variant="h2"
                      description={
                        isCommitsMetric
                          ? "Commit count and Copilot usage intensity over time"
                          : "Visual representation of code contribution metrics over time"
                      }
                      actions={<Badge color="blue">{formattedData.length} data points</Badge>}
                    >
                      {isCommitsMetric ? "Commit Analytics" : "Code Contribution Analytics"}
                    </Header>
                  }
                >
                  {isCommitsMetric ? (
                    <CommitMetricsChart
                      data={formattedData}
                      width={chartDimensions.width}
                      height={chartDimensions.height}
                    />
                  ) : (
                    <CodeLinesChart
                      data={formattedData}
                      width={chartDimensions.width}
                      height={chartDimensions.height}
                    />
                  )}
                  <Box margin={{ top: "xs" }}>
                    <Box
                      variant="small"
                      color="text-body-secondary"
                      textAlign="left"
                    >
                      <span style={{ fontStyle: "italic", fontSize: "0.85em" }}>
                        P.S. Copilot changed lines reflect taken suggestions from Copilot – it is possible for these numbers to be inflated, for instance, if a method is rewritten multiple times over a long period of time.
                      </span>
                    </Box>
                  </Box>
                </Container>

                <Container
                  header={
                    <Header
                      variant="h2"
                      description="Statistical relationship between metrics"
                    >
                      Pearson Correlation Analysis
                    </Header>
                  }
                >
                  <PearsonCorrelationDisplay
                    correlationValue={pearsonCorr}
                    isCommitsMetric={isCommitsMetric}
                  />
                </Container>
              </Grid>
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
    </div>
  );
};

export default CalculatedMetricsDashboard;
