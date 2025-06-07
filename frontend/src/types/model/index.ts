export interface CalculatedDataEntry {
  initial_date: string;
  final_date: string;
  relative_added_lines: number;
  percentage_lines_added_by_copilot: number;
  number_of_authors: number;
}

export interface CalculatedDashboardData {
  team: string;
  languages: string[];
  period: string;
  data: CalculatedDataEntry[];
}

export interface CalculatedMetricsRequest {
  team_name: string;
  period: "W" | "M" | "Q" | "Y"; // Week, Month, Quarter, Year
  productivity_metric: "code_lines" | "commits";
  initial_date: Date;
  final_date: Date;
  languages?: string[];
}

export interface CodeLineMetricsData {
  initial_date: string;
  final_date: string;
  net_changed_lines: number;
  net_changed_lines_by_copilot: number;
  percentage_changed_lines_by_copilot: number;
  number_of_authors: number;
}

export interface CodeLineMetrics {
  team: string;
  languages: string[];
  period: "W" | "M" | "Q" | "Y";
  data: CodeLineMetricsData[];
}

export type CalculatedMetricsResponse = CodeLineMetrics | null;
