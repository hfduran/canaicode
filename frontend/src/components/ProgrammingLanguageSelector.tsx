import React from "react";
import {
  Multiselect,
  FormField,
  SpaceBetween,
  Button,
  MultiselectProps,
} from "@cloudscape-design/components";
import { PROGRAMMING_LANGUAGES_OPTIONS } from "../constants/programming_languages";

interface ProgrammingLanguageSelectorProps {
  selectedLanguages: string[];
  onSelectedLanguagesChange: (languages: string[]) => void;
  label?: string;
  description?: string;
  enableDynamicDisabling?: boolean;
  availableLanguages?: Set<string>;
}

const ProgrammingLanguageSelector: React.FC<ProgrammingLanguageSelectorProps> = ({
  selectedLanguages,
  onSelectedLanguagesChange,
  label = "Programming Languages",
  description = "Select programming languages to analyze",
  enableDynamicDisabling = false,
  availableLanguages,
}) => {
  // Create dynamic language options with disabled state if needed
  const languageOptions: MultiselectProps.Option[] = enableDynamicDisabling && availableLanguages
    ? PROGRAMMING_LANGUAGES_OPTIONS.map(option => ({
        label: option.label,
        value: option.value,
        disabled: !availableLanguages.has(option.value),
        disabledReason: !availableLanguages.has(option.value)
          ? "No data available for this language"
          : undefined,
      }))
    : PROGRAMMING_LANGUAGES_OPTIONS;

  const handleSelectAll = () => {
    if (enableDynamicDisabling && availableLanguages) {
      // Only select available (non-disabled) languages
      const allAvailableLanguages = languageOptions
        .filter(option => !option.disabled)
        .map(option => option.value as string);
      onSelectedLanguagesChange(allAvailableLanguages);
    } else {
      // Select all languages
      const allLanguages = PROGRAMMING_LANGUAGES_OPTIONS.map(option => option.value as string);
      onSelectedLanguagesChange(allLanguages);
    }
  };

  const handleSelectNone = () => {
    onSelectedLanguagesChange([]);
  };

  return (
    <FormField label={label} description={description}>
      <SpaceBetween direction="vertical" size="xs">
        <Multiselect
          selectedOptions={languageOptions.filter(option =>
            selectedLanguages.includes(option.value as string)
          )}
          onChange={({ detail }) =>
            onSelectedLanguagesChange(
              detail.selectedOptions.map(option => option.value).filter((value): value is string => typeof value === "string")
            )
          }
          options={languageOptions}
          placeholder="Select programming languages"
        />
        <SpaceBetween direction="horizontal" size="xs">
          <Button variant="normal" onClick={handleSelectAll}>
            Select All
          </Button>
          <Button variant="normal" onClick={handleSelectNone}>
            Select None
          </Button>
        </SpaceBetween>
      </SpaceBetween>
    </FormField>
  );
};

export default ProgrammingLanguageSelector;
