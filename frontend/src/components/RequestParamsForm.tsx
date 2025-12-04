import React from "react";
import {
  Select,
  Multiselect,
  FormField,
  SpaceBetween,
  ColumnLayout,
  Button
} from "@cloudscape-design/components";
import { PROGRAMMING_LANGUAGES_OPTIONS } from "../constants/programming_languages";
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

        <FormField
          label="Programming Languages (Optional)"
          description="Select the programming languages to analyze"
        >
          <SpaceBetween direction="vertical" size="xs">
            <Multiselect
              selectedOptions={PROGRAMMING_LANGUAGES_OPTIONS.filter(option => programmingLanguages.includes(option.value))}
              onChange={({ detail }) => setProgrammingLanguages(detail.selectedOptions.map(option => option.value).filter((value): value is string => typeof value === "string"))}
              options={PROGRAMMING_LANGUAGES_OPTIONS}
              placeholder="Select programming languages"
            />
            <SpaceBetween direction="horizontal" size="xs">
              <Button
                variant="normal"
                onClick={() => {
                  const allLanguages = PROGRAMMING_LANGUAGES_OPTIONS.map(option => option.value as string);
                  setProgrammingLanguages(allLanguages);
                }}
              >
                Select All
              </Button>
              <Button
                variant="normal"
                onClick={() => setProgrammingLanguages([])}
              >
                Select None
              </Button>
            </SpaceBetween>
          </SpaceBetween>
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
