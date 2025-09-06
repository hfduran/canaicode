import React, { useState } from "react";
import {
  Container,
  Header,
  ContentLayout,
  SpaceBetween,
  FormField,
  Input,
  Button,
  Alert,
} from "@cloudscape-design/components";
import { useNavigate } from "react-router-dom";
import UserService from "../services/userLoginAndRegisterService";

const UserLogin: React.FC = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setErrorMsg(null);
    setSuccessMsg(null);

    try {
      const data = await UserService.login(username, password);
      if (data && data.access_token) {
        localStorage.setItem("token", data.access_token);
        setSuccessMsg("Login successful! Redirecting...");
        setTimeout(() => navigate("/"), 1200);
      } else {
        setErrorMsg("Login failed. Please check your credentials.");
      }
    } catch (error: any) {
      setErrorMsg("Login failed. Please check your credentials.");
    } finally {
      setIsLoading(false);
    }
  };

  const goToRegister = () => {
    navigate("/user-register");
  };

  return (
    <ContentLayout
      header={
        <Header
          variant="h1"
          description="Input your username and password to login."
        >
          User Login
        </Header>
      }
      defaultPadding={true}
    >
      <Container>
        <form onSubmit={handleLogin}>
          <SpaceBetween size="m">
            <FormField label="Username">
              <Input
                value={username}
                onChange={({ detail }) => setUsername(detail.value)}
                placeholder="Username"
                autoComplete="username"
              />
            </FormField>
            <FormField label="Password">
              <Input
                value={password}
                onChange={({ detail }) => setPassword(detail.value)}
                placeholder="Password"
                type="password"
                autoComplete="current-password"
              />
            </FormField>
            <Button
              variant="primary"
              loading={isLoading}
              disabled={!username || !password}
              formAction="submit"
            >
              Login
            </Button>
            <Button variant="link" onClick={goToRegister}>
              Not registered? Register here
            </Button>
            {successMsg && (
              <Alert type="success" statusIconAriaLabel="Success">
                {successMsg}
              </Alert>
            )}
            {errorMsg && (
              <Alert type="error" statusIconAriaLabel="Error">
                {errorMsg}
              </Alert>
            )}
          </SpaceBetween>
        </form>
      </Container>
    </ContentLayout>
  );
};

export default UserLogin;