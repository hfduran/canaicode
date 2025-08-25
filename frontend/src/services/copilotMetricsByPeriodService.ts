import { CopilotMetricsByPeriod } from "../types/model/index";
import axios from "axios";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

export class CopilotMetricsByPeriodService {
  static async getCopilotMetricsByPeriod(
    period: "W" | "M" | "Q" | "Y"
  ): Promise<CopilotMetricsByPeriod[]> {
    try {
      const queryParams = new URLSearchParams();
      queryParams.append("period", period);

      const url = `${API_BASE_URL}/copilot_metrics/period?${queryParams.toString()}`;

      const response = await axios.get<CopilotMetricsByPeriod[]>(url, {
        headers: {
          "Content-Type": "application/json",
        },
      });

      return response.data;
    } catch (error) {
      console.error("Error fetching copilot metrics by period:", error);

      if (axios.isAxiosError(error)) {
        throw new Error(`Failed to fetch copilot metrics by period: ${error.message}`);
      } else {
        throw new Error("Failed to fetch copilot metrics by period: Unknown error");
      }
    }
  }
}
