import axios from "axios";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

export class UploadMetricsService {
  static async uploadCopilotMetrics(user_id: string, file: File, token: string): Promise<void> {
    try {
      const formData = new FormData();
      formData.append("user_id", user_id);
      formData.append("file", file);

      await axios.post(`${API_BASE_URL}/copilot_metrics/upload`, formData, {
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "multipart/form-data",
        },
      });
    } catch (error) {
      console.error("Error uploading Copilot metrics:", error);
      throw error;
    }
  }

  static async uploadCommitMetrics(user_id: string, file: File, token: string): Promise<void> {
    try {
      const formData = new FormData();
      formData.append("user_id", user_id);
      formData.append("file", file);

      await axios.post(`${API_BASE_URL}/commit_metrics/upload`, formData, {
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "multipart/form-data",
        },
      });
    } catch (error) {
      console.error("Error uploading Commit metrics:", error);
      throw error;
    }
  }
}

export default UploadMetricsService;