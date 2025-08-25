import React, { useState } from "react";
import {
  Header,
  ContentLayout,
  Tabs
} from "@cloudscape-design/components";
import CopilotUsageChart from "../components/CopilotUsageChart";
import SuggestionAcceptanceChart from "../components/SuggestionAcceptanceChart";

const CopilotAnalytics: React.FC = () => {
  const [activeTabId, setActiveTabId] = useState("usage-chart");

  return (
    <div style={{ marginBottom: '25px' }}>
      <ContentLayout
        header={
          <Header
            variant="h1"
            description="Analyze GitHub Copilot Usage throughout time"
          >
            Copilot Usage Analytics
          </Header>
        }
        defaultPadding={true}
      >
        <Tabs
          activeTabId={activeTabId}
          onChange={({ detail }) => setActiveTabId(detail.activeTabId)}
          tabs={[
            {
              label: "Usage Chart",
              id: "usage-chart",
              content: <CopilotUsageChart />
            },
            {
              label: "Suggestion Acceptance Chart",
              id: "suggestion-acceptance-chart",
              content: <SuggestionAcceptanceChart />
            }
          ]}
        />
      </ContentLayout>
    </div>
  );
};

export default CopilotAnalytics;
