import React, { useEffect, useState } from "react";
import { Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Line, ComposedChart } from "recharts";
import {
  Container,
  Header,
  ContentLayout,
  SpaceBetween,
  Alert,
  Spinner,
  Box,
  Badge,
  Select,
} from "@cloudscape-design/components";
import { useLanguageMetrics } from "../hooks/useLanguageMetrics";
import { CopilotMetricsByLanguage } from "../types/model";

const LanguageAnalytics: React.FC = () => {
  const { languageData, isLoading, error, fetchLanguageMetrics } = useLanguageMetrics();
  const [selectedMetric, setSelectedMetric] = useState<string>("both");
  const [selectedMetricAbsVals, setSelectedMetricAbsVals] = useState<string>("both_abs");

  const metricOptions = [
    { label: "Accepted Suggestions and Accepted Lines", value: "both" },
    { label: "Accepted Suggestions Only", value: "suggestions" },
    { label: "Accepted Lines Only", value: "lines" },
  ];

  const metricOptionsAbsValues = [
    { label: "Code and Lines Suggestions", value: "both_abs" },
    { label: "Code Suggestions", value: "suggestions_abs" },
    { label: "Lines Suggested", value: "lines_abs" },
  ];

  useEffect(() => {
    fetchLanguageMetrics();
  }, [fetchLanguageMetrics]);

  // Chart data interface
  interface ChartDataEntry {
    language: string;
    percentage_accepted_suggestions: number;
    percentage_accepted_lines: number;
    code_acceptances: number;
    code_suggestions: number;
    lines_accepted: number;
    lines_suggested: number;
  }

  // Format data for the chart
  const chartData: ChartDataEntry[] = languageData.map((item: CopilotMetricsByLanguage) => ({
    language: item.language,
    percentage_accepted_suggestions: parseFloat(item.percentage_code_acceptances.toFixed(1)),
    percentage_accepted_lines: parseFloat(item.percentage_lines_accepted.toFixed(1)),
    code_acceptances: item.code_acceptances,
    code_suggestions: item.code_suggestions,
    lines_accepted: item.lines_accepted,
    lines_suggested: item.lines_suggested,
  }));

  console.log("chartData: ", chartData)

  // Calculate summary statistics
  const totalLanguages = languageData.length;
  const avgAcceptanceRate = totalLanguages > 0 
    ? (languageData.reduce((sum: number, item: CopilotMetricsByLanguage) => sum + item.percentage_code_acceptances, 0) / totalLanguages).toFixed(1)
    : "0";

  const highestAcceptanceLanguage = languageData.reduce((max: CopilotMetricsByLanguage, item: CopilotMetricsByLanguage) => 
    item.percentage_code_acceptances > max.percentage_code_acceptances ? item : max, 
    languageData[0] || { language: "N/A", percentage_code_acceptances: 0, percentage_lines_accepted: 0 }
  );

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div
          style={{
            backgroundColor: "#ffffff",
            border: "1px solid #e9ecef",
            borderRadius: "8px",
            boxShadow: "0 4px 12px rgba(0,0,0,0.15)",
            fontSize: "14px",
            padding: "12px",
          }}
        >
          <p style={{ color: "#232f3e", fontWeight: "bold", margin: "0 0 8px 0" }}>
            {`Language: ${label}`}
          </p>
          {payload.map((entry: any, index: number) => (
            <p key={index} style={{ color: entry.color, margin: "4px 0" }}>
              {`${entry.name}: ${entry.value.toLocaleString(undefined, {
                minimumFractionDigits: 0,
                maximumFractionDigits: 0
              })}`}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div style={{ marginBottom: '25px' }}>
      <ContentLayout
        header={
          <Header
            variant="h1"
            description="Analyze GitHub Copilot acceptance rates by programming language"
          >
            Language Analytics Dashboard
          </Header>
        }
        defaultPadding={true}
      >
        <SpaceBetween size="l">
          {/* Summary Cards */}
          <Container>
            <SpaceBetween size="m">
              <Box variant="h3">Summary Statistics</Box>
              <div style={{ display: "flex", gap: "20px", flexWrap: "wrap" }}>
                <div>
                  <Badge color="blue">Total Languages</Badge>
                  <Box variant="h2" color="text-body-secondary">
                    {totalLanguages}
                  </Box>
                </div>
                <div>
                  <Badge color="green">Average Acceptance Rate</Badge>
                  <Box variant="h2" color="text-body-secondary">
                    {avgAcceptanceRate}%
                  </Box>
                </div>
                <div>
                  <Badge color="red">Top Performing Language</Badge>
                  <Box variant="h2" color="text-body-secondary">
                    {highestAcceptanceLanguage.language}
                  </Box>
                </div>
              </div>
            </SpaceBetween>
          </Container>

          {/* Chart Section */}
          <Container
            header={
              <Header
                variant="h2"
                description="Percentage of accepted GitHub Copilot suggestions by programming language"
                actions={
                  <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                    <Select
                      selectedOption={{
                        label:
                          metricOptions.find((opt) => opt.value === selectedMetric)?.label ||
                          "Both Metrics",
                        value: selectedMetric,
                      }}
                      onChange={({ detail }) =>
                        setSelectedMetric(detail.selectedOption.value || "both")
                      }
                      options={metricOptions}
                      placeholder="Select percentage metric"
                    />

                    <Select
                      selectedOption={{
                        label:
                          metricOptionsAbsValues.find((opt) => opt.value === selectedMetricAbsVals)?.label ||
                          "Both Absolute Metrics",
                        value: selectedMetricAbsVals,
                      }}
                      onChange={({ detail }) =>
                        setSelectedMetricAbsVals(detail.selectedOption.value || "both_abs")
                      }
                      options={metricOptionsAbsValues}
                      placeholder="Select absolute metric"
                    />
                  </div>
                }
              >
                Acceptance Rates by Language
              </Header>
            }
          >
            {isLoading && (
              <Box textAlign="center" padding="xl">
                <Spinner size="large" />
                <Box variant="p" color="text-body-secondary">
                  Loading language analytics...
                </Box>
              </Box>
            )}

            {error && (
              <Alert statusIconAriaLabel="Error" type="error" header="Failed to load language analytics">
                {error}
              </Alert>
            )}

            {!isLoading && !error && chartData.length > 0 && (
              <div style={{ width: "100%", height: "500px" }}>
                <ResponsiveContainer width="100%" height="100%">
                  <ComposedChart
                    data={chartData}
                    margin={{
                      top: 20,
                      right: 50,
                      left: 20,
                      bottom: 50,
                    }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />

                    <XAxis
                      dataKey="language"
                      angle={-45}
                      textAnchor="end"
                      height={100}
                      fontSize={12}
                    />

                    {/* Left Y Axis - Percentages */}
                    <YAxis
                      yAxisId="left"
                      label={{ value: "Percentage (%)", angle: -90, position: "insideLeft" }}
                    />

                    {/* Right Y Axis - Absolute values */}
                    <YAxis
                      yAxisId="right"
                      orientation="right"
                      label={{ value: "Count ('000)", angle: 90, position: "insideRight" }}
                      tickFormatter={(value) => `${(value / 1000).toFixed(0)}`}
                    />

                    <Tooltip content={<CustomTooltip />} />
                    <Legend />

                    {/* Bars on Left Axis */}
                    {(selectedMetric === "both" || selectedMetric === "suggestions") && (
                      <Bar
                        yAxisId="left"
                        dataKey="percentage_accepted_suggestions"
                        fill="#8884d8"
                        name="Code Suggestions Accepted (%)"
                      />
                    )}
                    {(selectedMetric === "both" || selectedMetric === "lines") && (
                      <Bar
                        yAxisId="left"
                        dataKey="percentage_accepted_lines"
                        fill="#82ca9d"
                        name="Lines Accepted (%)"
                      />
                    )}

                    {/* Lines on Right Axis (Absolute Values) */}
                    {(selectedMetricAbsVals === "both_abs" || selectedMetricAbsVals === "suggestions_abs") && (
                      <Line
                        yAxisId="right"
                        type="monotone"
                        dataKey="lines_suggested"
                        stroke="#ff7300"
                        strokeWidth={3}
                        dot={{ r: 3 }}
                        name="Lines Suggested"
                      />
                    )}
                    {(selectedMetricAbsVals === "both_abs" || selectedMetricAbsVals === "lines_abs") && (
                      <Line
                        yAxisId="right"
                        type="monotone"
                        dataKey="code_suggestions"
                        stroke="#387908"
                        strokeWidth={2}
                        dot={{ r: 2 }}
                        name="Code Suggestions"
                      />
                    )}
                  </ComposedChart>
                </ResponsiveContainer>
              </div>
            )}

            {!isLoading && !error && chartData.length === 0 && (
              <Box textAlign="center" padding="xl">
                <Box variant="h3" color="text-body-secondary">
                  No language data available
                </Box>
                <Box variant="p" color="text-body-secondary">
                  There are no language analytics to display at the moment.
                </Box>
              </Box>
            )}
          </Container>
        </SpaceBetween>
      </ContentLayout>
    </div>
  );
};

export default LanguageAnalytics;
