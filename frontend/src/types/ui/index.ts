import { CodeLineMetrics, CodeLineMetricsData, CommitMetrics, CommitMetricsData } from "../model";

export type DataEntry = CodeLineMetricsData | CommitMetricsData;

export type DashboardData = (Omit<CodeLineMetrics, 'period'> | Omit<CommitMetrics, 'period'>) & {
  period: string
}

export interface FlattenedDataEntry {
  team: string;
  period: string;
  programming_languages: string[];
  initial_date: Date;
  final_date: Date;
  number_of_authors: number;
  net_changed_lines: number;
  net_changed_lines_by_copilot: number;
  percentage_changed_lines_by_copilot: number;
  total_commits?: number;
}

export interface FormattedDataEntry extends Omit<FlattenedDataEntry, 'initial_date' | 'final_date'> {
  initial_date: string;
  final_date: string;
  net_changed_lines_without_copilot: number;
}

export interface Filters {
  programmingLanguages: string[];
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
