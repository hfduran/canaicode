import React, { useState } from "react";
import {
  DatePicker,
  FormField,
  Form,
  Select,
  SpaceBetween
} from "@cloudscape-design/components";

interface DateRangeSelectorProps {
  startDate: string;
  endDate: string;
  onStartDateChange: (date: string) => void;
  onEndDateChange: (date: string) => void;
  direction?: "horizontal" | "vertical";
}

const DateRangeSelector: React.FC<DateRangeSelectorProps> = ({
  startDate,
  endDate,
  onStartDateChange,
  onEndDateChange,
  direction = "horizontal"
}) => {
  const [selectedPeriod, setSelectedPeriod] = useState<string>("last_6_months");

  // Period options
  const periodOptions = [
    { label: "All time", value: "all_time" },
    { label: "Last year", value: "last_year" },
    { label: "Last 6 months", value: "last_6_months" },
    { label: "Last month", value: "last_month" },
    { label: "Last week", value: "last_week" },
  ];

  // Handle period change
  const handlePeriodChange = (period: string) => {
    setSelectedPeriod(period);
    const today = new Date();
    const startDateCalc = new Date();

    switch (period) {
      case "all_time":
        const allTimeStart = new Date(1900, 0, 1); // January 1, 1900
        onStartDateChange(allTimeStart.toISOString().split('T')[0]);
        onEndDateChange(today.toISOString().split('T')[0]);
        break;
      case "last_year":
        startDateCalc.setFullYear(today.getFullYear() - 1);
        onStartDateChange(startDateCalc.toISOString().split('T')[0]);
        onEndDateChange(today.toISOString().split('T')[0]);
        break;
      case "last_6_months":
        startDateCalc.setMonth(today.getMonth() - 6);
        onStartDateChange(startDateCalc.toISOString().split('T')[0]);
        onEndDateChange(today.toISOString().split('T')[0]);
        break;
      case "last_month":
        startDateCalc.setMonth(today.getMonth() - 1);
        onStartDateChange(startDateCalc.toISOString().split('T')[0]);
        onEndDateChange(today.toISOString().split('T')[0]);
        break;
      case "last_week":
        startDateCalc.setDate(today.getDate() - 7);
        onStartDateChange(startDateCalc.toISOString().split('T')[0]);
        onEndDateChange(today.toISOString().split('T')[0]);
        break;
    }
  };

  return (
    <Form>
      <SpaceBetween size="m" direction={direction}>
        <FormField label="Time period">
          <Select
            selectedOption={periodOptions.find(opt => opt.value === selectedPeriod) || periodOptions[2]}
            onChange={({ detail }) => handlePeriodChange(detail.selectedOption.value || "last_6_months")}
            options={periodOptions}
            placeholder="Select time period"
          />
        </FormField>
        <FormField label="Beginning period">
          <DatePicker
            value={startDate}
            onChange={({ detail }) => onStartDateChange(detail.value)}
            placeholder="YYYY-MM-DD"
            openCalendarAriaLabel={() => "Open calendar"}
          />
        </FormField>
        <FormField label="Ending period">
          <DatePicker
            value={endDate}
            onChange={({ detail }) => onEndDateChange(detail.value)}
            placeholder="YYYY-MM-DD"
            openCalendarAriaLabel={() => "Open calendar"}
          />
        </FormField>
      </SpaceBetween>
    </Form>
  );
};

export default DateRangeSelector;
