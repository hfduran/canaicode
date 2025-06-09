import { DashboardData } from "../types/ui";

const mockDashboardData: DashboardData[] = [
  {
    team: "Team Alpha",
    languages: ["JavaScript", "Python"],
    period: "month",
    data: [
      {
        initial_date: new Date("2024-01-01"),
        final_date: new Date("2024-01-31"),
        net_changed_lines: 1500,
        percentage_changed_lines_by_copilot: 38,
        net_changed_lines_by_copilot: 0.38 * 1500,
        number_of_authors: 4,
      },
      {
        initial_date: new Date("2024-02-01"),
        final_date: new Date("2024-02-29"),
        net_changed_lines: 1700,
        percentage_changed_lines_by_copilot: 42,
        net_changed_lines_by_copilot: 0.42 * 1700,
        number_of_authors: 5,
      },
    ],
  },
  {
    team: "Team Beta",
    languages: ["Java", "C#"],
    period: "quarter",
    data: [
      {
        initial_date: new Date("2024-01-01"),
        final_date: new Date("2024-03-31"),
        net_changed_lines: 4500,
        percentage_changed_lines_by_copilot: 50,
        net_changed_lines_by_copilot: 0.5 * 4500,
        number_of_authors: 7,
      },
      {
        initial_date: new Date("2024-04-01"),
        final_date: new Date("2024-06-30"),
        net_changed_lines: 4800,
        percentage_changed_lines_by_copilot: 47,
        net_changed_lines_by_copilot: 0.47 * 4800,
        number_of_authors: 6,
      },
    ],
  },
  {
    team: "Team Gamma",
    languages: ["Go", "Rust"],
    period: "month",
    data: [
      {
        initial_date: new Date("2024-01-01"),
        final_date: new Date("2024-01-31"),
        net_changed_lines: 1200,
        percentage_changed_lines_by_copilot: 35,
        net_changed_lines_by_copilot: 0.35 * 1200,
        number_of_authors: 3,
      },
      {
        initial_date: new Date("2024-02-01"),
        final_date: new Date("2024-02-29"),
        net_changed_lines: 1300,
        percentage_changed_lines_by_copilot: 37,
        net_changed_lines_by_copilot: 0.37 * 1300,
        number_of_authors: 4,
      },
      {
        initial_date: new Date("2024-03-01"),
        final_date: new Date("2024-03-31"),
        net_changed_lines: 1400,
        percentage_changed_lines_by_copilot: 40,
        net_changed_lines_by_copilot: 0.4 * 1400,
        number_of_authors: 4,
      },
    ],
  },
  {
    team: "Team Delta",
    languages: ["TypeScript", "Python"],
    period: "week",
    data: [
      {
        initial_date: new Date("2024-04-01"),
        final_date: new Date("2024-04-07"),
        net_changed_lines: 300,
        percentage_changed_lines_by_copilot: 55,
        net_changed_lines_by_copilot: 0.55 * 300,
        number_of_authors: 2,
      },
      {
        initial_date: new Date("2024-04-08"),
        final_date: new Date("2024-04-14"),
        net_changed_lines: 350,
        percentage_changed_lines_by_copilot: 53,
        net_changed_lines_by_copilot: 0.53 * 350,
        number_of_authors: 2,
      },
      {
        initial_date: new Date("2024-04-15"),
        final_date: new Date("2024-04-21"),
        net_changed_lines: 400,
        percentage_changed_lines_by_copilot: 58,
        net_changed_lines_by_copilot: 0.58 * 400,
        number_of_authors: 3,
      },
    ],
  },
  {
    team: "Team Epsilon",
    languages: ["Ruby", "Elixir"],
    period: "6 months",
    data: [
      {
        initial_date: new Date("2024-01-01"),
        final_date: new Date("2024-06-30"),
        net_changed_lines: 9000,
        percentage_changed_lines_by_copilot: 44,
        net_changed_lines_by_copilot: 0.44 * 9000,
        number_of_authors: 8,
      },
    ],
  },
  {
    team: "Team Zeta",
    languages: ["C++", "C"],
    period: "year",
    data: [
      {
        initial_date: new Date("2024-01-01"),
        final_date: new Date("2024-12-31"),
        net_changed_lines: 21000,
        percentage_changed_lines_by_copilot: 48,
        net_changed_lines_by_copilot: 0.48 * 21000,
        number_of_authors: 15,
      },
    ],
  },
];

export default mockDashboardData;
