import { CopilotMetricsByLanguage } from "../types/model/index";
import axios from "axios";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

export class LanguageMetricsService {
  static async getLanguageMetrics(): Promise<CopilotMetricsByLanguage[]> {
    try {
      const url = `${API_BASE_URL}/copilot_metrics/language`;

      const response = await axios.get<CopilotMetricsByLanguage[]>(url, {
        headers: {
          "Content-Type": "application/json",
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
}
