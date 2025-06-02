import React from 'react';

const DropdownButton = ({ options, selected, setSelected, label }) => {
  const handleSelectChange = (event) => {
    const value = event.target.value;
    setSelected(value);
    console.log('Selected option:', value);
  };

  return (
    <div>
      <label htmlFor="my-select">{label}</label>
      <select id="my-select" value={selected} onChange={handleSelectChange}>
        <option value="" disabled>
          -- Select an option --
        </option>
        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
    </div>
  );
};

export default DropdownButton;