import React, { useState } from 'react';
import Filters from './Filters';
import mockDashboardData from '../data/mockData';
import { BarChart, Bar, CartesianGrid, XAxis, YAxis, Tooltip, Legend } from 'recharts';
import RequestDataButton from './RequestData';
import { Filters as FiltersType, FlattenedDataEntry } from "../types/ui";

const CalculatedMetricsDashboard: React.FC = () => {
  const [filters, setFilters] = useState<FiltersType>({
    languages: [],
    teams: [],
    initialDate: '',
    finalDate: '',
    period: '',
    numberOfAuthors: ''
  });

  // Gera opções únicas - p/ fazer o dropdown do filtro
  const availableLanguages = Array.from(new Set(mockDashboardData.flatMap(item => item.languages)));
  const availableTeams = Array.from(new Set(mockDashboardData.map(item => item.team)));

  // Filter
  const filteredData = mockDashboardData.filter(item => {
    return (
      (filters.languages.length === 0 || filters.languages.some(lang => item.languages.includes(lang))) &&
      (filters.teams.length === 0 || filters.teams.includes(item.team)) &&
      (filters.period === '' || filters.period === item.period)
    );
  });

  // Flatten os dados filtrados
  const flattenedData: FlattenedDataEntry[] = filteredData.flatMap(item =>
    item.data.filter(entry => (
      (!filters.numberOfAuthors || Number(filters.numberOfAuthors) === entry.number_of_authors) &&
      (!filters.initialDate || new Date(entry.initial_date) >= new Date(filters.initialDate)) &&
      (!filters.finalDate || new Date(entry.final_date) <= new Date(filters.finalDate))
    )).map(entry => ({
      ...entry,
      team: item.team,
      period: item.period,
      languages: item.languages
    }))
  );

  console.log("Flattened Data: ", flattenedData);

  return (
    <div className="dashboard-container" style={{ display: 'flex', gap: '20px', padding: '30px' }}>
      <div className="dashboard-main" style={{ flex: 0.7 }}>
        <h2>Select Language and Team data</h2>
          <RequestDataButton
            timeOptions={['Week', 'Month', 'Year', 'Semester']} // deve vir do back depois
            teamOptions={['Team Alpha', 'Team Beta']} // deve vir do back depois
          />
        <h2>Calculated Metrics</h2>

        <BarChart width={800} height={340} data={flattenedData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="initial_date" />
          <YAxis />
          <Tooltip 
            formatter={(value: any, name: string, props: any) => {
              if (name === 'Copilot Added Lines') {
                const percentage = props.payload.percentage_lines_added_by_copilot;
                return [`${value} lines (${percentage}%)`, name];
              }
              return [`${value} lines`, name];
            }}
          />
          <Legend />
          <Bar dataKey="relative_added_lines" fill="#8884d8" name="Total Added Lines" />
          <Bar dataKey="relative_added_lines_by_copilot" fill="#82ca9d" name="Copilot Added Lines" />
        </BarChart>
      </div>

      <div className="dashboard-filters" style={{ flex: 0.3 }}>
        <Filters
          filters={filters}
          setFilters={setFilters}
          availableLanguages={availableLanguages}
          availableTeams={availableTeams}
        />
      </div>
    </div>
  );
};

export default CalculatedMetricsDashboard;