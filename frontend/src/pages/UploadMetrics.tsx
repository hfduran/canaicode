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
  Table,
  StatusIndicator,
} from "@cloudscape-design/components";
import UploadMetricsService from "../services/uploadMetricsService";

const COPILOT_EXAMPLE_PATH = "/static/examples/Copilot_example.json";
const COMMIT_EXAMPLE_PATH = "/static/examples/Commits_example.xlsx";
const COMMIT_SCRIPT_PATH = "/static/examples/git_consumer.zip";

type FileUploadStatus = {
  file: File;
  status: 'pending' | 'uploading' | 'success' | 'error';
  error?: string;
};

const UploadMetrics: React.FC = () => {
  const [copilotFiles, setCopilotFiles] = useState<File[]>([]);
  const [commitFiles, setCommitFiles] = useState<File[]>([]);
  const [copilotUploads, setCopilotUploads] = useState<FileUploadStatus[]>([]);
  const [commitUploads, setCommitUploads] = useState<FileUploadStatus[]>([]);
  const [copilotLoading, setCopilotLoading] = useState(false);
  const [commitLoading, setCommitLoading] = useState(false);

  const handleCopilotUpload = async (e: React.FormEvent) => {
    e.preventDefault();

    if (copilotFiles.length === 0) {
      return;
    }

    setCopilotLoading(true);
    const uploadStatuses: FileUploadStatus[] = copilotFiles.map(file => ({
      file,
      status: 'pending' as const,
    }));
    setCopilotUploads(uploadStatuses);

    const uploadPromises = copilotFiles.map(async (file, index) => {
      setCopilotUploads(prev => {
        const updated = [...prev];
        updated[index] = { ...updated[index], status: 'uploading' };
        return updated;
      });

      try {
        await UploadMetricsService.uploadCopilotMetrics(file);
        setCopilotUploads(prev => {
          const updated = [...prev];
          updated[index] = { ...updated[index], status: 'success' };
          return updated;
        });
      } catch (error: any) {
        setCopilotUploads(prev => {
          const updated = [...prev];
          updated[index] = {
            ...updated[index],
            status: 'error',
            error: error.message || 'Upload failed'
          };
          return updated;
        });
      }
    });

    await Promise.allSettled(uploadPromises);
    setCopilotLoading(false);
  };

  const handleCommitUpload = async (e: React.FormEvent) => {
    e.preventDefault();

    if (commitFiles.length === 0) {
      return;
    }

    setCommitLoading(true);
    const uploadStatuses: FileUploadStatus[] = commitFiles.map(file => ({
      file,
      status: 'pending' as const,
    }));
    setCommitUploads(uploadStatuses);

    const uploadPromises = commitFiles.map(async (file, index) => {
      setCommitUploads(prev => {
        const updated = [...prev];
        updated[index] = { ...updated[index], status: 'uploading' };
        return updated;
      });

      try {
        await UploadMetricsService.uploadCommitMetrics(file);
        setCommitUploads(prev => {
          const updated = [...prev];
          updated[index] = { ...updated[index], status: 'success' };
          return updated;
        });
      } catch (error: any) {
        setCommitUploads(prev => {
          const updated = [...prev];
          updated[index] = {
            ...updated[index],
            status: 'error',
            error: error.message || 'Upload failed'
          };
          return updated;
        });
      }
    });

    await Promise.allSettled(uploadPromises);
    setCommitLoading(false);
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
              <FormField label="Copilot Metrics Files" description="Drop one or more JSON files here">
                <FileUpload
                  accept=".json"
                  onChange={({ detail }) => setCopilotFiles(detail.value)}
                  value={copilotFiles}
                  showFileLastModified
                  showFileSize
                  showFileThumbnail={false}
                  multiple={true}
                />
              </FormField>
              <Button
                variant="primary"
                loading={copilotLoading}
                disabled={copilotFiles.length === 0}
              >
                Upload Copilot Metrics
              </Button>
              {copilotUploads.length > 0 && (
                <Table
                  columnDefinitions={[
                    {
                      id: "filename",
                      header: "File name",
                      cell: (item: FileUploadStatus) => item.file.name,
                    },
                    {
                      id: "size",
                      header: "Size",
                      cell: (item: FileUploadStatus) => `${(item.file.size / 1024).toFixed(2)} KB`,
                    },
                    {
                      id: "status",
                      header: "Status",
                      cell: (item: FileUploadStatus) => {
                        if (item.status === 'pending') return <StatusIndicator>Pending</StatusIndicator>;
                        if (item.status === 'uploading') return <StatusIndicator type="in-progress">Uploading</StatusIndicator>;
                        if (item.status === 'success') return <StatusIndicator type="success">Success</StatusIndicator>;
                        if (item.status === 'error') return <StatusIndicator type="error">{item.error || 'Failed'}</StatusIndicator>;
                        return null;
                      },
                    },
                  ]}
                  items={copilotUploads}
                  variant="embedded"
                />
              )}
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
              <FormField label="Commit Metrics Files" description="Drop one or more XLSX files here">
                <FileUpload
                  accept=".xlsx"
                  onChange={({ detail }) => setCommitFiles(detail.value)}
                  value={commitFiles}
                  showFileLastModified
                  showFileSize
                  showFileThumbnail={false}
                  multiple={true}
                />
              </FormField>
              <Button
                variant="primary"
                loading={commitLoading}
                disabled={commitFiles.length === 0}
              >
                Upload Commit Metrics
              </Button>
              {commitUploads.length > 0 && (
                <Table
                  columnDefinitions={[
                    {
                      id: "filename",
                      header: "File name",
                      cell: (item: FileUploadStatus) => item.file.name,
                    },
                    {
                      id: "size",
                      header: "Size",
                      cell: (item: FileUploadStatus) => `${(item.file.size / 1024).toFixed(2)} KB`,
                    },
                    {
                      id: "status",
                      header: "Status",
                      cell: (item: FileUploadStatus) => {
                        if (item.status === 'pending') return <StatusIndicator>Pending</StatusIndicator>;
                        if (item.status === 'uploading') return <StatusIndicator type="in-progress">Uploading</StatusIndicator>;
                        if (item.status === 'success') return <StatusIndicator type="success">Success</StatusIndicator>;
                        if (item.status === 'error') return <StatusIndicator type="error">{item.error || 'Failed'}</StatusIndicator>;
                        return null;
                      },
                    },
                  ]}
                  items={commitUploads}
                  variant="embedded"
                />
              )}
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