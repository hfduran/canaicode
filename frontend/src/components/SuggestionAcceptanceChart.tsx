import React, { useState, useEffect } from "react";
import {
  Container,
  Header,
  FormField,
  Select,
  SelectProps,
  SpaceBetween,
  Box,
} from "@cloudscape-design/components";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { CopilotMetricsByPeriodService } from "../services/copilotMetricsByPeriodService";
import { CopilotMetricsByPeriod } from "../types/model/index";

interface ChartData {
  period: string;
  suggested: number;
  accepted: number;
}

interface SuggestionsChartData {
  period: string;
  suggested: number;
  accepted: number;
}

const SuggestionAcceptanceChart: React.FC = () => {
  const [period, setPeriod] = useState<"W" | "M" | "Q" | "Y">("M");
  const [data, setData] = useState<CopilotMetricsByPeriod[]>([]);
  const [chartData, setChartData] = useState<ChartData[]>([]);
  const [suggestionsChartData, setSuggestionsChartData] = useState<SuggestionsChartData[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const periodOptions: SelectProps.Option[] = [
    { label: "Weekly", value: "W" },
    { label: "Monthly", value: "M" },
    { label: "Quarterly", value: "Q" },
    { label: "Yearly", value: "Y" },
  ];

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await CopilotMetricsByPeriodService.getCopilotMetricsByPeriod(period);
      setData(result);

      // Transform data for the Lines of Code chart
      const transformedData: ChartData[] = result.map((item, index) => {
        const startDate = new Date(item.period_initial_date);
        const periodLabel = startDate.toLocaleDateString();

        // Calculate total suggested lines from acceptance ratio and accepted lines
        // percentage_lines_accepted is actually a ratio (0-1), not a percentage (0-100)
        const totalSuggested = item.total_lines_accepted > 0 && item.percentage_lines_accepted > 0
          ? Math.round(item.total_lines_accepted / item.percentage_lines_accepted)
          : item.total_lines_accepted;

        return {
          period: periodLabel,
          suggested: totalSuggested,
          accepted: item.total_lines_accepted,
        };
      });

      // Transform data for the Number of Suggestions chart
      const transformedSuggestionsData: SuggestionsChartData[] = result.map((item, index) => {
        const startDate = new Date(item.period_initial_date);
        const periodLabel = startDate.toLocaleDateString();

        // Calculate total suggested code suggestions from acceptance ratio and accepted suggestions
        // percentage_code_acceptances is actually a ratio (0-1), not a percentage (0-100)
        const totalCodeSuggestions = item.total_code_acceptances > 0 && item.percentage_code_acceptances > 0
          ? Math.round(item.total_code_acceptances / item.percentage_code_acceptances)
          : item.total_code_acceptances;

        return {
          period: periodLabel,
          suggested: totalCodeSuggestions,
          accepted: item.total_code_acceptances,
        };
      });

      setChartData(transformedData);
      setSuggestionsChartData(transformedSuggestionsData);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [period]);

  const customTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const suggested = payload.find((p: any) => p.dataKey === 'suggested')?.value || 0;
      const accepted = payload.find((p: any) => p.dataKey === 'accepted')?.value || 0;
      const acceptanceRate = suggested > 0 ? ((accepted / suggested) * 100).toFixed(1) : 0;

      return (
        <div style={{
          backgroundColor: '#ffffff',
          padding: '10px',
          border: '1px solid #ccc',
          borderRadius: '4px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
          <p style={{ margin: '0 0 5px 0', fontWeight: 'bold' }}>{label}</p>
          <p style={{ margin: '0 0 5px 0', color: '#8884d8' }}>
            Lines Suggested: {suggested.toLocaleString()}
          </p>
          <p style={{ margin: '0 0 5px 0', color: '#82ca9d' }}>
            Lines Accepted: {accepted.toLocaleString()}
          </p>
          <p style={{ margin: '0', color: '#666' }}>
            Acceptance Rate: {acceptanceRate}%
          </p>
        </div>
      );
    }
    return null;
  };

  const customSuggestionsTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const suggested = payload.find((p: any) => p.dataKey === 'suggested')?.value || 0;
      const accepted = payload.find((p: any) => p.dataKey === 'accepted')?.value || 0;
      const acceptanceRate = suggested > 0 ? ((accepted / suggested) * 100).toFixed(1) : 0;

      return (
        <div style={{
          backgroundColor: '#ffffff',
          padding: '10px',
          border: '1px solid #ccc',
          borderRadius: '4px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
          <p style={{ margin: '0 0 5px 0', fontWeight: 'bold' }}>{label}</p>
          <p style={{ margin: '0 0 5px 0', color: '#8884d8' }}>
            Suggestions Made: {suggested.toLocaleString()}
          </p>
          <p style={{ margin: '0 0 5px 0', color: '#82ca9d' }}>
            Suggestions Accepted: {accepted.toLocaleString()}
          </p>
          <p style={{ margin: '0', color: '#666' }}>
            Acceptance Rate: {acceptanceRate}%
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <Container
      header={
        <Header
          description="Compare lines of code suggested by Copilot vs. accepted by users over time"
        >
          Suggestion Acceptance Chart
        </Header>
      }
    >
      <SpaceBetween direction="vertical" size="l">
        <FormField label="Period">
          <Select
            selectedOption={periodOptions.find(option => option.value === period) || null}
            onChange={({ detail }) => setPeriod(detail.selectedOption.value as "W" | "M" | "Q" | "Y")}
            options={periodOptions}
            placeholder="Select a period"
          />
        </FormField>

        {error && (
          <Box variant="div" padding="m" color="text-status-error">
            Error: {error}
          </Box>
        )}

        {loading ? (
          <Box variant="div" textAlign="center" padding="l">
            Loading chart data...
          </Box>
        ) : chartData.length > 0 ? (
          <SpaceBetween direction="vertical" size="l">
            {/* Lines of Code Chart */}
            <Container
              header={
                <Header variant="h3">
                  Lines of Code - Suggested vs Accepted
                </Header>
              }
            >
              <div style={{ width: '100%', height: '400px' }}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={chartData} >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                      dataKey="period"
                      textAnchor="end"
                      height={100}
                      interval={0}
                    />
                    <YAxis />
                    <Tooltip content={customTooltip} />
                    <Legend verticalAlign="bottom" />
                    <Bar dataKey="suggested" fill="#8884d8" name="Lines Suggested" />
                    <Bar dataKey="accepted" fill="#82ca9d" name="Lines Accepted" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </Container>

            {/* Number of Suggestions Chart */}
            <Container
              header={
                <Header variant="h3">
                  Number of Suggestions - Made vs Accepted
                </Header>
              }
            >
              <div style={{ width: '100%', height: '400px' }}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={suggestionsChartData} >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                      dataKey="period"
                      textAnchor="end"
                      height={100}
                      interval={0}
                    />
                    <YAxis />
                    <Tooltip content={customSuggestionsTooltip} />
                    <Legend verticalAlign="bottom" />
                    <Bar dataKey="suggested" fill="#ff7c7c" name="Suggestions Made" />
                    <Bar dataKey="accepted" fill="#4caf50" name="Suggestions Accepted" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </Container>
          </SpaceBetween>
        ) : (
          <Box variant="div" textAlign="center" padding="l">
            No data available for the selected period
          </Box>
        )}
      </SpaceBetween>
    </Container>
  );
};

export default SuggestionAcceptanceChart;
