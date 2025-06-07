// Data types for the metrics dashboard

export interface DataEntry {
  initial_date: string;
  final_date: string;
  relative_added_lines: number;
  percentage_lines_added_by_copilot: number;
  relative_added_lines_by_copilot: number;
  number_of_authors: number;
}

export interface DashboardData {
  team: string;
  languages: string[];
  period: string;
  data: DataEntry[];
}

export interface FlattenedDataEntry extends DataEntry {
  team: string;
  period: string;
  languages: string[];
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

export interface RequestDataButtonProps {
  timeOptions: string[];
  teamOptions: string[];
}
export interface DropdownButtonProps {
  options: string[];
  selected: string;
  setSelected: (value: string) => void;
  label: string;
}
