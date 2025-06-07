import React, { useEffect, useState } from "react";
import Filters from "./Filters";
import mockDashboardData from "../data/mockData";
import { BarChart, Bar, CartesianGrid, XAxis, YAxis, Tooltip, Legend } from "recharts";
import RequestParamsForm from "./RequestParamsForm";
import { DashboardData, Filters as FiltersType, FlattenedDataEntry } from "../types/ui";
import { CalculatedMetricsService } from "../services/calculatedMetricsService";
import { CalculatedMetricsRequest } from "../types/model";
import { Button } from "@cloudscape-design/components";

const CalculatedMetricsDashboard: React.FC = () => {
  const [filters, setFilters] = useState<FiltersType>({
    languages: [],
    teams: [],
    initialDate: "",
    finalDate: "",
    period: "",
    numberOfAuthors: "",
  });
  const [requestData, setRequestData] = useState<DashboardData[]>(mockDashboardData);
  const [flattenedData, setFlattenedData] = useState<FlattenedDataEntry[]>([]);
  const [availableLanguages, setAvailableLanguages] = useState<Set<string>>(new Set());
  const [availableTeams, setAvailableTeams] = useState<Set<string>>(new Set());
  
  // Form state
  const [timeRange, setTimeRange] = useState<string>("");
  const [team, setTeam] = useState<string>("");
  const [metric, setMetric] = useState<string>("");
  const [initialDate, setInitialDate] = useState<string>("");
  const [finalDate, setFinalDate] = useState<string>("");

  useEffect(() => {
    setAvailableLanguages(new Set(requestData.flatMap((item) => item.languages)));
    setAvailableTeams(new Set(requestData.map((item) => item.team)));
  }, [requestData]);

  useEffect(() => {
    // Filter and flatten data
    const filteredData = requestData.filter((item) => {
      return (
        (filters.languages.length === 0 ||
          filters.languages.some((lang) => item.languages.includes(lang))) &&
        (filters.teams.length === 0 || filters.teams.includes(item.team)) &&
        (filters.period === "" || filters.period === item.period)
      );
    });
    const flat = filteredData.flatMap((item) =>
      item.data
        .filter(
          (entry) =>
            (!filters.numberOfAuthors ||
              Number(filters.numberOfAuthors) === entry.number_of_authors) &&
            (!filters.initialDate ||
              new Date(entry.initial_date) >= new Date(filters.initialDate)) &&
            (!filters.finalDate || new Date(entry.final_date) <= new Date(filters.finalDate))
        )
        .map((entry) => ({
          ...entry,
          team: item.team,
          period: item.period,
          languages: item.languages,
        }))
    );
    setFlattenedData(flat);
  }, [filters, requestData]);

  async function handleRequestData() {
    console.log("Form Data:", {
      timeRange,
      team,
      metric,
      initialDate,
      finalDate
    });

    try {
      // Map form values to request format
      const periodMap: { [key: string]: "W" | "M" | "Q" | "Y" } = {
        "Week": "W",
        "Month": "M",
        "Semester": "Q", // Using Q for semester/quarter
        "Year": "Y"
      };

      const productivityMetricMap: { [key: string]: "code_lines" | "commits" } = {
        "Codelines": "code_lines",
        "Commit": "commits"
      };

      // Use form date inputs or fallback to default range
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
        languages: [] // Empty for now, could be extended later
      };

      console.log("Sending request:", request);

      const response = await CalculatedMetricsService.getCalculatedMetrics(request);
      console.log("API Response:", response);

      if (response) {
        // Convert API response format to UI format
        const apiToDashboardPeriodMap: { [key: string]: string } = {
          "W": "week",
          "M": "month", 
          "Q": "quarter",
          "Y": "year"
        };

        const dashboardData: DashboardData[] = [{
          team: response.team,
          languages: response.languages,
          period: apiToDashboardPeriodMap[response.period] || response.period,
          data: response.data.map(item => ({
            initial_date: item.initial_date,
            final_date: item.final_date,
            net_changed_lines: item.net_changed_lines,
            net_changed_lines_by_copilot: item.net_changed_lines_by_copilot,
            percentage_changed_lines_by_copilot: item.percentage_changed_lines_by_copilot,
            number_of_authors: item.number_of_authors
          }))
        }];

        setRequestData(dashboardData);
        console.log("Updated requestData state:", dashboardData);
      }

    } catch (error) {
      console.error("Error calling API:", error);
    }
  }

  return (
    <div className="dashboard-container" style={{ display: "flex", gap: "20px", padding: "30px" }}>
      <div className="dashboard-main" style={{ flex: 0.7 }}>
        <h2>Select Language and Team data</h2>
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
        <Button variant="primary" onClick={handleRequestData}>
          Request Data
        </Button>
        <h2>Calculated Metrics</h2>

        <BarChart width={800} height={340} data={flattenedData}>
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
      </div>

      <div className="dashboard-filters" style={{ flex: 0.3 }}>
        <Filters
          filters={filters}
          setFilters={setFilters}
          availableLanguages={Array.from(availableLanguages)}
          availableTeams={Array.from(availableTeams)}
        />
      </div>
    </div>
  );
};

export default CalculatedMetricsDashboard;
