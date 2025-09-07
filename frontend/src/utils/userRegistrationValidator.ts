/**
 * Comprehensive validation utilities for user registration fields.
 * Handles Brazilian-specific formats for CPF/CNPJ and cellphone numbers.
 */

export interface ValidationError {
  field: string;
  message: string;
}

export interface ValidationResult {
  isValid: boolean;
  errors: ValidationError[];
}

export class UserRegistrationValidator {
  /**
   * Validate that full name has at least two terms (first and last name).
   */
  static validateFullName(fullName: string): ValidationResult {
    const result: ValidationResult = { isValid: true, errors: [] };

    if (!fullName || !fullName.trim()) {
      result.errors.push({ field: "fullName", message: "Full name is required" });
      result.isValid = false;
      return result;
    }

    // Remove extra spaces and split
    const nameParts = fullName.trim().split(/\s+/);

    if (nameParts.length < 2) {
      result.errors.push({ field: "fullName", message: "Full name must contain at least first and last name" });
      result.isValid = false;
    } else if (!nameParts.every(part => /^[a-zA-ZÀ-ÿ'-]+$/.test(part))) {
      result.errors.push({ field: "fullName", message: "Full name must contain only letters, hyphens, and apostrophes" });
      result.isValid = false;
    }

    return result;
  }

  /**
   * Validate email format using RFC 5322 compliant regex.
   */
  static validateEmail(email: string): ValidationResult {
    const result: ValidationResult = { isValid: true, errors: [] };

    if (!email || !email.trim()) {
      result.errors.push({ field: "email", message: "Email is required" });
      result.isValid = false;
      return result;
    }

    // RFC 5322 compliant email regex (simplified but robust)
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    if (!emailPattern.test(email.trim())) {
      result.errors.push({ field: "email", message: "Invalid email format" });
      result.isValid = false;
    } else if (email.trim().length > 254) { // RFC 5321 limit
      result.errors.push({ field: "email", message: "Email address is too long" });
      result.isValid = false;
    }

    return result;
  }

  /**
   * Validate Brazilian cellphone format: (XX) XXXXX-XXXX or variations.
   */
  static validateCellphone(cellphone: string): ValidationResult {
    const result: ValidationResult = { isValid: true, errors: [] };

    if (!cellphone || !cellphone.trim()) {
      result.errors.push({ field: "cellphone", message: "Cellphone is required" });
      result.isValid = false;
      return result;
    }

    // Extract only digits
    const digitsOnly = cellphone.replace(/\D/g, '');

    // Brazilian cellphone must have 11 digits (2 area code + 9 number with 9 as first digit)
    if (digitsOnly.length !== 11) {
      result.errors.push({ field: "cellphone", message: "Cellphone must have 11 digits in Brazilian format" });
      result.isValid = false;
    } else {
      // Valid Brazilian area codes
      const validAreaCodes = [
        '11', '12', '13', '14', '15', '16', '17', '18', '19', // São Paulo
        '21', '22', '24', '27', '28', // Rio de Janeiro/Espírito Santo
        '31', '32', '33', '34', '35', '37', '38', // Minas Gerais
        '41', '42', '43', '44', '45', '46', '47', '48', '49', // Paraná/Santa Catarina
        '51', '53', '54', '55', // Rio Grande do Sul
        '61', '62', '63', '64', '65', '66', '67', '68', '69', // Centro-Oeste
        '71', '73', '74', '75', '77', '79', // Bahia/Sergipe
        '81', '82', '83', '84', '85', '86', '87', '88', '89', // Nordeste
        '91', '92', '93', '94', '95', '96', '97', '98', '99'  // Norte
      ];

      const areaCode = digitsOnly.substring(0, 2);
      if (!validAreaCodes.includes(areaCode)) {
        result.errors.push({ field: "cellphone", message: "Invalid Brazilian area code" });
        result.isValid = false;
      } else if (digitsOnly[2] !== '9') {
        result.errors.push({ field: "cellphone", message: "Brazilian cellphone must start with 9 after area code" });
        result.isValid = false;
      }
    }

    return result;
  }

  /**
   * Validate Brazilian CPF using the official algorithm.
   */
  private static validateCPF(cpf: string): boolean {
    // Extract only digits
    const cpfDigits = cpf.replace(/\D/g, '');

    if (cpfDigits.length !== 11) {
      return false;
    }

    // Check for repeated digits (invalid CPFs)
    if (cpfDigits === cpfDigits[0].repeat(11)) {
      return false;
    }

    // Validate first check digit
    let sum1 = 0;
    for (let i = 0; i < 9; i++) {
      sum1 += parseInt(cpfDigits[i]) * (10 - i);
    }
    const remainder1 = sum1 % 11;
    const checkDigit1 = remainder1 < 2 ? 0 : 11 - remainder1;

    if (parseInt(cpfDigits[9]) !== checkDigit1) {
      return false;
    }

    // Validate second check digit
    let sum2 = 0;
    for (let i = 0; i < 10; i++) {
      sum2 += parseInt(cpfDigits[i]) * (11 - i);
    }
    const remainder2 = sum2 % 11;
    const checkDigit2 = remainder2 < 2 ? 0 : 11 - remainder2;

    return parseInt(cpfDigits[10]) === checkDigit2;
  }

  /**
   * Validate Brazilian CNPJ using the official algorithm.
   */
  private static validateCNPJ(cnpj: string): boolean {
    // Extract only digits
    const cnpjDigits = cnpj.replace(/\D/g, '');

    if (cnpjDigits.length !== 14) {
      return false;
    }

    // Check for repeated digits (invalid CNPJs)
    if (cnpjDigits === cnpjDigits[0].repeat(14)) {
      return false;
    }

    // Validate first check digit
    const weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2];
    let sum1 = 0;
    for (let i = 0; i < 12; i++) {
      sum1 += parseInt(cnpjDigits[i]) * weights1[i];
    }
    const remainder1 = sum1 % 11;
    const checkDigit1 = remainder1 < 2 ? 0 : 11 - remainder1;

    if (parseInt(cnpjDigits[12]) !== checkDigit1) {
      return false;
    }

    // Validate second check digit
    const weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2];
    let sum2 = 0;
    for (let i = 0; i < 13; i++) {
      sum2 += parseInt(cnpjDigits[i]) * weights2[i];
    }
    const remainder2 = sum2 % 11;
    const checkDigit2 = remainder2 < 2 ? 0 : 11 - remainder2;

    return parseInt(cnpjDigits[13]) === checkDigit2;
  }

  /**
   * Validate CPF or CNPJ format and check digits.
   */
  static validateCpfCnpj(cpfCnpj: string): ValidationResult {
    const result: ValidationResult = { isValid: true, errors: [] };

    if (!cpfCnpj || !cpfCnpj.trim()) {
      result.errors.push({ field: "cpfCnpj", message: "CPF or CNPJ is required" });
      result.isValid = false;
      return result;
    }

    // Extract only digits
    const digitsOnly = cpfCnpj.replace(/\D/g, '');

    if (digitsOnly.length === 11) {
      // Validate as CPF
      if (!this.validateCPF(cpfCnpj)) {
        result.errors.push({ field: "cpfCnpj", message: "Invalid CPF number" });
        result.isValid = false;
      }
    } else if (digitsOnly.length === 14) {
      // Validate as CNPJ
      if (!this.validateCNPJ(cpfCnpj)) {
        result.errors.push({ field: "cpfCnpj", message: "Invalid CNPJ number" });
        result.isValid = false;
      }
    } else {
      result.errors.push({ field: "cpfCnpj", message: "CPF must have 11 digits or CNPJ must have 14 digits" });
      result.isValid = false;
    }

    return result;
  }

  /**
   * Validate username format.
   */
  static validateUsername(username: string): ValidationResult {
    const result: ValidationResult = { isValid: true, errors: [] };

    if (!username || !username.trim()) {
      result.errors.push({ field: "username", message: "Username is required" });
      result.isValid = false;
      return result;
    }

    const trimmedUsername = username.trim();

    if (trimmedUsername.length < 3) {
      result.errors.push({ field: "username", message: "Username must be at least 3 characters long" });
      result.isValid = false;
    } else if (trimmedUsername.length > 50) {
      result.errors.push({ field: "username", message: "Username must be no more than 50 characters long" });
      result.isValid = false;
    } else if (!/^[a-z0-9]+$/.test(trimmedUsername)) {
      result.errors.push({ field: "username", message: "Username can only contain lowercase letters and numbers" });
      result.isValid = false;
    }

    return result;
  }

  /**
   * Validate password strength.
   */
  static validatePassword(password: string): ValidationResult {
    const result: ValidationResult = { isValid: true, errors: [] };

    if (!password) {
      result.errors.push({ field: "password", message: "Password is required" });
      result.isValid = false;
      return result;
    }

    if (password.length < 8) {
      result.errors.push({ field: "password", message: "Password must be at least 8 characters long" });
      result.isValid = false;
    } else if (password.length > 128) {
      result.errors.push({ field: "password", message: "Password must be no more than 128 characters long" });
      result.isValid = false;
    } else {
      // Check for at least one uppercase, one lowercase, and one digit
      if (!/[A-Z]/.test(password)) {
        result.errors.push({ field: "password", message: "Password must contain at least one uppercase letter" });
        result.isValid = false;
      }
      if (!/[a-z]/.test(password)) {
        result.errors.push({ field: "password", message: "Password must contain at least one lowercase letter" });
        result.isValid = false;
      }
      if (!/\d/.test(password)) {
        result.errors.push({ field: "password", message: "Password must contain at least one number" });
        result.isValid = false;
      }
    }

    return result;
  }

  /**
   * Validate enterprise name (optional field).
   */
  static validateEnterpriseName(enterpriseName?: string): ValidationResult {
    const result: ValidationResult = { isValid: true, errors: [] };

    if (enterpriseName && enterpriseName.trim()) {
      const trimmedName = enterpriseName.trim();
      if (trimmedName.length < 2) {
        result.errors.push({ field: "enterpriseName", message: "Enterprise name must be at least 2 characters long" });
        result.isValid = false;
      } else if (trimmedName.length > 100) {
        result.errors.push({ field: "enterpriseName", message: "Enterprise name must be no more than 100 characters long" });
        result.isValid = false;
      }
    }

    return result;
  }

  /**
   * Validate all registration fields and return combined result.
   */
  static validateAllFields(
    username: string,
    password: string,
    fullName: string,
    enterpriseName: string,
    email: string,
    cellphone: string,
    cpfCnpj: string
  ): ValidationResult {
    const overallResult: ValidationResult = { isValid: true, errors: [] };

    // Validate each field
    const validations = [
      this.validateUsername(username),
      this.validatePassword(password),
      this.validateFullName(fullName),
      this.validateEnterpriseName(enterpriseName),
      this.validateEmail(email),
      this.validateCellphone(cellphone),
      this.validateCpfCnpj(cpfCnpj)
    ];

    // Combine all errors
    for (const validation of validations) {
      if (!validation.isValid) {
        overallResult.isValid = false;
        overallResult.errors.push(...validation.errors);
      }
    }

    return overallResult;
  }

  /**
   * Get field-specific validation errors from a validation result.
   */
  static getFieldErrors(validationResult: ValidationResult, fieldName: string): string[] {
    return validationResult.errors
      .filter(error => error.field === fieldName)
      .map(error => error.message);
  }

  /**
   * Check if a specific field has validation errors.
   */
  static hasFieldErrors(validationResult: ValidationResult, fieldName: string): boolean {
    return validationResult.errors.some(error => error.field === fieldName);
  }
}

/**
 * Format Brazilian cellphone number as user types with automatic special character insertion.
 */
export function formatCellphone(value: string): string {
  // Remove all non-digit characters
  const clean = value.replace(/\D/g, '');

  // Limit to 11 digits (2 area code + 9 number)
  const limited = clean.substring(0, 11);

  // Apply formatting based on length
  if (limited.length <= 2) {
    return limited;
  } else if (limited.length <= 7) {
    return `(${limited.substring(0, 2)}) ${limited.substring(2)}`;
  } else if (limited.length <= 11) {
    return `(${limited.substring(0, 2)}) ${limited.substring(2, 7)}-${limited.substring(7)}`;
  }

  return limited;
}

/**
 * Format CPF/CNPJ as user types with automatic special character insertion.
 */
export function formatCpfCnpj(value: string): string {
  // Remove all non-digit characters
  const clean = value.replace(/\D/g, '');

  // Limit to 14 digits maximum (CNPJ)
  const limited = clean.substring(0, 14);

  // Format based on length - prioritize CPF format up to 11 digits
  if (limited.length <= 3) {
    return limited;
  } else if (limited.length <= 6) {
    return `${limited.substring(0, 3)}.${limited.substring(3)}`;
  } else if (limited.length <= 9) {
    return `${limited.substring(0, 3)}.${limited.substring(3, 6)}.${limited.substring(6)}`;
  } else if (limited.length <= 11) {
    // CPF format: XXX.XXX.XXX-XX
    return `${limited.substring(0, 3)}.${limited.substring(3, 6)}.${limited.substring(6, 9)}-${limited.substring(9)}`;
  } else if (limited.length === 12) {
    // Transition to CNPJ format: XX.XXX.XXX/XXXX
    return `${limited.substring(0, 2)}.${limited.substring(2, 5)}.${limited.substring(5, 8)}/${limited.substring(8)}`;
  } else if (limited.length <= 14) {
    // Full CNPJ format: XX.XXX.XXX/XXXX-XX
    return `${limited.substring(0, 2)}.${limited.substring(2, 5)}.${limited.substring(5, 8)}/${limited.substring(8, 12)}-${limited.substring(12)}`;
  }

  return limited;
}