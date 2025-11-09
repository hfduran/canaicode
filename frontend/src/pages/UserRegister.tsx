import React, { useState, useEffect, useRef } from "react";
import {
  Container,
  Header,
  SpaceBetween,
  FormField,
  Input,
  Button,
  Alert,
  Box,
} from "@cloudscape-design/components";
import { useNavigate } from "react-router-dom";
import UserService from "../services/userLoginAndRegisterService";
import {
  UserRegistrationValidator,
  ValidationResult,
  formatCellphone,
  formatCpfCnpj
} from "../utils/userRegistrationValidator";

const UserRegister: React.FC = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [enterpriseName, setEnterpriseName] = useState("");
  const [email, setEmail] = useState("");
  const [cellphone, setCellphone] = useState("");
  const [cpfCnpj, setCpfCnpj] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Validation states
  const [validationResult, setValidationResult] = useState<ValidationResult>({ isValid: true, errors: [] });
  const [debouncedValidationResult, setDebouncedValidationResult] = useState<ValidationResult>({ isValid: true, errors: [] });
  const [showValidationErrors, setShowValidationErrors] = useState(false);

  // Individual field validation states (tracks which fields have been "touched"/blurred)
  const [fieldTouched, setFieldTouched] = useState({
    fullName: false,
    enterpriseName: false,
    email: false,
    cellphone: false,
    cpfCnpj: false,
    username: false,
    password: false
  });

  // Track which fields are currently being typed in (to hide errors)
  const [fieldTyping, setFieldTyping] = useState({
    fullName: false,
    enterpriseName: false,
    email: false,
    cellphone: false,
    cpfCnpj: false,
    username: false,
    password: false
  });

  // Debounce timer ref
  const debounceTimerRef = useRef<NodeJS.Timeout | null>(null);

  const navigate = useNavigate();

  // Real-time validation (always runs to keep validation state updated)
  useEffect(() => {
    const result = UserRegistrationValidator.validateAllFields(
      username,
      password,
      fullName,
      enterpriseName,
      email,
      cellphone,
      cpfCnpj
    );
    setValidationResult(result);

    // Clear existing debounce timer
    if (debounceTimerRef.current) {
      clearTimeout(debounceTimerRef.current);
    }

    // Set up debounced validation for touched fields (1 second delay)
    debounceTimerRef.current = setTimeout(() => {
      setDebouncedValidationResult(result);
      // Clear typing state for all fields after debounce
      setFieldTyping({
        fullName: false,
        enterpriseName: false,
        email: false,
        cellphone: false,
        cpfCnpj: false,
        username: false,
        password: false
      });
    }, 1000);

    // Cleanup timeout on unmount
    return () => {
      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current);
      }
    };
  }, [username, password, fullName, enterpriseName, email, cellphone, cpfCnpj]);

  const handleCellphoneChange = (value: string) => {
    const formatted = formatCellphone(value);
    handleFieldChange("cellphone", formatted, setCellphone);
  };

  const handleCpfCnpjChange = (value: string) => {
    const formatted = formatCpfCnpj(value);
    handleFieldChange("cpfCnpj", formatted, setCpfCnpj);
  };

  // Helper function to get field errors (uses debounced validation for touched fields)
  const getFieldErrors = (fieldName: string): string[] => {
    const fieldKey = fieldName as keyof typeof fieldTouched;

    // If showing all validation errors (form submission), use immediate validation
    if (showValidationErrors) {
      return UserRegistrationValidator.getFieldErrors(validationResult, fieldName);
    }

    // If user is currently typing in this field, hide errors
    if (fieldTyping[fieldKey]) {
      return [];
    }

    // If field is touched, use debounced validation for better UX
    if (fieldTouched[fieldKey]) {
      return UserRegistrationValidator.getFieldErrors(debouncedValidationResult, fieldName);
    }

    return [];
  };

  // Helper function to check if field has errors and should show them
  const hasFieldErrors = (fieldName: string): boolean => {
    const fieldKey = fieldName as keyof typeof fieldTouched;

    // If showing all validation errors (form submission), use immediate validation
    if (showValidationErrors) {
      return UserRegistrationValidator.hasFieldErrors(validationResult, fieldName);
    }

    // If user is currently typing in this field, hide errors
    if (fieldTyping[fieldKey]) {
      return false;
    }

    // If field is touched, use debounced validation
    if (fieldTouched[fieldKey]) {
      return UserRegistrationValidator.hasFieldErrors(debouncedValidationResult, fieldName);
    }

    return false;
  };

  // Helper function to handle field blur events
  const handleFieldBlur = (fieldName: keyof typeof fieldTouched) => {
    setFieldTouched(prev => ({
      ...prev,
      [fieldName]: true
    }));

    // Clear typing state for this field
    setFieldTyping(prev => ({
      ...prev,
      [fieldName]: false
    }));

    // Immediately update debounced validation on blur for instant feedback
    const currentValidation = UserRegistrationValidator.validateAllFields(
      username,
      password,
      fullName,
      enterpriseName,
      email,
      cellphone,
      cpfCnpj
    );
    setDebouncedValidationResult(currentValidation);
  };

  // Helper function to handle field changes (marks field as typing)
  const handleFieldChange = (fieldName: keyof typeof fieldTyping, value: string, setter: (value: string) => void) => {
    // Mark field as currently being typed in
    setFieldTyping(prev => ({
      ...prev,
      [fieldName]: true
    }));

    // Update the field value
    setter(value);
  };


  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setShowValidationErrors(true);
    setErrorMsg(null);
    setSuccessMsg(null);

    // Validate all fields before submission
    const result = UserRegistrationValidator.validateAllFields(
      username,
      password,
      fullName,
      enterpriseName,
      email,
      cellphone,
      cpfCnpj
    );

    setValidationResult(result);

    if (!result.isValid) {
      setErrorMsg("Please fix the validation errors before submitting.");
      return;
    }

    setIsLoading(true);

    try {
      const data = await UserService.register(
        username,
        password,
        fullName,
        enterpriseName,
        email,
        cellphone,
        cpfCnpj
      );
      if (data && data.username) {
        setSuccessMsg("Registration successful! Redirecting...");
        setTimeout(() => navigate("/user-login"), 1200);
      } else {
        setErrorMsg("Registration failed.");
      }
    } catch (error: any) {
      setErrorMsg(error.response?.data?.detail || "Registration failed.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{
      height: '100%',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '20px',
      boxSizing: 'border-box'
    }}>
      <div style={{
        width: '100%',
        maxWidth: '400px',
        backgroundColor: 'white',
        padding: '32px'
      }}>
        <Box margin={{ bottom: 'l' }}>
          <Header
            variant="h1"
            description="Fill in all the required information to create your account."
          >
            User Register
          </Header>
        </Box>
        <Container fitHeight>
          <form onSubmit={handleRegister}>
            <SpaceBetween size="m">
              <FormField
                label="Full Name"
                constraintText="Your complete name (first and last name required)"
                errorText={hasFieldErrors("fullName") ? getFieldErrors("fullName").join(", ") : undefined}
              >
                <Input
                  value={fullName}
                  onChange={({ detail }) => handleFieldChange("fullName", detail.value, setFullName)}
                  onBlur={() => handleFieldBlur("fullName")}
                  placeholder="João Silva"
                  autoComplete="name"
                  invalid={hasFieldErrors("fullName")}
                />
              </FormField>
              <FormField
                label="Enterprise Name"
                constraintText="Company or business name (optional)"
                errorText={hasFieldErrors("enterpriseName") ? getFieldErrors("enterpriseName").join(", ") : undefined}
              >
                <Input
                  value={enterpriseName}
                  onChange={({ detail }) => handleFieldChange("enterpriseName", detail.value, setEnterpriseName)}
                  onBlur={() => handleFieldBlur("enterpriseName")}
                  placeholder="Empresa LTDA"
                  autoComplete="organization"
                  invalid={hasFieldErrors("enterpriseName")}
                />
              </FormField>
              <FormField
                label="Email"
                constraintText="Your email address"
                errorText={hasFieldErrors("email") ? getFieldErrors("email").join(", ") : undefined}
              >
                <Input
                  value={email}
                  onChange={({ detail }) => handleFieldChange("email", detail.value, setEmail)}
                  onBlur={() => handleFieldBlur("email")}
                  placeholder="joao@email.com"
                  type="email"
                  autoComplete="email"
                  invalid={hasFieldErrors("email")}
                />
              </FormField>
              <FormField
                label="Cellphone"
                constraintText="Brazilian cellphone number (11 digits)"
                errorText={hasFieldErrors("cellphone") ? getFieldErrors("cellphone").join(", ") : undefined}
              >
                <Input
                  value={cellphone}
                  onChange={({ detail }) => handleCellphoneChange(detail.value)}
                  onBlur={() => handleFieldBlur("cellphone")}
                  placeholder="(11) 99999-9999"
                  autoComplete="tel"
                  invalid={hasFieldErrors("cellphone")}
                />
              </FormField>
              <FormField
                label="CPF/CNPJ"
                constraintText="Your CPF (11 digits) or company CNPJ (14 digits)"
                errorText={hasFieldErrors("cpfCnpj") ? getFieldErrors("cpfCnpj").join(", ") : undefined}
              >
                <Input
                  value={cpfCnpj}
                  onChange={({ detail }) => handleCpfCnpjChange(detail.value)}
                  onBlur={() => handleFieldBlur("cpfCnpj")}
                  placeholder="000.000.000-00 or 00.000.000/0000-00"
                  invalid={hasFieldErrors("cpfCnpj")}
                />
              </FormField>
              <FormField
                label="Username"
                constraintText="3-50 characters, lowercase letters and numbers only"
                errorText={hasFieldErrors("username") ? getFieldErrors("username").join(", ") : undefined}
              >
                <Input
                  value={username}
                  onChange={({ detail }) => handleFieldChange("username", detail.value, setUsername)}
                  onBlur={() => handleFieldBlur("username")}
                  placeholder="Username"
                  autoComplete="username"
                  invalid={hasFieldErrors("username")}
                />
              </FormField>
              <FormField
                label="Password"
                constraintText="At least 8 characters with uppercase, lowercase, and number"
                errorText={hasFieldErrors("password") ? getFieldErrors("password").join(", ") : undefined}
              >
                <Input
                  value={password}
                  onChange={({ detail }) => handleFieldChange("password", detail.value, setPassword)}
                  onBlur={() => handleFieldBlur("password")}
                  placeholder="Password"
                  type="password"
                  autoComplete="new-password"
                  invalid={hasFieldErrors("password")}
                />
              </FormField>
              <Button
                variant="primary"
                loading={isLoading}
                disabled={
                  !username ||
                  !password ||
                  !fullName ||
                  !email ||
                  !cellphone ||
                  !cpfCnpj ||
                  (showValidationErrors && !validationResult.isValid)
                }
                formAction="submit"
                fullWidth
              >
                Register
              </Button>
              {successMsg && (
                <Alert type="success" statusIconAriaLabel="Success">
                  {successMsg}
                </Alert>
              )}
              {errorMsg && (
                <Alert type="error" statusIconAriaLabel="Error">
                  {errorMsg}
                </Alert>
              )}
            </SpaceBetween>
          </form>
          <Box margin={{ top: 'l' }} textAlign="center">
            <Box variant="p">Already have an account? <a href="/user-login">Login here.</a></Box>
          </Box>
        </Container>
      </div>
    </div>
  );
};

export default UserRegister;
