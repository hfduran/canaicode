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

const UserRegister: React.FC = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const navigate = useNavigate();

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setErrorMsg(null);
    setSuccessMsg(null);

    try {
      const data = await UserService.register(username, password);
      if (data && data.username) {
        setSuccessMsg("Registration successful! Redirecting...");
        setTimeout(() => navigate("/user-login"), 1200);
      } else {
        setErrorMsg("Registration failed. Try a different username.");
      }
    } catch (error: any) {
      setErrorMsg("Registration failed. Try a different username.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ContentLayout
      header={
        <Header
          variant="h1"
          description="Input your username and password to register."
        >
          User Register
        </Header>
      }
      defaultPadding={true}
    >
      <Container>
        <form onSubmit={handleRegister}>
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
                autoComplete="new-password"
              />
            </FormField>
            <Button
              variant="primary"
              loading={isLoading}
              disabled={!username || !password}
              formAction="submit"
            >
              Register
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

export default UserRegister;