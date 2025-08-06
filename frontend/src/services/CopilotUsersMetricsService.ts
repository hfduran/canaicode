import { CopilotUsersMetrics } from "../types/model/index";
import axios from "axios";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

export class CopilotUsersMetricsService {
  static async getCopilotUsersMetrics(): Promise<CopilotUsersMetrics[]> {
    try {
      const url = `${API_BASE_URL}/copilot_metrics/users`;

      const response = await axios.get<CopilotUsersMetrics[]>(url, {
        headers: {
          "Content-Type": "application/json",
        },
      });

      return response.data;
    } catch (error) {
      console.error("Error fetching copilot users metrics:", error);

      if (axios.isAxiosError(error)) {
        throw new Error(`Failed to fetch copilot users metrics: ${error.message}`);
      } else {
        throw new Error("Failed to fetch copilot users metrics: Unknown error");
      }
    }
  }
}
