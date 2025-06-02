import React, { useState } from 'react';
import DropdownButton from './DropdownButton';

const RequestDataButton = ({ timeOptions, teamOptions }) => {
  const [timeRange, setTimeRange] = useState('');
  const [team, setTeam] = useState('');

  const handleRequisitarDados = () => {
    console.log('Opção de tempo selecionada: ', timeRange);
    console.log('Equipe selecionada: ', team);
  };

  return (
    <div>
      <DropdownButton
        options={timeOptions}
        selected={timeRange}
        setSelected={setTimeRange}
        label="Selecione o período:"
      />

      <DropdownButton
        options={teamOptions}
        selected={team}
        setSelected={setTeam}
        label="Selecione a equipe:"
      />

      <button onClick={handleRequisitarDados}>
        Requisitar Dados
      </button>
    </div>
  );
};

export default RequestDataButton;
