import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Box,
  Header,
  Container,
  Button,
  SpaceBetween,
  FormField,
  Input,
  Alert,
  Select,
  Modal,
  SelectProps,
} from "@cloudscape-design/components";
import ReportConfigService from "../services/reportConfigService";
import { ReportConfig } from "../types/model";
import { getUserId } from "../utils/auth";
import { REPORT_PERIOD_OPTIONS, EMAIL_REGEX } from "../constants/reportPeriods";

const Reports: React.FC = () => {
  const [reportConfig, setReportConfig] = useState<ReportConfig | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [emailInput, setEmailInput] = useState("");
  const [emails, setEmails] = useState<string[]>([]);
  const [selectedPeriod, setSelectedPeriod] = useState<SelectProps.Option | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [deleteModalVisible, setDeleteModalVisible] = useState(false);

  const navigate = useNavigate();

  // Helper function to format error messages
  const formatErrorMessage = (err: any): string => {
    if (typeof err?.response?.data?.detail === 'string') {
      return err.response.data.detail;
    }

    // Handle array of validation errors
    if (Array.isArray(err?.response?.data?.detail)) {
      const errors = err.response.data.detail.map((e: any) => e.msg || JSON.stringify(e)).join(', ');
      return errors || "Validation error";
    }

    // Handle object validation error
    if (typeof err?.response?.data?.detail === 'object') {
      return err.response.data.detail.msg || JSON.stringify(err.response.data.detail);
    }

    return err?.message || "An error occurred";
  };

  useEffect(() => {
    const userId = getUserId();
    if (!userId) {
      navigate("/user-login");
      return;
    }
    loadReportConfig();
  }, [navigate]);

  const loadReportConfig = async () => {
    try {
      setIsLoading(true);
      setErrorMsg(null);
      const config = await ReportConfigService.getReportConfig();

      if (config) {
        setReportConfig(config);
        setEmails(config.emails);

        // Find and set the matching period option
        const periodOption = REPORT_PERIOD_OPTIONS.find(
          opt => opt.value === config.period
        );
        if (periodOption) {
          setSelectedPeriod(periodOption);
        }
      }
    } catch (err: any) {
      setErrorMsg(formatErrorMessage(err));
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddEmail = () => {
    const email = emailInput.trim().toLowerCase();

    // Validate email format
    if (!EMAIL_REGEX.test(email)) {
      setErrorMsg("Invalid email format");
      return;
    }

    // Check for duplicates
    if (emails.includes(email)) {
      setErrorMsg("Email already added");
      return;
    }

    setEmails([...emails, email]);
    setEmailInput("");
    setErrorMsg(null);
  };

  const handleRemoveEmail = (index: number) => {
    setEmails(emails.filter((_, i) => i !== index));
  };

  const handleSaveConfig = async () => {
    // Validate
    if (emails.length === 0) {
      setErrorMsg("Please add at least one email address");
      return;
    }
    if (!selectedPeriod) {
      setErrorMsg("Please select a report frequency");
      return;
    }

    try {
      setIsSaving(true);
      setErrorMsg(null);

      let savedConfig: ReportConfig;

      if (reportConfig?.id) {
        // Update existing
        savedConfig = await ReportConfigService.updateReportConfig(
          reportConfig.id,
          emails,
          selectedPeriod.value || ""
        );
      } else {
        // Create new
        savedConfig = await ReportConfigService.createReportConfig(
          emails,
          selectedPeriod.value || ""
        );
      }

      setReportConfig(savedConfig);
      setSuccessMsg("Configuration saved successfully! Reports will be sent to the specified email addresses.");

      // Auto-dismiss success message after 5 seconds
      setTimeout(() => setSuccessMsg(null), 5000);
    } catch (err: any) {
      setErrorMsg(formatErrorMessage(err));
    } finally {
      setIsSaving(false);
    }
  };

  const handleDeleteConfig = async () => {
    if (!reportConfig?.id) return;

    try {
      setIsDeleting(true);
      setErrorMsg(null);
      await ReportConfigService.deleteReportConfig(reportConfig.id);

      // Reset to create mode
      setReportConfig(null);
      setEmails([]);
      setSelectedPeriod(null);
      setDeleteModalVisible(false);
      setSuccessMsg("Configuration deleted successfully");

      setTimeout(() => setSuccessMsg(null), 3000);
    } catch (err: any) {
      setErrorMsg(formatErrorMessage(err));
      setDeleteModalVisible(false);
    } finally {
      setIsDeleting(false);
    }
  };

  const handleKeyPress = (event: CustomEvent<{ key: string }>) => {
    if (event.detail.key === 'Enter') {
      handleAddEmail();
    }
  };

  if (isLoading) {
    return (
      <div style={{ padding: 20 }}>
        <SpaceBetween size="l">
          <Header variant="h1">Report Configuration</Header>
          <Container>
            <Box textAlign="center" padding={{ vertical: "xl" }}>
              Loading...
            </Box>
          </Container>
        </SpaceBetween>
      </div>
    );
  }

  return (
    <div style={{ padding: 20 }}>
      <SpaceBetween size="l">
        <Header
          variant="h1"
          description="Configure automated email reports for productivity metrics. Reports include graphs of productivity trends, copilot usage, and inactive user alerts."
        >
          Report Configuration
        </Header>

        {errorMsg && (
          <Alert type="error" dismissible onDismiss={() => setErrorMsg(null)}>
            {errorMsg}
          </Alert>
        )}

        {successMsg && (
          <Alert type="success" dismissible onDismiss={() => setSuccessMsg(null)}>
            {successMsg}
          </Alert>
        )}

        {!reportConfig && !isLoading && (
          <Alert type="info">
            No report configuration found. Create one to start receiving automated email reports with productivity metrics and insights.
          </Alert>
        )}

        <Container>
          <SpaceBetween size="l">
            <FormField
              label="Email Recipients"
              description="Enter email addresses that will receive the reports"
            >
              <SpaceBetween size="s">
                <div style={{ display: "flex", gap: "8px" }}>
                  <div style={{ flex: 1 }}>
                    <Input
                      value={emailInput}
                      onChange={({ detail }) => setEmailInput(detail.value)}
                      onKeyDown={handleKeyPress}
                      placeholder="email@example.com"
                      type="email"
                    />
                  </div>
                  <Button onClick={handleAddEmail} disabled={!emailInput.trim()}>
                    Add Email
                  </Button>
                </div>

                {emails.length > 0 && (
                  <div style={{
                    display: "flex",
                    flexWrap: "wrap",
                    gap: "8px",
                    padding: "8px",
                    background: "#f9f9f9",
                    borderRadius: "4px"
                  }}>
                    {emails.map((email, index) => (
                      <div
                        key={index}
                        style={{
                          display: "inline-flex",
                          alignItems: "center",
                          background: "#0972d3",
                          color: "white",
                          padding: "4px 8px",
                          borderRadius: "4px",
                          fontSize: "14px",
                        }}
                      >
                        <span style={{ marginRight: "8px" }}>{email}</span>
                        <button
                          onClick={() => handleRemoveEmail(index)}
                          style={{
                            background: "transparent",
                            border: "none",
                            color: "white",
                            cursor: "pointer",
                            fontSize: "16px",
                            padding: "0 4px",
                            lineHeight: "1",
                          }}
                          aria-label={`Remove ${email}`}
                        >
                          ×
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </SpaceBetween>
            </FormField>

            <FormField
              label="Report Frequency"
              description="Choose how often reports should be sent"
            >
              <Select
                selectedOption={selectedPeriod}
                onChange={({ detail }) => setSelectedPeriod(detail.selectedOption)}
                options={REPORT_PERIOD_OPTIONS}
                placeholder="Choose frequency..."
              />
            </FormField>

            <Box float="right">
              <SpaceBetween direction="horizontal" size="xs">
                {reportConfig && (
                  <Button
                    variant="normal"
                    onClick={() => setDeleteModalVisible(true)}
                  >
                    Delete Configuration
                  </Button>
                )}
                <Button
                  variant="primary"
                  onClick={handleSaveConfig}
                  loading={isSaving}
                  disabled={emails.length === 0 || !selectedPeriod}
                >
                  {reportConfig ? "Update Configuration" : "Save Configuration"}
                </Button>
              </SpaceBetween>
            </Box>
          </SpaceBetween>
        </Container>
      </SpaceBetween>

      {/* Delete Confirmation Modal */}
      <Modal
        visible={deleteModalVisible}
        onDismiss={() => setDeleteModalVisible(false)}
        header="Delete Report Configuration"
        footer={
          <Box float="right">
            <SpaceBetween direction="horizontal" size="xs">
              <Button
                variant="link"
                onClick={() => setDeleteModalVisible(false)}
              >
                Cancel
              </Button>
              <Button
                variant="primary"
                onClick={handleDeleteConfig}
                loading={isDeleting}
              >
                Delete
              </Button>
            </SpaceBetween>
          </Box>
        }
      >
        <Box>
          <Alert type="warning">
            Are you sure you want to delete your report configuration? You will stop receiving automated email reports. This action cannot be undone.
          </Alert>
        </Box>
      </Modal>
    </div>
  );
};

export default Reports;
