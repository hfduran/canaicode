import axios from "axios";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

export class UserService {
  static async login(username: string, password: string): Promise<{ access_token: string; user_id: string; token_type: string }> {
    const params = new URLSearchParams();
    params.append("username", username);
    params.append("password", password);

    const response = await axios.post(
      `${API_BASE_URL}/login`,
      params,
      {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      }
    );
    return response.data;
  }

  static async register(
    username: string,
    password: string,
    fullName: string,
    enterpriseName: string,
    email: string,
    cellphone: string,
    cpfCnpj: string
  ): Promise<{ username: string }> {
    const response = await axios.post(
      `${API_BASE_URL}/register`,
      {
        username,
        password,
        full_name: fullName,
        enterprise_name: enterpriseName,
        email,
        cellphone,
        cpf_cnpj: cpfCnpj
      },
      { headers: { "Content-Type": "application/json" } }
    );
    return response.data;
  }
}

export default UserService;