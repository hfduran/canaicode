// Data types for the metrics dashboard

import { CodeLineMetrics, CodeLineMetricsData } from "../model";

export interface DataEntry extends CodeLineMetricsData {}

export interface DashboardData extends Omit<CodeLineMetrics, 'period'> {
  period: string
}

export interface FlattenedDataEntry extends DataEntry {
  team: string;
  period: string;
  languages: string[];
}

export interface FormattedDataEntry extends Omit<FlattenedDataEntry, 'initial_date' | 'final_date'> {
  initial_date: string;
  final_date: string;
}

export interface Filters {
  languages: string[];
  teams: string[];
  initialDate: string;
  finalDate: string;
  period: string;
  numberOfAuthors: string;
}

export interface SelectOption {
  value: string;
  label: string;
}

export interface FiltersProps {
  filters: Filters;
  setFilters: (filters: Filters) => void;
  availableLanguages?: string[];
  availableTeams?: string[];
}

export interface DropdownButtonProps {
  options: string[];
  selected: string;
  setSelected: (value: string) => void;
  label: string;
}

export interface InputFormProps {
  value: string;
  setValue: (value: string) => void;
  label: string;
  placeholder?: string;
}
