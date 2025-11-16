import React, { useEffect, useState, useRef } from "react";
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
  FormField,
  Button,
  Form,
  Multiselect,
} from "@cloudscape-design/components";
import { useLanguageMetrics } from "../hooks/useLanguageMetrics";
import { CopilotMetricsByLanguage } from "../types/model";
import { PROGRAMMING_LANGUAGES_OPTIONS, PROGRAMMING_LANGUAGES } from "../constants/programming_languages";
import DateRangeSelector from "../components/DateRangeSelector";

const LanguageAnalytics: React.FC = () => {
  const {
    languageData,
    languageDataTimeFiltered,
    isLoading,
    error,
    fetchLanguageMetrics,
    fetchLanguageMetricsTimeFiltered,
  } = useLanguageMetrics();

  const [selectedMetric, setSelectedMetric] = useState<string>("both");
  const [selectedMetricAbsVals, setSelectedMetricAbsVals] = useState<string>("both_abs");

  // Initialize with 6 months ago to today
  const getDefaultDates = () => {
    const today = new Date();
    const sixMonthsAgo = new Date();
    sixMonthsAgo.setMonth(today.getMonth() - 6);

    return {
      start: sixMonthsAgo.toISOString().split('T')[0],
      end: today.toISOString().split('T')[0]
    };
  };

  const defaultDates = getDefaultDates();
  const [startDate, setStartDate] = useState<string>(defaultDates.start);
  const [endDate, setEndDate] = useState<string>(defaultDates.end);
  const [isFiltering, setIsFiltering] = useState<boolean>(false);
  const [useFilteredData, setUseFilteredData] = useState<boolean>(false);
  const [selectedLanguages, setSelectedLanguages] = useState<string[]>([]);
  const hasInitialized = useRef(false);

  const metricOptions = [
    { label: "Code and Lines Suggestions", value: "both" },
    { label: "Code Suggestions", value: "suggestions" },
    { label: "Lines Suggested", value: "lines" },
  ];

  const metricOptionsAbsValues = [
    { label: "Accepted Suggestions and Accepted Lines (%)", value: "both_abs" },
    { label: "Accepted Suggestions (%)", value: "suggestions_abs" },
    { label: "Accepted Lines (%)", value: "lines_abs" },
  ];

  // Helper function to normalize language names (case-insensitive matching)
  const normalizeLanguageName = (languageName: string): string => {
    const canonicalLanguage = PROGRAMMING_LANGUAGES.find(
      lang => lang.toLowerCase() === languageName.toLowerCase()
    );
    return canonicalLanguage || languageName;
  };

  useEffect(() => {
    fetchLanguageMetrics();
  }, [fetchLanguageMetrics]);

  // Initialize selectedLanguages with all available languages on first load only
  useEffect(() => {
    if (languageData.length > 0 && !hasInitialized.current) {
      const availableLangs = new Set(
        languageData.map((item: CopilotMetricsByLanguage) => normalizeLanguageName(item.language))
      );
      const allAvailableLanguages = PROGRAMMING_LANGUAGES_OPTIONS
        .filter(option => availableLangs.has(option.value))
        .map(option => option.value);
      setSelectedLanguages(allAvailableLanguages);
      hasInitialized.current = true;
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [languageData]);

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

  // Get available languages from current dataset
  const currentDataset = useFilteredData ? languageDataTimeFiltered : languageData;
  const availableLanguages = new Set(
    currentDataset.map((item: CopilotMetricsByLanguage) => normalizeLanguageName(item.language))
  );

  // Create dynamic language options with disabled state
  const dynamicLanguageOptions = PROGRAMMING_LANGUAGES_OPTIONS.map(option => ({
    label: option.label,
    value: option.value,
    disabled: !availableLanguages.has(option.value),
    disabledReason: !availableLanguages.has(option.value)
      ? "No data available for this language"
      : undefined
  }));

  // Format data for the chart with aggregation for duplicate languages
  const chartData: ChartDataEntry[] = (() => {
    // Step 1: Filter by selected languages
    const filteredData = currentDataset.filter((item: CopilotMetricsByLanguage) => {
      if (selectedLanguages.length === 0) return false;
      const normalizedLanguage = normalizeLanguageName(item.language);
      return selectedLanguages.includes(normalizedLanguage);
    });

    // Step 2: Aggregate by normalized language name
    const aggregatedMap = filteredData.reduce((acc, item) => {
      const normalizedLanguage = normalizeLanguageName(item.language);

      if (!acc.has(normalizedLanguage)) {
        acc.set(normalizedLanguage, {
          code_acceptances: 0,
          code_suggestions: 0,
          lines_accepted: 0,
          lines_suggested: 0,
        });
      }

      const aggregated = acc.get(normalizedLanguage)!;
      aggregated.code_acceptances += item.code_acceptances;
      aggregated.code_suggestions += item.code_suggestions;
      aggregated.lines_accepted += item.lines_accepted;
      aggregated.lines_suggested += item.lines_suggested;

      return acc;
    }, new Map<string, {
      code_acceptances: number;
      code_suggestions: number;
      lines_accepted: number;
      lines_suggested: number;
    }>());

    // Step 3: Convert to chart data format with recalculated percentages
    const chartDataArray = Array.from(aggregatedMap.entries()).map(([language, data]) => ({
      language,
      percentage_accepted_suggestions: parseFloat(
        (data.code_suggestions > 0 ? (data.code_acceptances / data.code_suggestions) * 100 : 0).toFixed(1)
      ),
      percentage_accepted_lines: parseFloat(
        (data.lines_suggested > 0 ? (data.lines_accepted / data.lines_suggested) * 100 : 0).toFixed(1)
      ),
      code_acceptances: data.code_acceptances,
      code_suggestions: data.code_suggestions,
      lines_accepted: data.lines_accepted,
      lines_suggested: data.lines_suggested,
    }));

    // Step 4: Sort by lines_suggested (descending)
    return chartDataArray.sort((a, b) => b.lines_suggested - a.lines_suggested);
  })();

  // Calculate summary statistics
  const totalLanguages = chartData.length;
  const avgAcceptanceRate =
    totalLanguages > 0
      ? (
        chartData.reduce(
          (sum: number, item: ChartDataEntry) => sum + item.percentage_accepted_suggestions,
          0
        ) / totalLanguages
      ).toFixed(1)
      : "0";

  const highestAcceptanceLanguage =
    chartData.reduce(
      (max: ChartDataEntry, item: ChartDataEntry) =>
        item.percentage_accepted_suggestions > max.percentage_accepted_suggestions ? item : max,
      chartData[0] || { language: "N/A", percentage_accepted_suggestions: 0 }
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
                maximumFractionDigits: 0,
              })}`}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  // Handle filter button click
  const handleFilter = async () => {
    if (!startDate || !endDate) return;
    setIsFiltering(true);
    await fetchLanguageMetricsTimeFiltered(startDate, endDate);
    setUseFilteredData(true);
    setIsFiltering(false);
  };

  // Handle clear filter
  const handleClearFilter = () => {
    setStartDate("");
    setEndDate("");
    setUseFilteredData(false);
    setSelectedLanguages([]);
  };

  return (
    <div style={{ marginBottom: "25px" }}>
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
              <Box variant="h3">
                Summary Statistics {useFilteredData || selectedLanguages.length > 0 ? "(Filtered)" : "(Alltime)"}
                {selectedLanguages.length > 0 && (
                  <Badge color="grey"> {selectedLanguages.length} language{selectedLanguages.length !== 1 ? 's' : ''} selected</Badge>
                )}
              </Box>
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

          {/* Filter Section */}
          <Container
            header={
              <Header variant="h2" description="Filter statistics by time period and languages">
                Filters
              </Header>
            }
          >
            <Form>
              <SpaceBetween direction="vertical" size="xl">
                <SpaceBetween direction="vertical" size="m">
                  <DateRangeSelector
                    startDate={startDate}
                    endDate={endDate}
                    onStartDateChange={setStartDate}
                    onEndDateChange={setEndDate}
                  />
                </SpaceBetween>
                <FormField
                  label="Programming Languages"
                  description="Select at least one language to display analytics"
                >
                  <SpaceBetween direction="vertical" size="xs">
                    <Multiselect
                      selectedOptions={dynamicLanguageOptions.filter(option =>
                        selectedLanguages.includes(option.value)
                      )}
                      onChange={({ detail }) =>
                        setSelectedLanguages(
                          detail.selectedOptions.map(option => option.value).filter((value): value is string => typeof value === "string")
                        )
                      }
                      options={dynamicLanguageOptions}
                      placeholder="Select programming languages"
                    />
                    <SpaceBetween direction="horizontal" size="xs">
                      <Button
                        variant="normal"
                        onClick={() => {
                          const allAvailableLanguages = dynamicLanguageOptions
                            .filter(option => !option.disabled)
                            .map(option => option.value as string);
                          setSelectedLanguages(allAvailableLanguages);
                        }}
                      >
                        Select All
                      </Button>
                      <Button
                        variant="normal"
                        onClick={() => setSelectedLanguages([])}
                      >
                        Select None
                      </Button>
                    </SpaceBetween>
                  </SpaceBetween>
                </FormField>
                <SpaceBetween direction="horizontal" size="m">
                  <Button
                    variant="primary"
                    onClick={handleFilter}
                    loading={isFiltering}
                    disabled={!startDate || !endDate}
                  >
                    Filter Language Statistics
                  </Button>
                  {useFilteredData && (
                    <Button variant="link" onClick={handleClearFilter}>
                      Clear Filter
                    </Button>
                  )}
                </SpaceBetween>
              </SpaceBetween>
            </Form>
          </Container>

          {/* Chart Section */}
          <Container
            header={
              <Header
                variant="h2"
                description="GitHub Copilot suggestions and acceptance rates by programming language"
                actions={
                  <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
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
                      placeholder="Select bar chart metric"
                    />

                    <Select
                      selectedOption={{
                        label:
                          metricOptionsAbsValues.find((opt) => opt.value === selectedMetricAbsVals)
                            ?.label || "Both Percentage Metrics",
                        value: selectedMetricAbsVals,
                      }}
                      onChange={({ detail }) =>
                        setSelectedMetricAbsVals(detail.selectedOption.value || "both_abs")
                      }
                      options={metricOptionsAbsValues}
                      placeholder="Select line chart metric"
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
              <Alert
                statusIconAriaLabel="Error"
                type="error"
                header="Failed to load language analytics"
              >
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

                    {/* Left Y Axis - Absolute values */}
                    <YAxis
                      yAxisId="left"
                      label={{ value: "Count ('000)", angle: -90, position: "insideLeft" }}
                      tickFormatter={(value) => `${(value / 1000).toFixed(0)}`}
                    />

                    {/* Right Y Axis - Percentages */}
                    <YAxis
                      yAxisId="right"
                      orientation="right"
                      label={{ value: "Percentage (%)", angle: 90, position: "insideRight" }}
                    />

                    <Tooltip content={<CustomTooltip />} />
                    <Legend />

                    {/* Bars on Left Axis (Absolute Values) */}
                    {(selectedMetric === "both" || selectedMetric === "suggestions") && (
                      <Bar
                        yAxisId="left"
                        dataKey="code_suggestions"
                        fill="#8884d8"
                        name="Code Suggestions"
                      />
                    )}
                    {(selectedMetric === "both" || selectedMetric === "lines") && (
                      <Bar
                        yAxisId="left"
                        dataKey="lines_suggested"
                        fill="#82ca9d"
                        name="Lines Suggested"
                      />
                    )}

                    {/* Lines on Right Axis (Percentages) */}
                    {(selectedMetricAbsVals === "both_abs" || selectedMetricAbsVals === "suggestions_abs") && (
                      <Line
                        yAxisId="right"
                        type="monotone"
                        dataKey="percentage_accepted_suggestions"
                        stroke="#4B2E83"
                        strokeWidth={2}
                        dot={{ r: 2, stroke: "#4B2E83", strokeWidth: 1 }}
                        name="Code Suggestions Accepted (%)"
                        strokeDasharray="0"
                        style={{
                          filter: "drop-shadow(0px 0px 2px #4B2E83)",
                        }}
                        activeDot={{ r: 5, stroke: "#4B2E83", strokeWidth: 2 }}
                      />
                    )}
                    {(selectedMetricAbsVals === "both_abs" || selectedMetricAbsVals === "lines_abs") && (
                      <Line
                        yAxisId="right"
                        type="monotone"
                        dataKey="percentage_accepted_lines"
                        stroke="#2E8B57"
                        strokeWidth={3}
                        dot={{ r: 3, stroke: "#2E8B57", strokeWidth: 1 }}
                        name="Lines Accepted (%)"
                        strokeDasharray="0"
                        style={{
                          filter: "drop-shadow(0px 0px 2px #2E8B57)",
                        }}
                        activeDot={{ r: 6, stroke: "#2E8B57", strokeWidth: 2 }}
                      />
                    )}
                  </ComposedChart>
                </ResponsiveContainer>
              </div>
            )}

            {!isLoading && !error && selectedLanguages.length === 0 && (
              <Box textAlign="center" padding="xl">
                <Box variant="h3" color="text-body-secondary">
                  No languages selected
                </Box>
                <Box variant="p" color="text-body-secondary">
                  Please select at least one programming language from the filter above to view analytics.
                </Box>
              </Box>
            )}

            {!isLoading && !error && selectedLanguages.length > 0 && chartData.length === 0 && (
              <Box textAlign="center" padding="xl">
                <Box variant="h3" color="text-body-secondary">
                  No language data available
                </Box>
                <Box variant="p" color="text-body-secondary">
                  There are no language analytics to display for the selected languages.
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
