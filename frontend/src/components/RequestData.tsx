import React, { useState } from 'react';
import DropdownButton from './DropdownButton';
import { RequestDataButtonProps } from "../types/ui";

const RequestDataButton: React.FC<RequestDataButtonProps> = ({ timeOptions, teamOptions }) => {
  const [timeRange, setTimeRange] = useState<string>('');
  const [team, setTeam] = useState<string>('');

  const handleRequisitarDados = (): void => {
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
