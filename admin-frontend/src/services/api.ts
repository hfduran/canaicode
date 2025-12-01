import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
const ADMIN_TOKEN = process.env.REACT_APP_ADMIN_KEY || '';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface FetchMetricsRequest {
  token: string;
}

export interface SendReportRequest {
  date_string: string;
  token: string;
}

export const adminAPI = {
  /**
   * Fetch copilot metrics from GitHub
   */
  fetchCopilotMetrics: async (): Promise<void> => {
    const request: FetchMetricsRequest = {
      token: ADMIN_TOKEN,
    };
    await apiClient.post('/admin/copilot_metrics/fetch', request);
  },

  /**
   * Send metrics email report
   * @param dateString - Optional date in YYYY-MM-DD format. If empty, uses today.
   */
  sendMetricsEmail: async (dateString: string = ''): Promise<void> => {
    const request: SendReportRequest = {
      date_string: dateString,
      token: ADMIN_TOKEN,
    };
    await apiClient.post('/admin/report/send', request);
  },
};
