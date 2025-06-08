import React, { useState } from "react";
import mockDashboardData from "../data/mockData";
import { BarChart, Bar, CartesianGrid, XAxis, YAxis, Tooltip, Legend } from "recharts";
import RequestParamsForm from "./RequestParamsForm";
import { DashboardData, FlattenedDataEntry, FormattedDataEntry } from "../types/ui";
import { CalculatedMetricsService } from "../services/calculatedMetricsService";
import { CalculatedMetricsRequest } from "../types/model";
import { Button, SpaceBetween } from "@cloudscape-design/components";
import { DashboardFiltersModal } from "./DashboardFiltersModal";
import {formatDate} from "../utils/date/formatDate"; 

const CalculatedMetricsDashboard: React.FC = () => {
  const [requestData, setRequestData] = useState<DashboardData[]>([]);

  // Form state
  const [timeRange, setTimeRange] = useState<string>("");
  const [team, setTeam] = useState<string>("");
  const [metric, setMetric] = useState<string>("");
  const [initialDate, setInitialDate] = useState<string>("");
  const [finalDate, setFinalDate] = useState<string>("");
  const [filteredData, setFilteredData] = useState<FlattenedDataEntry[]>([]);
  const [formattedData, setFormattedData] = useState<FormattedDataEntry[]>([]);
  const [isFiltersModalVisible, setIsFiltersModalVisible] = useState<boolean>(false);

  // Effect to format data for the chart
  React.useEffect(() => {
    const formatted: FormattedDataEntry[] = filteredData.map((entry) => ({
      ...entry,
      initial_date: formatDate(entry.initial_date),
      final_date: formatDate(entry.final_date),
    }));
    setFormattedData(formatted);
  }, [filteredData]);

  async function handleRequestData() {
    console.log("Form Data:", {
      timeRange,
      team,
      metric,
      initialDate,
      finalDate,
    });

    try {
      const periodMap: { [key: string]: "W" | "M" | "Q" | "Y" } = {
        Week: "W",
        Month: "M",
        Semester: "Q",
        Year: "Y",
      };

      const productivityMetricMap: { [key: string]: "code_lines" | "commits" } = {
        Codelines: "code_lines",
        Commit: "commits",
      };

      let requestInitialDate: Date;
      let requestFinalDate: Date;

      if (initialDate && finalDate) {
        requestInitialDate = new Date(initialDate);
        requestFinalDate = new Date(finalDate);
      } else {
        // Fallback to default date range (last month)
        requestFinalDate = new Date();
        requestInitialDate = new Date();
        requestInitialDate.setMonth(requestFinalDate.getMonth() - 1);
      }

      const request: CalculatedMetricsRequest = {
        team_name: team,
        period: periodMap[timeRange] || "M",
        productivity_metric: productivityMetricMap[metric] || "code_lines",
        initial_date: requestInitialDate,
        final_date: requestFinalDate,
        languages: [], // Empty for now, could be extended later
      };

      console.log("Sending request:", request);

      const response = await CalculatedMetricsService.getCalculatedMetrics(request);
      console.log("API Response:", response);

      if (response) {
        // Convert API response format to UI format
        const apiToDashboardPeriodMap: { [key: string]: string } = {
          W: "week",
          M: "month",
          Q: "quarter",
          Y: "year",
        };

        const dashboardData: DashboardData[] = [
          {
            team: response.team,
            languages: response.languages,
            period: apiToDashboardPeriodMap[response.period] || response.period,
            data: response.data.map((item) => ({ ...item })),
          },
        ];

        setRequestData(dashboardData);
        console.log("Updated requestData state:", dashboardData);
      } else {
        setRequestData([]);
      }
    } catch (error) {
      console.error("Error calling API:", error);
    }
  }

  const handleLoadDemoData = () => {
    setRequestData(mockDashboardData);
  };

  const handleOpenFiltersModal = () => {
    setIsFiltersModalVisible(true);
  };

  return (
    <div
      className="dashboard-container"
      style={{ display: "flex", flexDirection: "column", gap: "20px", padding: "30px" }}
    >
      <div className="dashboard-main">
        <h2>Select Language and Team data</h2>
        <SpaceBetween size="m" direction="vertical">
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
          />
          <SpaceBetween direction="horizontal" size="m">
            <Button variant="primary" onClick={handleRequestData}>
              Request Data
            </Button>
            <Button variant="normal" onClick={handleOpenFiltersModal}>
              Open Filters
            </Button>
            <Button variant="normal" onClick={handleLoadDemoData}>
              Load demo data
            </Button>
          </SpaceBetween>
        </SpaceBetween>
        <h2>Calculated Metrics</h2>
        <BarChart width={800} height={340} data={formattedData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="initial_date" />
          <YAxis />
          <Tooltip
            formatter={(value: any, name: string, props: any) => {
              if (name === "Copilot Added Lines") {
                const percentage = props.payload.percentage_lines_added_by_copilot;
                return [`${value} lines (${percentage}%)`, name];
              }
              return [`${value} lines`, name];
            }}
          />
          <Legend />
          <Bar dataKey="net_changed_lines" fill="#8884d8" name="Total Added Lines" />
          <Bar dataKey="net_changed_lines_by_copilot" fill="#82ca9d" name="Copilot Added Lines" />
        </BarChart>
        <DashboardFiltersModal
          data={requestData}
          setFilteredData={setFilteredData}
          visible={isFiltersModalVisible}
          setVisible={setIsFiltersModalVisible}
        />
      </div>
    </div>
  );
};

export default CalculatedMetricsDashboard;
