// Programming languages configuration constants for the application
export const PROGRAMMING_LANGUAGES = [
  "Python",
  "Java",
  "JavaScript",
  "C",
  "C++",
  "C#",
  "Golang",
  "Rust",
  "Swift",
  "Kotlin",
  "PHP",
  "Ruby",
  "Dart",
  "Scala",
  "Julia",
  "Haskell",
  "Erlang",
  "Clojure",
  "Bash",
  "Perl",
  "PowerShell",
  "Lua",
  "VBA",
  "R",
  "TypeScript"
] as const;

export type ProgrammingLanguageType = typeof PROGRAMMING_LANGUAGES[number];

export const PROGRAMMING_LANGUAGES_OPTIONS = PROGRAMMING_LANGUAGES.map(lang => ({
  label: lang,
  value: lang
}));

