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
  Box,
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
      if (data && data.access_token && data.user_id) {
        localStorage.setItem("token", data.access_token);
        localStorage.setItem("user_id", data.user_id);
        // Trigger storage event to update navigation state
        window.dispatchEvent(new Event("storage"));
        setSuccessMsg("Login successful! Redirecting...");
        setTimeout(() => navigate("/"), 200);
      } else {
        setErrorMsg("Login failed. Please check your credentials.");
      }
    } catch (error: any) {
      setErrorMsg("Login failed. Please check your credentials.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{
      height: '100%',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '20px',
      boxSizing: 'border-box'
    }}>
      <div style={{
        width: '100%',
        maxWidth: '400px',
        backgroundColor: 'white',
        padding: '32px'
      }}>
        <Box margin={{ bottom: 'l' }}>
          <Header
            variant="h1"
            description="Input your username and password to login."
          >
            User Login
          </Header>
        </Box>
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
                fullWidth
              >
                Login
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
          <Box margin={{ top: 'l' }} textAlign="center">
            <Box variant="p">Don't have an account? <a href="/user-register">Register here.</a></Box>
          </Box>
        </Container>
      </div>
    </div>
  );
};

export default UserLogin;
