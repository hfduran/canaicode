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
  programming_languages?: string[];
}

export interface CodeLineMetricsData {
  initial_date: Date;
  final_date: Date;
  net_changed_lines: number;
  net_changed_lines_by_copilot: number;
  percentage_changed_lines_by_copilot: number;
  number_of_authors: number;
}

export interface CodeLineMetrics {
  programming_languages: string[];
  team: string;
  period: "W" | "M" | "Q" | "Y";
  data: CodeLineMetricsData[];
}

export type CalculatedMetricsResponse = CodeLineMetrics | null;

export interface CopilotMetricsByLanguage {
  language: string;
  code_acceptances: number;
  code_suggestions: number;
  lines_accepted: number;
  lines_suggested: number;
  percentage_code_acceptances: number;
  percentage_lines_accepted: number;
}

export interface CopilotUsersMetrics {
  date: Date;
  total_code_assistant_users: number;
  total_chat_users: number;
}

export interface CopilotMetricsByPeriod {
  period_initial_date: string;
  period_final_date: string;
  percentage_code_acceptances: number;
  total_code_acceptances: number;
  percentage_lines_accepted: number;
  total_lines_accepted: number;
}

export interface ApiKey {
  id: string;
  key_prefix: string;
  key_name: string;
  created_at: string;
  last_used_at: string | null;
  expires_at: string | null;
}

export interface ApiKeyCreateResponse {
  id: string;
  key: string;
  key_name: string;
  created_at: string;
  expires_at: string | null;
}
