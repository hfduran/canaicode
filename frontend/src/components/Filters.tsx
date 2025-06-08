import React from "react";
import { 
  Multiselect, 
  DatePicker, 
  Select, 
  Input, 
  FormField, 
  SpaceBetween,
  Header 
} from "@cloudscape-design/components";
import { FiltersProps } from "../types/ui";

const Filters: React.FC<FiltersProps> = ({
  filters,
  setFilters,
  availableLanguages = [],
  availableTeams = [],
}) => {
  // Convert arrays to CloudScape option format
  const languageOptions = availableLanguages.map((lang) => ({
    label: lang,
    value: lang,
  }));
  
  const teamOptions = availableTeams.map((team) => ({
    label: team,
    value: team,
  }));

  const periodOptions = [
    { label: "All", value: "" },
    { label: "Week", value: "week" },
    { label: "Month", value: "month" },
    { label: "Quarter", value: "quarter" },
    { label: "6 Months", value: "6 months" },
    { label: "Year", value: "year" },
  ];

  return (
    <SpaceBetween direction="vertical" size="m">
      <Header variant="h3">Filters</Header>

      <FormField label="Languages">
        <Multiselect
          selectedOptions={languageOptions.filter((opt) => 
            filters.languages.includes(opt.value)
          )}
          onChange={({ detail }) => {
            const selectedValues = detail.selectedOptions.map(opt => opt.value || '');
            setFilters({ ...filters, languages: selectedValues });
          }}
          options={languageOptions}
          placeholder="Choose languages"
          selectedAriaLabel="Selected languages"
        />
      </FormField>

      <FormField label="Teams">
        <Multiselect
          selectedOptions={teamOptions.filter((opt) => 
            filters.teams.includes(opt.value)
          )}
          onChange={({ detail }) => {
            const selectedValues = detail.selectedOptions.map(opt => opt.value || '');
            setFilters({ ...filters, teams: selectedValues });
          }}
          options={teamOptions}
          placeholder="Choose teams"
          selectedAriaLabel="Selected teams"
        />
      </FormField>

      <FormField label="Initial Date">
        <DatePicker
          value={filters.initialDate}
          onChange={({ detail }) => 
            setFilters({ ...filters, initialDate: detail.value })
          }
          placeholder="YYYY-MM-DD"
        />
      </FormField>

      <FormField label="Final Date">
        <DatePicker
          value={filters.finalDate}
          onChange={({ detail }) => 
            setFilters({ ...filters, finalDate: detail.value })
          }
          placeholder="YYYY-MM-DD"
        />
      </FormField>

      <FormField label="Period">
        <Select
          selectedOption={periodOptions.find(opt => opt.value === filters.period) || null}
          onChange={({ detail }) => 
            setFilters({ ...filters, period: detail.selectedOption?.value || "" })
          }
          options={periodOptions}
          placeholder="Select period"
        />
      </FormField>

      <FormField label="Number of Authors">
        <Input
          value={filters.numberOfAuthors}
          onChange={({ detail }) => {
            const value = detail.value;
            if (value === '' || (Number(value) >= 0 && !isNaN(Number(value)))) {
              setFilters({ ...filters, numberOfAuthors: value });
            }
          }}
          type="number"
          placeholder="Enter number of authors"
          inputMode="numeric"
        />
      </FormField>
    </SpaceBetween>
  );
};

export default Filters;
