import { CalculatedMetricsRequest, CalculatedMetricsResponse } from "../types/model/index";
import axios from "axios";
import { formatDate } from "../utils/date/formatDate";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

export class CalculatedMetricsService {
  static async getCalculatedMetrics(
    request: CalculatedMetricsRequest
  ): Promise<CalculatedMetricsResponse> {
    try {
      const queryParams = new URLSearchParams();

      queryParams.append("period", request.period);
      queryParams.append("productivity_metric", request.productivity_metric);
      queryParams.append("initial_date_string", formatDate(request.initial_date));
      queryParams.append("final_date_string", formatDate(request.final_date));
      if (request.programming_languages) queryParams.append("languages_string", request.programming_languages.join(","));

      const url = `${API_BASE_URL}/calculated_metrics/${encodeURIComponent(
        request.team_name
      )}?${queryParams.toString()}`;

      const response = await axios.get<CalculatedMetricsResponse>(url, {
        headers: {
          "Content-Type": "application/json",
        },
      });

      return response.data;
    } catch (error) {
      console.error("Error fetching calculated metrics:", error);

      if (axios.isAxiosError(error)) {
        throw new Error(`Failed to fetch calculated metrics: ${error.message}`);
      } else {
        throw new Error("Failed to fetch calculated metrics: Unknown error");
      }
    }
  }

  static formatDateString(date: Date): string {
    return date.toISOString().split("T")[0];
  }

  static formatLanguagesString(languages: string[]): string {
    return languages.join(",");
  }
}

export default CalculatedMetricsService;
