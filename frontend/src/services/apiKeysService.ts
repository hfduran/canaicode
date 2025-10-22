import axios from "axios";
import { ApiKey, ApiKeyCreateResponse } from "../types/model";
import { getToken, getUserId } from "../utils/auth";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

class ApiKeysService {
  static async createApiKey(
    keyName: string,
    expiresAt?: string
  ): Promise<ApiKeyCreateResponse> {
    const token = getToken();
    const userId = getUserId();

    if (!token || !userId) {
      throw new Error("Authentication required");
    }

    const payload: any = {
      user_id: userId,
      key_name: keyName,
    };

    if (expiresAt) {
      payload.expires_at = expiresAt;
    }

    const headers: Record<string, string> = { "Content-Type": "application/json" };
    headers["Authorization"] = `Bearer ${token}`;

    const response = await axios.post<ApiKeyCreateResponse>(
      `${API_BASE_URL}/api_keys`,
      payload,
      { headers }
    );

    return response.data;
  }

  static async listApiKeys(): Promise<ApiKey[]> {
    const token = getToken();
    const userId = getUserId();

    if (!token || !userId) {
      throw new Error("Authentication required");
    }

    const headers: Record<string, string> = { "Content-Type": "application/json" };
    headers["Authorization"] = `Bearer ${token}`;

    const response = await axios.get<ApiKey[]>(
      `${API_BASE_URL}/api_keys/${userId}`,
      { headers }
    );

    return response.data;
  }

  static async revokeApiKey(keyId: string): Promise<void> {
    const token = getToken();
    const userId = getUserId();

    if (!token || !userId) {
      throw new Error("Authentication required");
    }

    const headers: Record<string, string> = { "Content-Type": "application/json" };
    headers["Authorization"] = `Bearer ${token}`;

    await axios.delete(
      `${API_BASE_URL}/api_keys/${keyId}`,
      {
        headers,
        data: { user_id: userId },
      }
    );
  }
}

export default ApiKeysService;
