import React from "react";
import { Select, Input, DatePicker, FormField, SpaceBetween } from "@cloudscape-design/components";

interface RequestParamsFormProps {
  timeRange: string;
  setTimeRange: (value: string) => void;
  team: string;
  setTeam: (value: string) => void;
  metric: string;
  setMetric: (value: string) => void;
  initialDate: string;
  setInitialDate: (value: string) => void;
  finalDate: string;
  setFinalDate: (value: string) => void;
}

const RequestParamsForm: React.FC<RequestParamsFormProps> = ({
  timeRange,
  setTimeRange,
  team,
  setTeam,
  metric,
  setMetric,
  initialDate,
  setInitialDate,
  finalDate,
  setFinalDate
}) => {
  const TIME_OPTIONS = [
    { label: "Week", value: "Week" },
    { label: "Month", value: "Month" },
    { label: "Year", value: "Year" },
    { label: "Semester", value: "Semester" }
  ];
  
  const METRIC_OPTIONS = [
    { label: "Code Lines", value: "Codelines" },
    { label: "Commits", value: "Commit" }
  ];

  return (
    <SpaceBetween direction="vertical" size="m">
      <FormField label="Time Period">
        <Select
          selectedOption={TIME_OPTIONS.find(option => option.value === timeRange) || null}
          onChange={({ detail }) => setTimeRange(detail.selectedOption?.value || "")}
          options={TIME_OPTIONS}
          placeholder="Select time period"
        />
      </FormField>

      <FormField label="Metric Type">
        <Select
          selectedOption={METRIC_OPTIONS.find(option => option.value === metric) || null}
          onChange={({ detail }) => setMetric(detail.selectedOption?.value || "")}
          options={METRIC_OPTIONS}
          placeholder="Select metric option"
        />
      </FormField>

      <FormField label="Developer Team">
        <Input
          value={team}
          onChange={({ detail }) => setTeam(detail.value)}
          placeholder="e.g., Team Alpha, Team Beta"
        />
      </FormField>

      <FormField label="Initial Date">
        <DatePicker
          value={initialDate}
          onChange={({ detail }) => setInitialDate(detail.value)}
          placeholder="YYYY-MM-DD"
        />
      </FormField>

      <FormField label="Final Date">
        <DatePicker
          value={finalDate}
          onChange={({ detail }) => setFinalDate(detail.value)}
          placeholder="YYYY-MM-DD"
        />
      </FormField>
    </SpaceBetween>
  );
};

export default RequestParamsForm;
