import { CopilotUsersMetrics } from "../types/model/index";
import axios from "axios";
import { getToken, getUserId } from "../utils/auth";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

export class CopilotUsersMetricsService {
  static async getCopilotUsersMetrics(): Promise<CopilotUsersMetrics[]> {
    try {
      const token = getToken();
      const userId = getUserId();
      
      if (!token || !userId) {
        throw new Error("Authentication required");
      }

      const url = `${API_BASE_URL}/copilot_metrics/users/${encodeURIComponent(userId)}`;

      const response = await axios.get<CopilotUsersMetrics[]>(url, {
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
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
