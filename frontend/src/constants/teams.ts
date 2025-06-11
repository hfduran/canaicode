// Team configuration constants for the application
export const TEAMS = [
  "frontend-team",
  "backend-team", 
  "data-team",
  "devops-team",
  "mobile-team"
] as const;

export type TeamType = typeof TEAMS[number];

export const TEAM_OPTIONS = TEAMS.map(team => ({
  label: team.split('-').map(word => 
    word.charAt(0).toUpperCase() + word.slice(1)
  ).join(' '),
  value: team
}));
