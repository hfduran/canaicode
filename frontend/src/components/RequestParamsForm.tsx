import React from "react";
import {
  Select,
  FormField,
  SpaceBetween,
  ColumnLayout,
} from "@cloudscape-design/components";
import DateRangeSelector from "./DateRangeSelector";

interface RequestParamsFormProps {
  timeRange: string;
  setTimeRange: (value: string) => void;
  metric: string;
  setMetric: (value: string) => void;
  initialDate: string;
  setInitialDate: (value: string) => void;
  finalDate: string;
  setFinalDate: (value: string) => void;
  programmingLanguages: string[];
  setProgrammingLanguages: (value: string[]) => void;
}

const RequestParamsForm: React.FC<RequestParamsFormProps> = ({
  timeRange,
  setTimeRange,
  metric,
  setMetric,
  initialDate,
  setInitialDate,
  finalDate,
  setFinalDate,
  programmingLanguages,
  setProgrammingLanguages,
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
    <ColumnLayout columns={2} variant="text-grid">
      <SpaceBetween direction="vertical" size="m">
        <FormField 
          label="Time Period"
          description="Select the time range for data aggregation"
        >
          <Select
            selectedOption={TIME_OPTIONS.find(option => option.value === timeRange) || null}
            onChange={({ detail }) => setTimeRange(detail.selectedOption?.value || "")}
            options={TIME_OPTIONS}
            placeholder="Select time period"
          />
        </FormField>

        <FormField
          label="Metric Type"
          description="Choose the type of metrics to analyze"
        >
          <Select
            selectedOption={METRIC_OPTIONS.find(option => option.value === metric) || null}
            onChange={({ detail }) => setMetric(detail.selectedOption?.value || "")}
            options={METRIC_OPTIONS}
            placeholder="Select metric option"
          />
        </FormField>
      </SpaceBetween>

      <SpaceBetween direction="vertical" size="m">
        <DateRangeSelector
          startDate={initialDate}
          endDate={finalDate}
          onStartDateChange={setInitialDate}
          onEndDateChange={setFinalDate}
          direction="vertical"
        />
      </SpaceBetween>
    </ColumnLayout>
  );
};

export default RequestParamsForm;
