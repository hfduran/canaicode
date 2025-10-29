import axios from "axios";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

class GitHubAppService {
  static async createGitHubApp(
    userId: string,
    organizationName: string,
    appId: string,
    installationId: string,
    privateKey: string
  ): Promise<void> {
    const token = localStorage.getItem("access_token");

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
}

export default GitHubAppService;
