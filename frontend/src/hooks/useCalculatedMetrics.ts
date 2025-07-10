import { useState } from 'react';
import { DashboardData } from '../types/ui';
import { CalculatedMetricsRequest } from '../types/model';
import { CalculatedMetricsService } from '../services/calculatedMetricsService';

interface UseCalculatedMetricsParams {
  timeRange: string;
  team: string;
  metric: string;
  initialDate: string;
  finalDate: string;
  programmingLanguages: string[];
}

export const useCalculatedMetrics = () => {
  const [requestData, setRequestData] = useState<DashboardData[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleRequestData = async (params: UseCalculatedMetricsParams) => {
    const { timeRange, team, metric, initialDate, finalDate, programmingLanguages } = params;
    
    // Validate that all required parameters are provided
    if (!timeRange || !team || !metric || !initialDate || !finalDate) {
      setError('All fields except Programming Languages are required');
      return;
    }
    
    console.log("Form Data:", {
      timeRange,
      team,
      metric,
      initialDate,
      finalDate,
      programmingLanguages,
    });
    
    setIsLoading(true);
    setError(null);

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

      requestInitialDate = new Date(initialDate);
      requestFinalDate = new Date(finalDate);

      const request: CalculatedMetricsRequest = {
        team_name: team,
        period: periodMap[timeRange] || "M",
        productivity_metric: productivityMetricMap[metric] || "code_lines",
        initial_date: requestInitialDate,
        final_date: requestFinalDate,
        programming_languages: programmingLanguages,
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
            programming_languages: response.programming_languages,
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
      setError(error instanceof Error ? error.message : 'An error occurred while fetching data');
    } finally {
      setIsLoading(false);
    }
  };

  const setMockData = (mockData: DashboardData[]) => {
    setRequestData(mockData);
  };

  return {
    requestData,
    isLoading,
    error,
    handleRequestData,
    setMockData,
  };
};
