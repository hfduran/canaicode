import React, { useEffect, useState } from "react";
import { Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ComposedChart } from "recharts";
import {
  Container,
  Header,
  ContentLayout,
  SpaceBetween,
  Alert,
  Spinner,
  Box,
  DatePicker,
  FormField,
  Form
} from "@cloudscape-design/components";
import { useCopilotUsersMetrics } from "../hooks/useCopilotUsersMetrics";
import { CopilotUsersMetrics } from "../types/model";

const CopilotUsageChart: React.FC = () => {
  const { copilotUsersData, isLoading, error, fetchCopilotUsersMetrics } = useCopilotUsersMetrics();

  // Add state for period selection
  // Initialize with 6 months ago to today
  const getDefaultDates = () => {
    const today = new Date();
    const sixMonthsAgo = new Date();
    sixMonthsAgo.setMonth(today.getMonth() - 6);

    return {
      begin: sixMonthsAgo.toISOString().split('T')[0],
      end: today.toISOString().split('T')[0]
    };
  };

  const defaultDates = getDefaultDates();
  const [beginDate, setBeginDate] = useState<string>(defaultDates.begin);
  const [endDate, setEndDate] = useState<string>(defaultDates.end);

  useEffect(() => {
    fetchCopilotUsersMetrics();
  }, [fetchCopilotUsersMetrics]);

  interface ChartDataEntry {
    date: Date;
    total_code_assistant_users: number;
    total_chat_users: number;
  }

  // Parse and map data
  const chartData: ChartDataEntry[] = copilotUsersData.map((item: CopilotUsersMetrics) => ({
    date: new Date(item.date),
    total_code_assistant_users: parseFloat(item.total_code_assistant_users.toFixed(1)),
    total_chat_users: parseFloat(item.total_chat_users.toFixed(1)),
  }));

  // Filter data by selected period
  const filteredChartData = chartData.filter((entry) => {
    const entryTime = entry.date.getTime();
    const beginTime = beginDate ? new Date(beginDate).getTime() : -Infinity;
    const endTime = endDate ? new Date(endDate).getTime() : Infinity;
    return entryTime >= beginTime && entryTime <= endTime;
  });

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
            {`Date: ${(() => {
              const d = new Date(label);
              const day = d.getDate().toString().padStart(2, "0");
              const month = d.toLocaleString("en-US", { month: "short" }).toLowerCase();
              const year = d.getFullYear();
              return `${day}-${month}-${year}`;
            })()}`}
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
    <SpaceBetween size="l">
      {/* Period selection inputs - copied design from RequestParamsForm.tsx */}
      <Form>
        <SpaceBetween size="m" direction="horizontal">
          <FormField label="Beginning period">
            <DatePicker
              value={beginDate}
              onChange={({ detail }) => setBeginDate(detail.value)}
              placeholder="YYYY-MM-DD"
              openCalendarAriaLabel={() => "Open calendar"}
            />
          </FormField>
          <FormField label="Ending period">
            <DatePicker
              value={endDate}
              onChange={({ detail }) => setEndDate(detail.value)}
              placeholder="YYYY-MM-DD"
              openCalendarAriaLabel={() => "Open calendar"}
            />
          </FormField>
        </SpaceBetween>
      </Form>
      {/* Chart Section - total_code_assistant_users*/}
      <Container
        header={
          <Header
            description="Number of users who used Copilot at least once per period"
          >
            Copilot Usage
          </Header>
        }
      >
        {isLoading && (
          <Box textAlign="center" padding="xl">
            <Spinner size="large" />
            <Box variant="p" color="text-body-secondary">
              Loading Copilot usage analytics...
            </Box>
          </Box>
        )}

        {error && (
          <Alert statusIconAriaLabel="Error" type="error" header="Failed to load copilot usage analytics">
            {error}
          </Alert>
        )}

        {!isLoading && !error && filteredChartData.length > 0 && (
          <div style={{ width: "100%", height: "500px" }}>
            <ResponsiveContainer width="100%" height="100%">
              <ComposedChart
                data={filteredChartData}
                margin={{
                  top: 20,
                  right: 50,
                  left: 20,
                  bottom: 50,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" />

                <XAxis
                  dataKey="date"
                  angle={-45}
                  textAnchor="end"
                  height={100}
                  fontSize={12}
                  tickFormatter={(date) =>
                    date instanceof Date
                      ? date.toLocaleDateString()
                      : new Date(date).toLocaleDateString()
                  }
                />

                <YAxis
                  yAxisId="left"
                  label={{ value: "Number of different users", angle: -90, position: "insideLeft" }}
                />

                <Tooltip content={<CustomTooltip />} />
                <Legend />

                <Bar
                  yAxisId="left"
                  dataKey="total_code_assistant_users"
                  fill="#8884d8"
                  name="Number of different users who used Copilot chat"
                />
                <Bar
                  yAxisId="left"
                  dataKey="total_chat_users"
                  fill="#82ca9d"
                  name="Number of different users who accepted a Copilot suggestion"
                />
              </ComposedChart>
            </ResponsiveContainer>
          </div>
        )}

        {!isLoading && !error && filteredChartData.length === 0 && (
          <Box textAlign="center" padding="xl">
            <Box variant="h3" color="text-body-secondary">
              No Copilot usage data available
            </Box>
            <Box variant="p" color="text-body-secondary">
              There are no Copilot usage analytics to display at the moment.
            </Box>
          </Box>
        )}
      </Container>
    </SpaceBetween>
  );
};

export default CopilotUsageChart;
