import React from 'react';
import Select, { MultiValue } from 'react-select';
import './Filters.css';
import { FiltersProps, SelectOption } from '../types';

const Filters: React.FC<FiltersProps> = ({
  filters,
  setFilters,
  availableLanguages = [],
  availableTeams = []
}) => {

  const handleMultiSelectChange = (selectedOptions: MultiValue<SelectOption>, field: keyof typeof filters) => {
    const values = selectedOptions ? selectedOptions.map(option => option.value) : [];
    setFilters({ ...filters, [field]: values });
  };

  const languageOptions: SelectOption[] = availableLanguages.map(lang => ({ value: lang, label: lang }));
  const teamOptions: SelectOption[] = availableTeams.map(team => ({ value: team, label: team }));

  return (
    <div className="filters-container">
      <h3>Filters</h3>

      <div className="filter-group">
        <label>Languages:</label>
        <Select
          isMulti
          name="languages"
          options={languageOptions}
          value={languageOptions.filter(opt => filters.languages.includes(opt.value))}
          onChange={(selected) => handleMultiSelectChange(selected, 'languages')}
        />
      </div>

      <div className="filter-group">
        <label>Teams:</label>
        <Select
          isMulti
          name="teams"
          options={teamOptions}
          value={teamOptions.filter(opt => filters.teams.includes(opt.value))}
          onChange={(selected) => handleMultiSelectChange(selected, 'teams')}
        />
      </div>

      <div className="filter-group">
        <label>Initial Date:</label>
        <input
          type="date"
          value={filters.initialDate}
          onChange={(e) => setFilters({ ...filters, initialDate: e.target.value })}
        />
      </div>

      <div className="filter-group">
        <label>Final Date:</label>
        <input
          type="date"
          value={filters.finalDate}
          onChange={(e) => setFilters({ ...filters, finalDate: e.target.value })}
        />
      </div>

      <div className="filter-group">
        <label>Period:</label>
        <select
          value={filters.period}
          onChange={(e) => setFilters({ ...filters, period: e.target.value })}
        >
          <option value="">All</option>
          <option value="week">Week</option>
          <option value="month">Month</option>
          <option value="quarter">Quarter</option>
          <option value="6 months">6 Months</option>
          <option value="year">Year</option>
        </select>
      </div>

      <div className="filter-group">
        <label>Number of Authors:</label>
        <input
          type="number"
          value={filters.numberOfAuthors}
          onChange={(e) => setFilters({ ...filters, numberOfAuthors: e.target.value })}
        />
      </div>
    </div>
  );
};

export default Filters;
