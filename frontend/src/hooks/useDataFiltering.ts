import { useState, useEffect } from "react";
import { DashboardData, Filters as FiltersType, FlattenedDataEntry } from "../types/ui";

export const DEFAULT_FILTERS: FiltersType = {
  programmingLanguages: [],
  teams: [],
  initialDate: "",
  finalDate: "",
  period: "",
  numberOfAuthors: "",
};

interface UseDataFilteringResult {
  filteredData: FlattenedDataEntry[];
  availableLanguages: Set<string>;
  availableTeams: Set<string>;
  resetFilters: () => void;
  // Modal filtering functionality
  tempFilters: FiltersType;
  setTempFilters: (filters: FiltersType) => void;
  handleApplyFilters: () => void;
  handleCancelFilters: () => void;
  handleResetFilters: () => void;
}

export const useDataFiltering = (data: DashboardData[], done: () => void): UseDataFilteringResult => {
  const [filters, setFilters] = useState<FiltersType>(DEFAULT_FILTERS);
  const [filteredData, setFilteredData] = useState<FlattenedDataEntry[]>([]);
  const [availableLanguages, setAvailableLanguages] = useState<Set<string>>(new Set());
  const [availableTeams, setAvailableTeams] = useState<Set<string>>(new Set());
  const [tempFilters, setTempFilters] = useState<FiltersType>(filters);

  // Update available options when requestData changes
  useEffect(() => {
    setAvailableLanguages(new Set(data.flatMap((item) => item.programming_languages)));
    setAvailableTeams(new Set(data.map((item) => item.team)));
  }, [data]);

  // Filter and flatten data when filters or requestData changes
  useEffect(() => {
    const filtered = data.filter((item) => {
      const selectedProgrammingLanguages = filters.programmingLanguages ?? [];

      return (
        (selectedProgrammingLanguages.length === 0 || selectedProgrammingLanguages.some((lang) => item.programming_languages.includes(lang))) &&
        (filters.teams.length === 0 || filters.teams.includes(item.team)) &&
        (filters.period === "" || filters.period === item.period)
      );
    });

    const flattened = filtered.flatMap((item) =>
      item.data
        .filter(
          (entry) =>
            (!filters.numberOfAuthors ||
              Number(filters.numberOfAuthors) === entry.number_of_authors) &&
            (!filters.initialDate ||
              entry.initial_date >= new Date(filters.initialDate)) &&
            (!filters.finalDate || new Date(entry.final_date) <= new Date(filters.finalDate))
        )
        .map((entry) => ({
          ...entry,
          team: item.team,
          period: item.period,
          programming_languages: item.programming_languages,
        }))
    );

    setFilteredData(flattened);
  }, [filters, data]);

  const resetFilters = () => {
    setFilters(DEFAULT_FILTERS);
  };

  const handleApplyFilters = () => {
    setFilters(tempFilters);
    done();
  };

  const handleCancelFilters = () => {
    setTempFilters(filters);
    done();
  };

  const handleResetFilters = () => {
    setTempFilters(DEFAULT_FILTERS);
  };

  return {
    filteredData,
    availableLanguages,
    availableTeams,
    resetFilters,
    tempFilters,
    setTempFilters,
    handleApplyFilters,
    handleCancelFilters,
    handleResetFilters,
  };
};
