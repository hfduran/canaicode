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
import { pearsonCorrCalculator } from "../tools/pearsonCorrelationCalculator";

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
  const [team, setTeam] = useState<string>("");
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
    net_changed_lines_without_copilot: entry.net_changed_lines - entry.net_changed_lines_by_copilot,
  }));

  const pearsonCorr = pearsonCorrCalculator(formattedData);

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

          {/* Data showing Section */}
          {formattedData.length > 0 && (
            <div style={{ display: "flex", justifyContent: "center", alignItems: "stretch", flexGrow: 1 }}>
              <Grid gridDefinition={[{ colspan: 8 }, { colspan: 4 }]}>
                {/* Bar Charts Section */}
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
                        const total = props.payload.net_changed_lines;
                        let percent = 0;
                        if (name === "Copilot Changed Lines") {
                          percent = total > 0 ? (value / total) * 100 : 0;
                          return [
                            `${value} lines (${percent.toFixed(1)}% of total)`,
                            "Copilot Changed Lines",
                          ];
                        }
                        if (name === "Changed Lines without Copilot") {
                          percent = total > 0 ? (value / total) * 100 : 0;
                          return [
                            `${value} lines (${percent.toFixed(1)}% of total)`,
                            "Changed Lines without Copilot",
                          ];
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
                      name="Changed Lines without Copilot"
                      radius={[4, 4, 0, 0]}
                      stackId="a"
                    />
                    <Bar
                      dataKey="net_changed_lines_by_copilot"
                      fill="#037f0c"
                      name="Copilot Changed Lines"
                      radius={[4, 4, 0, 0]}
                      stackId="a"
                    />
                  </BarChart>
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
                  {!isNaN(pearsonCorr) && (
                    <div style={{ padding: '20px', textAlign: 'center' }}>
                      <p style={{ fontSize: '1.0em', color: '#6c757d', textAlign: 'left' }}>
                        Pearson Correlation between
                        <br />- <i>Total Changed Lines</i>
                        <br />- <i>Copilot Changed Lines</i>
                      </p>

                      {/* Visual Bar and Number Section */}
                      <div style={{ position: 'relative', width: '100%', margin: '15px 0' }}>
                        {/* Bar container */}
                        <div style={{
                          height: '10px',
                          width: '100%',
                          backgroundColor: '#e9ecef',
                          borderRadius: '5px'
                        }} />

                        {/* Filled bar */}
                        {pearsonCorr !== null && (
                          <>
                            <div style={{
                              position: 'absolute',
                              top: 0,
                              left: 0,
                              height: '100%',
                              width: `${Math.max(0, Math.min(1, pearsonCorr)) * 100}%`,
                              backgroundColor: '#0073bb',
                              borderRadius: '5px',
                            }} />

                            {/* Number on the bar */}
                            <span style={{
                              position: 'absolute',
                              top: '-25px',
                              left: `${Math.max(0, Math.min(1, pearsonCorr)) * 100}%`,
                              transform: 'translateX(-50%)',
                              fontSize: '1.2em',
                              fontWeight: 'bold',
                              color: '#0073bb',
                            }}>
                              {pearsonCorr.toFixed(2)}
                            </span>
                          </>
                        )}
                      </div>

                      {/* Legend */}
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '10px', fontSize: '0.8em', color: '#0073bb' }}>
                        <p style={{ margin: 0 }}>
                          Weaker correlation
                        </p>
                        <p style={{ margin: 0 }}>
                          Stronger correlation
                        </p>
                      </div>

                      <p style={{ fontSize: '0.7em', color: '#6c757d', textAlign: 'left', marginTop: '20px' }}>
                        (A value closer to 1 indicates a strong positive linear relationship)
                      </p>
                    </div>
                  )}
                  {isNaN(pearsonCorr) && (
                    <div style={{ padding: '20px', textAlign: 'center' }}>
                      <p style={{ fontSize: '1.0em', color: '#6c757d' }}>
                        Sorry! No Pearson Correlation for commit metrics.
                      </p>
                    </div>
                  )}
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
