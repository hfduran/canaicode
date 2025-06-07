import React, { useState } from "react";
import Filters from "./Filters";
import mockDashboardData from "../data/mockData";
import { BarChart, Bar, CartesianGrid, XAxis, YAxis, Tooltip, Legend } from "recharts";
import RequestParamsForm from "./RequestParamsForm";
import { DashboardData, FlattenedDataEntry } from "../types/ui";
import { CalculatedMetricsService } from "../services/calculatedMetricsService";
import { CalculatedMetricsRequest } from "../types/model";
import { Button, Modal, Box, SpaceBetween } from "@cloudscape-design/components";
import { useDataFiltering } from "../hooks/useDataFiltering";
import { DashboardFiltersModal } from "./DashboardFiltersModal";

const CalculatedMetricsDashboard: React.FC = () => {
  const [requestData, setRequestData] = useState<DashboardData[]>([]);
  
  // Form state
  const [timeRange, setTimeRange] = useState<string>("");
  const [team, setTeam] = useState<string>("");
  const [metric, setMetric] = useState<string>("");
  const [initialDate, setInitialDate] = useState<string>("");
  const [finalDate, setFinalDate] = useState<string>("");
  const [filteredData, setFilteredData] = useState<FlattenedDataEntry[]>([]);
  const [isFiltersModalVisible, setIsFiltersModalVisible] = useState<boolean>(false);

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
            data: response.data.map((item) => ({
              initial_date: item.initial_date,
              final_date: item.final_date,
              net_changed_lines: item.net_changed_lines,
              net_changed_lines_by_copilot: item.net_changed_lines_by_copilot,
              percentage_changed_lines_by_copilot: item.percentage_changed_lines_by_copilot,
              number_of_authors: item.number_of_authors,
            })),
          },
        ];

        setRequestData(dashboardData);
        console.log("Updated requestData state:", dashboardData);
      } else {
        setRequestData([])
      }
    } catch (error) {
      console.error("Error calling API:", error);
    }
  }

  const handleLoadDemoData = () => {
    setRequestData(mockDashboardData);
  }

  const handleOpenFiltersModal = () => {
    setIsFiltersModalVisible(true)
  }

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
        <BarChart width={800} height={340} data={filteredData}>
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
