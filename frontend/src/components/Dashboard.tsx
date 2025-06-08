import React, { useState } from "react";
import mockDashboardData from "../data/mockData";
import { BarChart, Bar, CartesianGrid, XAxis, YAxis, Tooltip, Legend } from "recharts";
import RequestParamsForm from "./RequestParamsForm";
import { FlattenedDataEntry, FormattedDataEntry } from "../types/ui";
import { Button, SpaceBetween } from "@cloudscape-design/components";
import { DashboardFiltersModal } from "./DashboardFiltersModal";
import { formatDate } from "../utils/date/formatDate";
import { useCalculatedMetrics } from "../hooks"; 

const CalculatedMetricsDashboard: React.FC = () => {
  const [timeRange, setTimeRange] = useState<string>("");
  const [team, setTeam] = useState<string>("");
  const [metric, setMetric] = useState<string>("");
  const [initialDate, setInitialDate] = useState<string>("");
  const [finalDate, setFinalDate] = useState<string>("");
  const [filteredData, setFilteredData] = useState<FlattenedDataEntry[]>([]);
  const [isFiltersModalVisible, setIsFiltersModalVisible] = useState<boolean>(false);

  const { requestData, isLoading, error, handleRequestData, setMockData } = useCalculatedMetrics();

  const formattedData: FormattedDataEntry[] = filteredData.map((entry) => ({
    ...entry,
    initial_date: formatDate(entry.initial_date),
    final_date: formatDate(entry.final_date),
  }));

  const isFormValid = timeRange && team && metric && initialDate && finalDate;

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
    });
  };

  const handleLoadDemoData = () => {
    setMockData(mockDashboardData);
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
            <Button 
              variant="primary" 
              onClick={handleSubmitRequest}
              loading={isLoading}
              disabled={!isFormValid}
            >
              Request Data
            </Button>
            <Button variant="normal" onClick={handleOpenFiltersModal}>
              Open Filters
            </Button>
            <Button variant="normal" onClick={handleLoadDemoData}>
              Load demo data
            </Button>
          </SpaceBetween>
          {error && (
            <div style={{ color: 'red', marginTop: '10px' }}>
              Error: {error}
            </div>
          )}
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
