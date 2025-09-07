import { CopilotMetricsByLanguage } from "../types/model/index";
import axios from "axios";
import { formatDate } from "../utils/date/formatDate";
import { getToken, getUserId } from "../utils/auth";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

export class LanguageMetricsService {
  static async getLanguageMetrics(): Promise<CopilotMetricsByLanguage[]> {
    try {
      const token = getToken();
      const userId = getUserId();
      
      if (!token || !userId) {
        throw new Error("Authentication required");
      }

      const url = `${API_BASE_URL}/copilot_metrics/language/${encodeURIComponent(userId)}`;

      const response = await axios.get<CopilotMetricsByLanguage[]>(url, {
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
      });

      return response.data;
    } catch (error) {
      console.error("Error fetching language metrics:", error);

      if (axios.isAxiosError(error)) {
        throw new Error(`Failed to fetch language metrics: ${error.message}`);
      } else {
        throw new Error("Failed to fetch language metrics: Unknown error");
      }
    }
  }

  static async getLanguageMetricsByPeriod(
    initial_date: Date,
    final_date: Date
  ): Promise<CopilotMetricsByLanguage[]> {
    try {
      const token = getToken();
      const userId = getUserId();
      
      if (!token || !userId) {
        throw new Error("Authentication required");
      }

      const queryParams = new URLSearchParams();
      queryParams.append("initial_date_string", formatDate(initial_date));
      queryParams.append("final_date_string", formatDate(final_date));

      const url = `${API_BASE_URL}/copilot_metrics/language/${encodeURIComponent(userId)}?${queryParams.toString()}`;

      const response = await axios.get<CopilotMetricsByLanguage[]>(url, {
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
      });

      return response.data;
    } catch (error) {
      console.error("Error fetching language metrics by period:", error);

      if (axios.isAxiosError(error)) {
        throw new Error(`Failed to fetch language metrics by period: ${error.message}`);
      } else {
        throw new Error("Failed to fetch language metrics by period: Unknown error");
      }
    }
  }
}
