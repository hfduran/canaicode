import axios from "axios";
import { ReportConfig } from "../types/model";
import { getToken, getUserId } from "../utils/auth";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

class ReportConfigService {
  // Get existing config for current user
  static async getReportConfig(): Promise<ReportConfig | null> {
    const token = getToken();
    const userId = getUserId();

    if (!token || !userId) {
      throw new Error("Authentication required");
    }

    const headers = {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    };

    try {
      const response = await axios.get<ReportConfig>(
        `${API_BASE_URL}/report_config/${userId}`,
        { headers }
      );
      return response.data;
    } catch (error: any) {
      // 404 means no config exists yet - this is not an error
      if (error.response?.status === 404) {
        return null;
      }
      throw error;
    }
  }

  // Create new config
  static async createReportConfig(emails: string[], period: string): Promise<ReportConfig> {
    const token = getToken();
    const userId = getUserId();

    if (!token || !userId) {
      throw new Error("Authentication required");
    }

    const headers = {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    };

    const payload = {
      user_id: userId,
      emails: emails,
      period: period
    };

    const response = await axios.post<ReportConfig>(
      `${API_BASE_URL}/report_config`,
      payload,
      { headers }
    );

    return response.data;
  }

  // Update existing config
  static async updateReportConfig(
    configId: string,
    emails: string[],
    period: string
  ): Promise<ReportConfig> {
    const token = getToken();
    const userId = getUserId();

    if (!token || !userId) {
      throw new Error("Authentication required");
    }

    const headers = {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    };

    const payload = {
      user_id: userId,
      emails: emails,
      period: period
    };

    const response = await axios.put<ReportConfig>(
      `${API_BASE_URL}/report_config/${configId}`,
      payload,
      { headers }
    );

    return response.data;
  }

  // Delete config
  static async deleteReportConfig(configId: string): Promise<void> {
    const token = getToken();
    const userId = getUserId();

    if (!token || !userId) {
      throw new Error("Authentication required");
    }

    const headers = {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    };

    await axios.delete(
      `${API_BASE_URL}/report_config/${configId}`,
      {
        headers,
        data: { user_id: userId }
      }
    );
  }
}

export default ReportConfigService;
