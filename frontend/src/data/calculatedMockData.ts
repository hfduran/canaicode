import { CalculatedDashboardData } from '../types';

const calculatedMockData_1: CalculatedDashboardData[] = [
    {
        team: "Team Alpha",
        languages: ["JavaScript", "Python"],
        period: "month",
        data: [
            {
                initial_date: "2024-01-01",
                final_date: "2024-01-31",
                relative_added_lines: 1500,
                percentage_lines_added_by_copilot: 38,
                number_of_authors: 4
            },
            {
                initial_date: "2024-02-01",
                final_date: "2024-02-29",
                relative_added_lines: 1700,
                percentage_lines_added_by_copilot: 42,
                number_of_authors: 5
            },
            {
                initial_date: "2024-03-01",
                final_date: "2024-03-31",
                relative_added_lines: 2100,
                percentage_lines_added_by_copilot: 71,
                number_of_authors: 6
            },
            {
                initial_date: "2024-04-01",
                final_date: "2024-04-30",
                relative_added_lines: 1650,
                percentage_lines_added_by_copilot: 63,
                number_of_authors: 3
            }
        ]
    },
    {
        team: "Team Alpha",
        languages: ["JavaScript", "Python"],
        period: "Week",
        data: [
            {
                initial_date: "2024-01-01",
                final_date: "2024-01-07",
                relative_added_lines: 1500,
                percentage_lines_added_by_copilot: 38,
                number_of_authors: 4
            },
            {
                initial_date: "2024-01-08",
                final_date: "2024-01-14",
                relative_added_lines: 1600,
                percentage_lines_added_by_copilot: 41,
                number_of_authors: 5
            },
            {
                initial_date: "2024-01-15",
                final_date: "2024-01-21",
                relative_added_lines: 1700,
                percentage_lines_added_by_copilot: 40,
                number_of_authors: 5
            },
            {
                initial_date: "2024-01-22",
                final_date: "2024-01-28",
                relative_added_lines: 1800,
                percentage_lines_added_by_copilot: 47,
                number_of_authors: 4
            }
        ]
    },
    {
        team: "Team Beta",
        languages: ["Java", "C++"],
        period: "week",
        data: [
            {
                initial_date: "2024-01-01",
                final_date: "2024-01-31",
                relative_added_lines: 2200,
                percentage_lines_added_by_copilot: 62,
                number_of_authors: 4
            },
            {
                initial_date: "2024-02-01",
                final_date: "2024-02-29",
                relative_added_lines: 2700,
                percentage_lines_added_by_copilot: 63,
                number_of_authors: 5
            },
            {
                initial_date: "2024-03-01",
                final_date: "2024-03-31",
                relative_added_lines: 2450,
                percentage_lines_added_by_copilot: 81,
                number_of_authors: 6
            },
            {
                initial_date: "2024-04-01",
                final_date: "2024-04-30",
                relative_added_lines: 2200,
                percentage_lines_added_by_copilot: 53,
                number_of_authors: 3
            }
        ]
    }
];

export default calculatedMockData_1;
