import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Box, Header, Container, Input, FormField, Button, SpaceBetween, Alert } from "@cloudscape-design/components";
import GitHubAppService, { GitHubAppResponse } from "../services/gitHubAppService";
import { getUserId } from "../utils/auth";

const GitHubApp: React.FC = () => {
	const [organizationName, setOrganizationName] = useState("");
	const [appId, setAppId] = useState("");
	const [installationId, setInstallationId] = useState("");
	const [privateKey, setPrivateKey] = useState("");
	const [isLoading, setIsLoading] = useState(false);
	const [isDeleting, setIsDeleting] = useState(false);
	const [isFetching, setIsFetching] = useState(true);
	const [existingApp, setExistingApp] = useState<GitHubAppResponse | null>(null);
	const [successMsg, setSuccessMsg] = useState<string | null>(null);
	const [errorMsg, setErrorMsg] = useState<string | null>(null);

	const navigate = useNavigate();

	useEffect(() => {
		const userId = getUserId();
		if (!userId) navigate("/user-login");
		else loadExistingApp(userId);
	}, [navigate]);

	const loadExistingApp = async (userId: string) => {
		setIsFetching(true);
		try {
			const app = await GitHubAppService.findGitHubApp(userId);
			setExistingApp(app);
		} catch (err: any) {
			// If no app found, that's okay - just leave existingApp as null
			console.log("No existing GitHub App found or error fetching:", err);
		} finally {
			setIsFetching(false);
		}
	};

	const submit = async () => {
		const userId = getUserId();
		if (!userId) {
			setErrorMsg("Non-authenticated user.");
			return;
		}

		setErrorMsg(null);
		setSuccessMsg(null);

		if (!organizationName || !appId || !installationId || !privateKey) {
			setErrorMsg("Please fill all fields.");
			return;
		}

		setIsLoading(true);
		try {
			await GitHubAppService.createGitHubApp(userId, organizationName, appId, installationId, privateKey);
			setSuccessMsg("GitHub App saved successfully.");
			await loadExistingApp(userId);
			// Clear form
			setOrganizationName("");
			setAppId("");
			setInstallationId("");
			setPrivateKey("");
		} catch (err: any) {
			setErrorMsg(err?.response?.data?.detail || err.message || "Failed to save GitHub App.");
		} finally {
			setIsLoading(false);
		}
	};

	const handleDelete = async () => {
		const userId = getUserId();
		if (!userId || !existingApp) return;

		if (!window.confirm("Are you sure you want to delete this GitHub App? This action cannot be undone.")) {
			return;
		}

		setErrorMsg(null);
		setSuccessMsg(null);
		setIsDeleting(true);

		try {
			await GitHubAppService.deleteGitHubApp(userId, existingApp.id);
			setSuccessMsg("GitHub App deleted successfully.");
			setExistingApp(null);
		} catch (err: any) {
			setErrorMsg(err?.response?.data?.detail || err.message || "Failed to delete GitHub App.");
		} finally {
			setIsDeleting(false);
		}
	};

	return (
		<div style={{ height: "100%", display: "flex", alignItems: "center", justifyContent: "center", padding: 20, boxSizing: "border-box" }}>
			<div style={{ width: "100%", maxWidth: 1000, backgroundColor: "white", padding: 24, boxSizing: "border-box" }}>
				<Box margin={{ bottom: "l" }}>
					<Header variant="h1" description="Register a GitHub App installation so the backend can fetch data for your organization.">GitHub App</Header>
				</Box>

				{isFetching ? (
					<Container>
						<div style={{ padding: 20, textAlign: "center" }}>Loading...</div>
					</Container>
				) : (
					<>
						<Box margin={{ bottom: "l" }}>
							<Container header={<Header variant="h2">Current GitHub App</Header>}>
								{existingApp ? (
									<SpaceBetween size="m">
										<div>
											<div style={{ fontWeight: 600, marginBottom: 4 }}>Organization Name:</div>
											<div>{existingApp.organization_name}</div>
										</div>
										<div>
											<div style={{ fontWeight: 600, marginBottom: 4 }}>App ID:</div>
											<div>{existingApp.app_id}</div>
										</div>
										<div>
											<div style={{ fontWeight: 600, marginBottom: 4 }}>Installation ID:</div>
											<div>{existingApp.installation_id}</div>
										</div>
										<div>
											<div style={{ fontWeight: 600, marginBottom: 4 }}>Created At:</div>
											<div>{new Date(existingApp.created_at).toLocaleString()}</div>
										</div>
										<Alert type="warning">
											The private key is encrypted and cannot be displayed for security reasons.
										</Alert>
										<div style={{ display: "flex", justifyContent: "flex-end" }}>
											<Button loading={isDeleting} variant="primary" onClick={handleDelete}>Delete GitHub App</Button>
										</div>
									</SpaceBetween>
								) : (
									<Alert type="info">
										No GitHub App registered yet. Use the form below to register one.
									</Alert>
								)}
							</Container>
						</Box>

						<div style={{ display: "flex", gap: 24, alignItems: "flex-start", flexWrap: "wrap" }}>
							<div style={{ flex: "1 1 400px", minWidth: 320 }}>
								<Container header={<Header variant="h2">Register GitHub App</Header>} fitHeight>
									<form onSubmit={(e) => { e.preventDefault(); submit(); }}>
										<SpaceBetween size="m">
											<FormField label="Organization Name" constraintText="The GitHub organization where the app is installed.">
												<Input value={organizationName} onChange={({ detail }) => setOrganizationName(detail.value)} placeholder="my-org" autoComplete="organization" />
											</FormField>

											<FormField label="App ID" constraintText="The GitHub App ID (numeric).">
												<Input value={appId} onChange={({ detail }) => setAppId(detail.value)} placeholder="12345" />
											</FormField>

											<FormField label="Installation ID" constraintText="The installation id for the organization (numeric).">
												<Input value={installationId} onChange={({ detail }) => setInstallationId(detail.value)} placeholder="67890" />
											</FormField>

											<FormField label="Private Key" constraintText="PEM private key for the GitHub App (paste entire key).">
												<textarea value={privateKey} onChange={(e) => setPrivateKey(e.target.value)} placeholder={
		                      "-----BEGIN PRIVATE KEY-----\n...your private key here...\n-----END PRIVATE KEY-----"
		                      } style={{ width: "100%", minHeight: 160, padding: 8, boxSizing: "border-box", fontFamily: "monospace" }} />
											</FormField>

											{errorMsg && <div style={{ color: "#d13438", fontWeight: 600 }}>{errorMsg}</div>}
											{successMsg && <div style={{ color: "#0b8457", fontWeight: 600 }}>{successMsg}</div>}

											<div style={{ display: "flex", justifyContent: "flex-end", gap: 8 }}>
												<Button onClick={() => navigate(-1)} variant="link">Cancel</Button>
												<Button loading={isLoading} variant="primary" onClick={() => submit()}>Save</Button>
											</div>
										</SpaceBetween>
									</form>
								</Container>
							</div>

							<div style={{ flex: "0 1 400px", minWidth: 280 }}>
								<div style={{ padding: 16, borderRadius: 6 }}>
									<Header variant="h2">Tutorial</Header>
									<div style={{ marginTop: 8, marginBottom: 12, color: '#666', fontSize: 14 }}>
										Find below the instructions to locate the referenced data to be filled in the left form.
									</div>
									<Container>
											<ol style={{ paddingLeft: 18 }}>
												<li>
													<strong>Create the GitHub App</strong>
													<ol style={{ paddingLeft: 14, marginTop: 6 }}>
														<li>In the organization: go to <em>Developer settings &gt; GitHub Apps</em>.</li>
														<li>Click <strong>New GitHub App</strong>.</li>
														<li>Fill <em>GitHub App name</em>, <em>Homepage URL</em>; leave Webhook URL empty if not needed.</li>
														<li>Set permissions: <em>Organization &gt; Copilot Business Metrics</em> to <strong>Read-only</strong>.</li>
														<li>Choose <em>Where can this GitHub App be installed?</em> → <strong>Only on this account</strong>, then <strong>Create GitHub App</strong>.</li>
													</ol>
												</li>

												<li style={{ marginTop: 8 }}>
													<strong>Generate credentials</strong>
													<ol style={{ paddingLeft: 14, marginTop: 6 }}>
														<li>Under <em>Private keys</em> click <strong>Generate a private key</strong> — a <code>.pem</code> file will be downloaded.</li>
														<li>Copy the <strong>App ID</strong> (shown on the app page).</li>
														<li>Install the App into the organization via <strong>Install App</strong>.</li>
													</ol>
												</li>
											</ol>
									</Container>
								</div>
							</div>
						</div>
					</>
				)}
			</div>
		</div>
	);
};

export default GitHubApp;
