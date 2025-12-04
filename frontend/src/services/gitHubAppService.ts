import axios from "axios";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

export interface GitHubAppResponse {
  id: string;
  organization_name: string;
  app_id: string;
  installation_id: string;
  private_key_encrypted: string;
  user_id: string;
  created_at: string;
}

class GitHubAppService {
  static async createGitHubApp(
    userId: string,
    organizationName: string,
    appId: string,
    installationId: string,
    privateKey: string
  ): Promise<void> {
    const token = localStorage.getItem("token");

    const payload = {
      user_id: userId,
      organization_name: organizationName,
      app_id: appId,
      installation_id: installationId,
      private_key: privateKey,
    };

    const headers: Record<string, string> = { "Content-Type": "application/json" };
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    await axios.post(`${API_BASE_URL}/github_app`, payload, { headers });
  }

  static async findGitHubApp(userId: string): Promise<GitHubAppResponse | null> {
    const token = localStorage.getItem("token");

    const headers: Record<string, string> = {};
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await axios.get(`${API_BASE_URL}/github_app/${userId}`, { headers });
    return response.data;
  }

  static async deleteGitHubApp(userId: string, githubAppId: string): Promise<void> {
    const token = localStorage.getItem("token");

    const headers: Record<string, string> = { "Content-Type": "application/json" };
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    await axios.delete(`${API_BASE_URL}/github_app/${githubAppId}`, {
      headers,
      data: { user_id: userId },
    });
  }
}

export default GitHubAppService;
