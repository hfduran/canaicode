import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Box,
  Header,
  Container,
  Button,
  SpaceBetween,
  Table,
  Modal,
  FormField,
  Input,
  Alert,
  DateInput,
  Link,
} from "@cloudscape-design/components";
import ApiKeysService from "../services/apiKeysService";
import { ApiKey, ApiKeyCreateResponse } from "../types/model";
import { getUserId } from "../utils/auth";

const ApiKeys: React.FC = () => {
  const [apiKeys, setApiKeys] = useState<ApiKey[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [createModalVisible, setCreateModalVisible] = useState(false);
  const [deleteModalVisible, setDeleteModalVisible] = useState(false);
  const [keyToDelete, setKeyToDelete] = useState<ApiKey | null>(null);
  const [newKeyName, setNewKeyName] = useState("");
  const [newKeyExpiry, setNewKeyExpiry] = useState("");
  const [createdKey, setCreatedKey] = useState<ApiKeyCreateResponse | null>(null);
  const [isCreating, setIsCreating] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [copiedToClipboard, setCopiedToClipboard] = useState(false);
  const [githubIntegrationModalVisible, setGithubIntegrationModalVisible] = useState(false);
  const [copiedYaml, setCopiedYaml] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    const userId = getUserId();
    if (!userId) {
      navigate("/user-login");
      return;
    }
    loadApiKeys();
  }, [navigate]);

  const loadApiKeys = async () => {
    try {
      setIsLoading(true);
      setErrorMsg(null);
      const keys = await ApiKeysService.listApiKeys();
      setApiKeys(keys);
    } catch (err: any) {
      setErrorMsg(err?.response?.data?.detail || err.message || "Failed to load API keys");
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateKey = async () => {
    if (!newKeyName.trim()) {
      setErrorMsg("Please provide a name for the API key");
      return;
    }

    try {
      setIsCreating(true);
      setErrorMsg(null);

      // Convert date format from YYYY/MM/DD to YYYY-MM-DD
      const formattedExpiry = newKeyExpiry ? newKeyExpiry.replace(/\//g, '-') : undefined;

      const response = await ApiKeysService.createApiKey(
        newKeyName,
        formattedExpiry
      );
      setCreatedKey(response);
      setNewKeyName("");
      setNewKeyExpiry("");
      setCreateModalVisible(false);
      await loadApiKeys();
    } catch (err: any) {
      setErrorMsg(err?.response?.data?.detail || err.message || "Failed to create API key");
    } finally {
      setIsCreating(false);
    }
  };

  const handleDeleteKey = async () => {
    if (!keyToDelete) return;

    try {
      setIsDeleting(true);
      setErrorMsg(null);
      await ApiKeysService.revokeApiKey(keyToDelete.id);
      setDeleteModalVisible(false);
      setKeyToDelete(null);
      await loadApiKeys();
    } catch (err: any) {
      setErrorMsg(err?.response?.data?.detail || err.message || "Failed to revoke API key");
    } finally {
      setIsDeleting(false);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedToClipboard(true);
    setTimeout(() => setCopiedToClipboard(false), 2000);
  };

  const copyYamlToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedYaml(true);
    setTimeout(() => setCopiedYaml(false), 2000);
  };

  const formatDate = (dateString: string | null) => {
    if (!dateString) return "Never";
    return new Date(dateString).toLocaleString();
  };

  const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";
  const UPLOAD_ENDPOINT = `${API_BASE_URL}/commit_metrics/upload`;

  const workflowYaml = `name: Extract Commits

on:
  schedule:
    - cron: '0 1 * * *'  # Daily at 1 AM UTC
  workflow_dispatch:

jobs:
  extract:
    uses: hfduran/canaicode-git-extractor/.github/workflows/extract-and-upload-reusable.yml@main
    secrets:
      upload_url: \${{ secrets.UPLOAD_ENDPOINT_URL }}
      upload_key: \${{ secrets.UPLOAD_AUTH_KEY }}
      user_id: \${{ secrets.USER_ID }}`;

  return (
    <div style={{ padding: 20 }}>
      <SpaceBetween size="l">
        <Header
          variant="h1"
          description="Create and manage API keys for programmatic access to the Copilot Metrics Upload endpoint."
          actions={
            <SpaceBetween direction="horizontal" size="xs">
              <Button onClick={() => setGithubIntegrationModalVisible(true)}>
                Integrate with GitHub
              </Button>
              <Button variant="primary" onClick={() => setCreateModalVisible(true)}>
                Create API Key
              </Button>
            </SpaceBetween>
          }
        >
          API Keys
        </Header>

        {errorMsg && (
          <Alert type="error" dismissible onDismiss={() => setErrorMsg(null)}>
            {errorMsg}
          </Alert>
        )}

        {createdKey && (
          <Alert
            type="success"
            dismissible
            onDismiss={() => setCreatedKey(null)}
            header="API Key Created Successfully"
          >
            <div style={{ marginBottom: 8 }}>
              <strong>Key Name:</strong> {createdKey.key_name}
            </div>
            <div style={{ marginBottom: 12 }}>
              <strong>This is your only chance to copy this key:</strong>
            </div>
            <div
              style={{
                fontFamily: "monospace",
                background: "#f0f0f0",
                padding: 12,
                borderRadius: 4,
                wordBreak: "break-all",
                marginBottom: 8,
              }}
            >
              {createdKey.key}
            </div>
            <Button
              iconName={copiedToClipboard ? "status-positive" : "copy"}
              onClick={() => copyToClipboard(createdKey.key)}
            >
              {copiedToClipboard ? "Copied!" : "Copy to Clipboard"}
            </Button>
          </Alert>
        )}

        <Container>
          <Table
            loading={isLoading}
            columnDefinitions={[
              {
                id: "name",
                header: "Name",
                cell: (item) => item.key_name,
              },
              {
                id: "key",
                header: "Key",
                cell: (item) => (
                  <span style={{ fontFamily: "monospace", fontSize: "0.9em" }}>
                    {item.key_prefix}
                  </span>
                ),
              },
              {
                id: "created",
                header: "Created",
                cell: (item) => formatDate(item.created_at),
              },
              {
                id: "last_used",
                header: "Last Used",
                cell: (item) => formatDate(item.last_used_at),
              },
              {
                id: "expires",
                header: "Expires",
                cell: (item) => formatDate(item.expires_at),
              },
              {
                id: "actions",
                header: "Actions",
                cell: (item) => (
                  <Button
                    variant="normal"
                    onClick={() => {
                      setKeyToDelete(item);
                      setDeleteModalVisible(true);
                    }}
                  >
                    Delete
                  </Button>
                ),
              },
            ]}
            items={apiKeys}
            empty={
              <Box textAlign="center" color="inherit">
                <b>No API keys</b>
                <Box padding={{ bottom: "s" }} variant="p" color="inherit">
                  No API keys found. Create one to get started.
                </Box>
              </Box>
            }
          />
        </Container>
      </SpaceBetween>

      {/* Create Modal */}
      <Modal
        visible={createModalVisible}
        onDismiss={() => {
          setCreateModalVisible(false);
          setNewKeyName("");
          setNewKeyExpiry("");
        }}
        header="Create API Key"
        footer={
          <Box float="right">
            <SpaceBetween direction="horizontal" size="xs">
              <Button
                variant="link"
                onClick={() => {
                  setCreateModalVisible(false);
                  setNewKeyName("");
                  setNewKeyExpiry("");
                }}
              >
                Cancel
              </Button>
              <Button variant="primary" onClick={handleCreateKey} loading={isCreating}>
                Create
              </Button>
            </SpaceBetween>
          </Box>
        }
      >
        <SpaceBetween size="m">
          <FormField
            label="Key Name"
            description="A descriptive name to identify this API key"
          >
            <Input
              value={newKeyName}
              onChange={({ detail }) => setNewKeyName(detail.value)}
              placeholder="e.g., Production Server"
            />
          </FormField>

          <FormField
            label="Expiration Date (Optional)"
            constraintText="Use YYYY/MM/DD format."
            description="Leave empty for no expiration"
          >
            <DateInput
              value={newKeyExpiry}
              onChange={({ detail }) => setNewKeyExpiry(detail.value)}
              placeholder="YYYY/MM/DD"
            />
          </FormField>
        </SpaceBetween>
      </Modal>

      {/* Delete Modal */}
      <Modal
        visible={deleteModalVisible}
        onDismiss={() => {
          setDeleteModalVisible(false);
          setKeyToDelete(null);
        }}
        header="Delete API Key"
        footer={
          <Box float="right">
            <SpaceBetween direction="horizontal" size="xs">
              <Button
                variant="link"
                onClick={() => {
                  setDeleteModalVisible(false);
                  setKeyToDelete(null);
                }}
              >
                Cancel
              </Button>
              <Button variant="primary" onClick={handleDeleteKey} loading={isDeleting}>
                Delete
              </Button>
            </SpaceBetween>
          </Box>
        }
      >
        {keyToDelete && (
          <Box>
            <Alert type="warning">
              Are you sure you want to delete the API key "{keyToDelete.key_name}"? This
              action cannot be undone and any applications using this key will lose access.
            </Alert>
          </Box>
        )}
      </Modal>

      {/* GitHub Integration Modal */}
      <Modal
        visible={githubIntegrationModalVisible}
        onDismiss={() => setGithubIntegrationModalVisible(false)}
        size="large"
        header="Integrate with GitHub Actions"
        footer={
          <Box float="right">
            <SpaceBetween direction="horizontal" size="xs">
              <Button
                variant="link"
                iconName="external"
                iconAlign="right"
                href="https://github.com/hfduran/canaicode-git-extractor/blob/main/SETUP.md"
                target="_blank"
              >
                View Full Documentation
              </Button>
              <Button variant="primary" onClick={() => setGithubIntegrationModalVisible(false)}>
                Close
              </Button>
            </SpaceBetween>
          </Box>
        }
      >
        <SpaceBetween size="l">
          <Box>
            <p>
              Automate commit extraction from your repositories using{" "}
              <Link external href="https://github.com/hfduran/canaicode-git-extractor">
                canaicode-git-extractor
              </Link>
              . This GitHub Actions workflow will extract commits daily and upload them automatically.
            </p>
          </Box>

          <Alert type="info">
            You'll need an API key to authenticate the uploads. Create one using the "Create API Key" button above.
          </Alert>

          <Container header={<Header variant="h3">Step 1: Add GitHub Secrets</Header>}>
            <SpaceBetween size="m">
              <p>
                In your repository, go to <strong>Settings → Secrets and variables → Actions</strong> and add these secrets:
              </p>
              <div>
                <strong>UPLOAD_ENDPOINT_URL</strong>
                <div
                  style={{
                    fontFamily: "monospace",
                    background: "#f0f0f0",
                    padding: 8,
                    borderRadius: 4,
                    marginTop: 4,
                    wordBreak: "break-all",
                  }}
                >
                  {UPLOAD_ENDPOINT}
                </div>
              </div>
              <div>
                <strong>UPLOAD_AUTH_KEY</strong>
                <div
                  style={{
                    fontFamily: "monospace",
                    background: "#f0f0f0",
                    padding: 8,
                    borderRadius: 4,
                    marginTop: 4,
                  }}
                >
                  Your API key
                </div>
              </div>
              <div>
                <strong>USER_ID</strong>
                <div
                  style={{
                    fontFamily: "monospace",
                    background: "#f0f0f0",
                    padding: 8,
                    borderRadius: 4,
                    marginTop: 4,
                  }}
                >
                  {getUserId()}
                </div>
              </div>
            </SpaceBetween>
          </Container>

          <Container header={<Header variant="h3">Step 2: Create Workflow File</Header>}>
            <SpaceBetween size="m">
              <p>
                Create <code>.github/workflows/extract-commits.yml</code> in your repository:
              </p>
              <div>
                <pre
                  style={{
                    fontFamily: "monospace",
                    background: "#f0f0f0",
                    padding: 12,
                    borderRadius: 4,
                    overflow: "auto",
                    fontSize: "0.9em",
                  }}
                >
                  {workflowYaml}
                </pre>
                <div style={{ marginTop: 8 }}>
                  <Button
                    iconName={copiedYaml ? "status-positive" : "copy"}
                    onClick={() => copyYamlToClipboard(workflowYaml)}
                  >
                    {copiedYaml ? "Copied!" : "Copy YAML"}
                  </Button>
                </div>
              </div>
            </SpaceBetween>
          </Container>

          <Container header={<Header variant="h3">Step 3: Commit and Done!</Header>}>
            <SpaceBetween size="m">
              <p>
                Commit and push the workflow file. The workflow will run daily at 1 AM UTC, or you can trigger it manually from the Actions tab.
              </p>
              <div>
                <strong>What it does:</strong>
                <ul style={{ paddingLeft: 20, marginTop: 8 }}>
                  <li>Extracts commits from your repository</li>
                  <li>Creates an Excel file with commit data</li>
                  <li>Uploads it to your endpoint using the API key</li>
                  <li>Saves a backup in GitHub Actions artifacts (30 days)</li>
                </ul>
              </div>
            </SpaceBetween>
          </Container>

          <Alert type="success">
            For advanced options (multiple repositories, custom date ranges, etc.), see the{" "}
            <Link external href="https://github.com/hfduran/canaicode-git-extractor/blob/main/SETUP.md">
              full documentation
            </Link>
            .
          </Alert>
        </SpaceBetween>
      </Modal>
    </div>
  );
};

export default ApiKeys;
