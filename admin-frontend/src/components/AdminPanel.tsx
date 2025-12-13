import React, { useState } from 'react';
import {
  Container,
  Header,
  SpaceBetween,
  Button,
  DatePicker,
  FormField,
  Alert,
  Box,
  Input,
} from '@cloudscape-design/components';
import { adminAPI } from '../services/api';

interface AlertMessage {
  type: 'success' | 'error' | 'info' | 'warning';
  message: string;
}

export const AdminPanel: React.FC = () => {
  const [selectedDate, setSelectedDate] = useState<string>('');
  const [username, setUsername] = useState<string>('');
  const [isLoadingMetrics, setIsLoadingMetrics] = useState(false);
  const [isLoadingEmail, setIsLoadingEmail] = useState(false);
  const [isLoadingDeleteUser, setIsLoadingDeleteUser] = useState(false);
  const [isLoadingClearDb, setIsLoadingClearDb] = useState(false);
  const [isLoadingInitDb, setIsLoadingInitDb] = useState(false);
  const [alert, setAlert] = useState<AlertMessage | null>(null);

  const handleFetchMetrics = async () => {
    setIsLoadingMetrics(true);
    setAlert(null);
    try {
      await adminAPI.fetchCopilotMetrics();
      setAlert({
        type: 'success',
        message: 'Copilot metrics fetch initiated successfully!',
      });
    } catch (error: any) {
      setAlert({
        type: 'error',
        message: `Failed to fetch metrics: ${error.response?.data?.detail || error.message}`,
      });
    } finally {
      setIsLoadingMetrics(false);
    }
  };

  const handleSendEmail = async () => {
    setIsLoadingEmail(true);
    setAlert(null);
    try {
      await adminAPI.sendMetricsEmail(selectedDate);
      setAlert({
        type: 'success',
        message: 'Metrics email sent successfully!',
      });
    } catch (error: any) {
      setAlert({
        type: 'error',
        message: `Failed to send email: ${error.response?.data?.detail || error.message}`,
      });
    } finally {
      setIsLoadingEmail(false);
    }
  };

  const handleDeleteUserData = async () => {
    if (!username.trim()) {
      setAlert({
        type: 'error',
        message: 'Please enter a username',
      });
      return;
    }

    if (!window.confirm(`Are you sure you want to delete all data for user "${username}"? This action cannot be undone.`)) {
      return;
    }

    setIsLoadingDeleteUser(true);
    setAlert(null);
    try {
      await adminAPI.deleteUserData(username);
      setAlert({
        type: 'success',
        message: `User data for "${username}" deleted successfully!`,
      });
      setUsername('');
    } catch (error: any) {
      setAlert({
        type: 'error',
        message: `Failed to delete user data: ${error.response?.data?.detail || error.message}`,
      });
    } finally {
      setIsLoadingDeleteUser(false);
    }
  };

  const handleClearDatabase = async () => {
    if (!window.confirm('⚠️ WARNING: This will delete ALL data from the database! This action cannot be undone. Are you absolutely sure?')) {
      return;
    }

    setIsLoadingClearDb(true);
    setAlert(null);
    try {
      await adminAPI.clearDatabase();
      setAlert({
        type: 'success',
        message: 'Database cleared successfully!',
      });
    } catch (error: any) {
      setAlert({
        type: 'error',
        message: `Failed to clear database: ${error.response?.data?.detail || error.message}`,
      });
    } finally {
      setIsLoadingClearDb(false);
    }
  };

  const handleInitializeDatabase = async () => {
    setIsLoadingInitDb(true);
    setAlert(null);
    try {
      await adminAPI.initializeDatabase();
      setAlert({
        type: 'success',
        message: 'Database initialized successfully!',
      });
    } catch (error: any) {
      setAlert({
        type: 'error',
        message: `Failed to initialize database: ${error.response?.data?.detail || error.message}`,
      });
    } finally {
      setIsLoadingInitDb(false);
    }
  };

  return (
    <Box padding={{ vertical: 'xl', horizontal: 'l' }}>
      <SpaceBetween size="l">
        <Header variant="h1">CanAICode Admin Panel</Header>

        {alert && (
          <Alert
            type={alert.type}
            dismissible
            onDismiss={() => setAlert(null)}
          >
            {alert.message}
          </Alert>
        )}

        <Container header={<Header variant="h2">Fetch Copilot Metrics</Header>}>
          <SpaceBetween size="m">
            <Box variant="p">
              Fetch the latest GitHub Copilot usage metrics for all configured organizations.
              This will retrieve and store metrics data from GitHub for analysis.
            </Box>
            <Button
              variant="primary"
              onClick={handleFetchMetrics}
              loading={isLoadingMetrics}
              disabled={isLoadingEmail}
            >
              Fetch Metrics
            </Button>
          </SpaceBetween>
        </Container>

        <Container header={<Header variant="h2">Send Metrics Email Report</Header>}>
          <SpaceBetween size="m">
            <Box variant="p">
              Send the metrics email report to all configured recipients.
              You can optionally specify a date, or leave it empty to use today's date.
            </Box>
            <FormField
              label="Report Date (optional)"
              description="Leave empty to use today's date"
            >
              <DatePicker
                onChange={({ detail }) => setSelectedDate(detail.value)}
                value={selectedDate}
                openCalendarAriaLabel={(selectedDate) =>
                  'Choose date' + (selectedDate ? `, selected date is ${selectedDate}` : '')
                }
                placeholder="YYYY-MM-DD"
              />
            </FormField>
            <Button
              variant="primary"
              onClick={handleSendEmail}
              loading={isLoadingEmail}
              disabled={isLoadingMetrics}
            >
              Send Email Report
            </Button>
          </SpaceBetween>
        </Container>

        <Container header={<Header variant="h2">Delete User Data</Header>}>
          <SpaceBetween size="m">
            <Alert type="warning">
              This will delete all metrics data for the specified user. This action cannot be undone.
            </Alert>
            <Box variant="p">
              Delete all commit and copilot metrics data for a specific user.
              The user account itself will remain, but all associated metrics will be removed.
            </Box>
            <FormField
              label="Username"
              description="Enter the username of the user whose data should be deleted"
            >
              <Input
                value={username}
                onChange={({ detail }) => setUsername(detail.value)}
                placeholder="Enter username"
              />
            </FormField>
            <Button
              onClick={handleDeleteUserData}
              loading={isLoadingDeleteUser}
              disabled={isLoadingClearDb || isLoadingInitDb}
            >
              Delete User Data
            </Button>
          </SpaceBetween>
        </Container>

        <Container header={<Header variant="h2">Clear Entire Database</Header>}>
          <SpaceBetween size="m">
            <Alert type="error">
              DANGER: This will delete ALL data from the database, including all users and metrics!
              The database tables will remain intact. This action cannot be undone.
            </Alert>
            <Box variant="p">
              Use this before starting a demo to ensure a clean slate.
              This clears all data but keeps the database structure intact.
            </Box>
            <Button
              onClick={handleClearDatabase}
              loading={isLoadingClearDb}
              disabled={isLoadingDeleteUser || isLoadingInitDb}
            >
              Clear All Database Data
            </Button>
          </SpaceBetween>
        </Container>

        <Container header={<Header variant="h2">Initialize Database</Header>}>
          <SpaceBetween size="m">
            <Box variant="p">
              Initialize the database by creating all required tables.
              This is safe to run multiple times - it will only create tables that don't exist yet.
            </Box>
            <Button
              variant="primary"
              onClick={handleInitializeDatabase}
              loading={isLoadingInitDb}
              disabled={isLoadingDeleteUser || isLoadingClearDb}
            >
              Initialize Database
            </Button>
          </SpaceBetween>
        </Container>
      </SpaceBetween>
    </Box>
  );
};
