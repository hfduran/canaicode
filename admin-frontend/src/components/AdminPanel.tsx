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
} from '@cloudscape-design/components';
import { adminAPI } from '../services/api';

interface AlertMessage {
  type: 'success' | 'error' | 'info';
  message: string;
}

export const AdminPanel: React.FC = () => {
  const [selectedDate, setSelectedDate] = useState<string>('');
  const [isLoadingMetrics, setIsLoadingMetrics] = useState(false);
  const [isLoadingEmail, setIsLoadingEmail] = useState(false);
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
      </SpaceBetween>
    </Box>
  );
};
