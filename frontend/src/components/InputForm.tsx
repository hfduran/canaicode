import { InputFormProps } from '../types';

const InputForm: React.FC<InputFormProps> = ({ value, setValue, label, placeholder }) => {
    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
        const inputValue = event.target.value;
        setValue(inputValue);
        console.log('Input value:', inputValue);
    };

    return (
        <div>
            <label htmlFor="my-text-input">{label}</label>
            <input
                type="text"
                id="my-text-input"
                value={value}
                onChange={handleInputChange}
                placeholder={placeholder}
            />
        </div>
    );
};

export default InputForm;