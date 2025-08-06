import { useState, useCallback } from 'react';
import { CopilotUsersMetrics } from '../types/model';
import { CopilotUsersMetricsService } from '../services/CopilotUsersMetricsService';

export const useCopilotUsersMetrics = () => {
  const [copilotUsersData, setCopilotUsersData] = useState<CopilotUsersMetrics[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const fetchCopilotUsersMetrics = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await CopilotUsersMetricsService.getCopilotUsersMetrics();
      console.log("Copilot users metrics API response:", response);
      
      if (response) {
        setCopilotUsersData(response);
      } else {
        setCopilotUsersData([]);
      }
    } catch (error) {
      console.error("Error fetching copilot users metrics:", error);
      setError(error instanceof Error ? error.message : 'An error occurred while fetching copilot users metrics');
    } finally {
      setIsLoading(false);
    }
  }, []);

  return {
    copilotUsersData,
    isLoading,
    error,
    fetchCopilotUsersMetrics,
  };
};
