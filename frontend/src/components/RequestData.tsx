import React, { useState } from 'react';
import DropdownButton from './DropdownButton';
import InputForm from './InputForm';
import { RequestDataButtonProps } from '../types/ui';

const RequestDataButton: React.FC<RequestDataButtonProps> = ({ timeOptions, metricOptions }) => {
  const [timeRange, setTimeRange] = useState<string>('');
  const [team, setTeam] = useState<string>('');
  const [metricOption, setMetricOption] = useState<string>('');

  const handleRequisitarDados = (): void => {
    console.log('Time period selected: ', timeRange);
    console.log('Team selected: ', team);
    console.log('Metric option selected: ', metricOption);
  };

  return (
    <div>
      <DropdownButton
        options={timeOptions}
        selected={timeRange}
        setSelected={setTimeRange}
        label="Select time period "
      />

      <DropdownButton
        options={metricOptions}
        selected={metricOption}
        setSelected={setMetricOption}
        label="Select metric option "
      />

      <InputForm 
        value={team}
        setValue={setTeam}
        label="Enter developer team "
        placeholder="e.g., Team Alpha, Team Beta"
      />

      <button onClick={handleRequisitarDados}>
        Click to Request Data
      </button>
    </div>
  );
};

export default RequestDataButton;
