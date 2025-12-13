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

export interface DeleteUserDataRequest {
  username: string;
  token: string;
}

export interface AdminActionRequest {
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

  /**
   * Delete all metrics data for a specific user
   * @param username - Username of the user whose data should be deleted
   */
  deleteUserData: async (username: string): Promise<void> => {
    const request: DeleteUserDataRequest = {
      username,
      token: ADMIN_TOKEN,
    };
    await apiClient.delete('/admin/user_metrics', { data: request });
  },

  /**
   * Clear all data from the database (keeps table structure)
   */
  clearDatabase: async (): Promise<void> => {
    const request: AdminActionRequest = {
      token: ADMIN_TOKEN,
    };
    await apiClient.post('/admin/database/clear', request);
  },

  /**
   * Initialize database tables (creates tables if they don't exist)
   */
  initializeDatabase: async (): Promise<void> => {
    const request: AdminActionRequest = {
      token: ADMIN_TOKEN,
    };
    await apiClient.post('/admin/database/init', request);
  },
};
