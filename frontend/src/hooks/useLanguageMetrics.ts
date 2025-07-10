import { useState, useCallback } from 'react';
import { CopilotMetricsByLanguage } from '../types/model';
import { LanguageMetricsService } from '../services/languageMetricsService';

export const useLanguageMetrics = () => {
  const [languageData, setLanguageData] = useState<CopilotMetricsByLanguage[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const fetchLanguageMetrics = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await LanguageMetricsService.getLanguageMetrics();
      console.log("Language metrics API response:", response);
      
      if (response) {
        setLanguageData(response);
      } else {
        setLanguageData([]);
      }
    } catch (error) {
      console.error("Error fetching language metrics:", error);
      setError(error instanceof Error ? error.message : 'An error occurred while fetching language metrics');
    } finally {
      setIsLoading(false);
    }
  }, []);

  return {
    languageData,
    isLoading,
    error,
    fetchLanguageMetrics,
  };
};
