import React, { useState } from "react";
import {
  Container,
  Header,
  ContentLayout,
  SpaceBetween,
  FormField,
  Button,
  Box,
  FileUpload,
} from "@cloudscape-design/components";
import UploadMetricsService from "../services/uploadMetricsService";

const COPILOT_EXAMPLE_PATH = "/static/examples/Copilot_example.json";
const COMMIT_EXAMPLE_PATH = "/static/examples/Commits_example.xlsx";
const COMMIT_SCRIPT_PATH = "/static/examples/git_consumer.zip";

const UploadMetrics: React.FC = () => {
  const [copilotFile, setCopilotFile] = useState<File | null>(null);
  const [commitFile, setCommitFile] = useState<File | null>(null);
  const [copilotLoading, setCopilotLoading] = useState(false);
  const [commitLoading, setCommitLoading] = useState(false);
  const [copilotSuccess, setCopilotSuccess] = useState<string | null>(null);
  const [commitSuccess, setCommitSuccess] = useState<string | null>(null);
  const [copilotError, setCopilotError] = useState<string | null>(null);
  const [commitError, setCommitError] = useState<string | null>(null);

  const handleCopilotUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    setCopilotLoading(true);
    setCopilotSuccess(null);
    setCopilotError(null);

    try {
      if (!copilotFile) {
        setCopilotError("Please select a JSON file.");
        setCopilotLoading(false);
        return;
      }
      await UploadMetricsService.uploadCopilotMetrics(copilotFile);
      setCopilotSuccess("Copilot metrics uploaded successfully!");
    } catch (error: any) {
      setCopilotError("Failed to upload copilot metrics.");
    } finally {
      setCopilotLoading(false);
    }
  };

  const handleCommitUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    setCommitLoading(true);
    setCommitSuccess(null);
    setCommitError(null);

    try {
      if (!commitFile) {
        setCommitError("Please select an XLSX file.");
        setCommitLoading(false);
        return;
      }
      await UploadMetricsService.uploadCommitMetrics(commitFile);
      setCommitSuccess("Commit metrics uploaded successfully!");
    } catch (error: any) {
      setCommitError("Failed to upload commit metrics.");
    } finally {
      setCommitLoading(false);
    }
  };

  const handleDownloadCopilotExample = () => {
    // This will trigger download from the static path
    window.open(COPILOT_EXAMPLE_PATH, "_blank");
  };

  const handleDownloadCommitExample = () => {
    const link = document.createElement('a');
    link.href = COMMIT_EXAMPLE_PATH;
    link.download = "Commits_example.xlsx";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleDownloadCommitScript = () => {
    const link = document.createElement('a');
    link.href = COMMIT_SCRIPT_PATH;
    link.download = "git_consumer.zip";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <ContentLayout
      header={
        <Header
          variant="h1"
          description="Use the forms below to upload your metrics data."
        >
          Upload your Metrics
        </Header>
      }
      defaultPadding={true}
    >
      <SpaceBetween direction="horizontal" size="l">
        {/* Copilot Metrics Upload */}
        <div style={{ minWidth: "500px", width: "100%", maxWidth: "900px" }}>
          <Container
            header={<Header variant="h2">Upload Copilot Metrics (JSON)</Header>}
          >
            <form onSubmit={handleCopilotUpload}>
              <SpaceBetween size="m">
              <FormField label="Copilot Metrics File" description="Drop a JSON file here">
                <FileUpload
                  accept=".json"
                  onChange={({ detail }) => setCopilotFile(detail.value[0] || null)}
                  value={copilotFile ? [copilotFile] : []}
                  showFileLastModified
                  showFileSize
                  showFileThumbnail={false}
                  multiple={false}
                />
              </FormField>
              <Button
                variant="primary"
                loading={copilotLoading}
                disabled={!copilotFile}
              >
                Upload Copilot Metrics
              </Button>
              {copilotSuccess && <Box color="text-status-success">{copilotSuccess}</Box>}
              {copilotError && <Box color="text-status-error">{copilotError}</Box>}
              <Box margin={{ top: "m" }}>
                <Button
                  variant="link"
                  iconName="download"
                  onClick={handleDownloadCopilotExample}
                >
                  Download Copilot Metrics JSON Example
                </Button>
              </Box>
            </SpaceBetween>
          </form>
        </Container>
        </div>

        {/* Commit Metrics Upload */}
        <div style={{ minWidth: "500px", width: "100%", maxWidth: "900px" }}>
          <Container
            header={<Header variant="h2">Upload Commit Metrics (XLSX)</Header>}
          >
            <form onSubmit={handleCommitUpload}>
              <SpaceBetween size="m">
              <FormField label="Commit Metrics File" description="Drop an XLSX file here">
                <FileUpload
                  accept=".xlsx"
                  onChange={({ detail }) => setCommitFile(detail.value[0] || null)}
                  value={commitFile ? [commitFile] : []}
                  showFileLastModified
                  showFileSize
                  showFileThumbnail={false}
                  multiple={false}
                />
              </FormField>
              <Button
                variant="primary"
                loading={commitLoading}
                disabled={!commitFile}
              >
                Upload Commit Metrics
              </Button>
              {commitSuccess && <Box color="text-status-success">{commitSuccess}</Box>}
              {commitError && <Box color="text-status-error">{commitError}</Box>}
              <Box margin={{ top: "m" }}>
                <Button
                  variant="link"
                  iconName="download"
                  onClick={handleDownloadCommitExample}
                >
                  Download Commit Metrics XLSX Example
                </Button>
                <br />
                <Button
                  variant="link"
                  iconName="download"
                  onClick={handleDownloadCommitScript}
                >
                  Download Commit Script for XLSX Generation
                </Button>
              </Box>
            </SpaceBetween>
          </form>
        </Container>
        </div>
      </SpaceBetween>
    </ContentLayout>
  );
};

export default UploadMetrics;