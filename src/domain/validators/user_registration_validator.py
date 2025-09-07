import re
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class ValidationError:
    field: str
    message: str


@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[ValidationError]

    def add_error(self, field: str, message: str) -> None:
        self.errors.append(ValidationError(field, message))
        self.is_valid = False


class UserRegistrationValidator:
    """
    Comprehensive validation class for user registration fields.
    Validates Brazilian-specific formats for CPF/CNPJ and cellphone numbers.
    """

    @staticmethod
    def validate_full_name(full_name: str) -> ValidationResult:
        """Validate that full name has at least two terms (first and last name)."""
        result = ValidationResult(is_valid=True, errors=[])

        if not full_name or not full_name.strip():
            result.add_error("full_name", "Full name is required")
            return result

        # Remove extra spaces and split
        name_parts = full_name.strip().split()

        if len(name_parts) < 2:
            result.add_error("full_name", "Full name must contain at least first and last name")
        elif not all(part.replace("'", "").replace("-", "").isalpha() for part in name_parts):
            result.add_error("full_name", "Full name must contain only letters, hyphens, and apostrophes")

        return result

    @staticmethod
    def validate_email(email: str) -> ValidationResult:
        """Validate email format using RFC 5322 compliant regex."""
        result = ValidationResult(is_valid=True, errors=[])

        if not email or not email.strip():
            result.add_error("email", "Email is required")
            return result

        # RFC 5322 compliant email regex (simplified but robust)
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not re.match(email_pattern, email.strip()):
            result.add_error("email", "Invalid email format")
        elif len(email.strip()) > 254:  # RFC 5321 limit
            result.add_error("email", "Email address is too long")

        return result

    @staticmethod
    def validate_cellphone(cellphone: str) -> ValidationResult:
        """Validate Brazilian cellphone format: (XX) XXXXX-XXXX or variations."""
        result = ValidationResult(is_valid=True, errors=[])

        if not cellphone or not cellphone.strip():
            result.add_error("cellphone", "Cellphone is required")
            return result

        # Extract only digits
        digits_only = re.sub(r'\D', '', cellphone)

        # Brazilian cellphone must have 11 digits (2 area code + 9 number with 9 as first digit)
        if len(digits_only) != 11:
            result.add_error("cellphone", "Cellphone must have 11 digits in Brazilian format")
        elif not digits_only.startswith(('11', '12', '13', '14', '15', '16', '17', '18', '19',
                                         '21', '22', '24', '27', '28',
                                         '31', '32', '33', '34', '35', '37', '38',
                                         '41', '42', '43', '44', '45', '46', '47', '48', '49',
                                         '51', '53', '54', '55',
                                         '61', '62', '63', '64', '65', '66', '67', '68', '69',
                                         '71', '73', '74', '75', '77', '79',
                                         '81', '82', '83', '84', '85', '86', '87', '88', '89',
                                         '91', '92', '93', '94', '95', '96', '97', '98', '99')):
            result.add_error("cellphone", "Invalid Brazilian area code")
        elif digits_only[2] != '9':
            result.add_error("cellphone", "Brazilian cellphone must start with 9 after area code")

        return result

    @staticmethod
    def validate_cpf(cpf: str) -> bool:
        """Validate Brazilian CPF using the official algorithm."""
        # Extract only digits
        cpf_digits = re.sub(r'\D', '', cpf)

        if len(cpf_digits) != 11:
            return False

        # Check for repeated digits (invalid CPFs)
        if cpf_digits == cpf_digits[0] * 11:
            return False

        # Validate first check digit
        sum1 = sum(int(cpf_digits[i]) * (10 - i) for i in range(9))
        remainder1 = sum1 % 11
        check_digit1 = 0 if remainder1 < 2 else 11 - remainder1

        if int(cpf_digits[9]) != check_digit1:
            return False

        # Validate second check digit
        sum2 = sum(int(cpf_digits[i]) * (11 - i) for i in range(10))
        remainder2 = sum2 % 11
        check_digit2 = 0 if remainder2 < 2 else 11 - remainder2

        return int(cpf_digits[10]) == check_digit2

    @staticmethod
    def validate_cnpj(cnpj: str) -> bool:
        """Validate Brazilian CNPJ using the official algorithm."""
        # Extract only digits
        cnpj_digits = re.sub(r'\D', '', cnpj)

        if len(cnpj_digits) != 14:
            return False

        # Check for repeated digits (invalid CNPJs)
        if cnpj_digits == cnpj_digits[0] * 14:
            return False

        # Validate first check digit
        weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        sum1 = sum(int(cnpj_digits[i]) * weights1[i] for i in range(12))
        remainder1 = sum1 % 11
        check_digit1 = 0 if remainder1 < 2 else 11 - remainder1

        if int(cnpj_digits[12]) != check_digit1:
            return False

        # Validate second check digit
        weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        sum2 = sum(int(cnpj_digits[i]) * weights2[i] for i in range(13))
        remainder2 = sum2 % 11
        check_digit2 = 0 if remainder2 < 2 else 11 - remainder2

        return int(cnpj_digits[13]) == check_digit2

    @staticmethod
    def validate_cpf_cnpj(cpf_cnpj: str) -> ValidationResult:
        """Validate CPF or CNPJ format and check digits."""
        result = ValidationResult(is_valid=True, errors=[])

        if not cpf_cnpj or not cpf_cnpj.strip():
            result.add_error("cpf_cnpj", "CPF or CNPJ is required")
            return result

        # Extract only digits
        digits_only = re.sub(r'\D', '', cpf_cnpj)

        if len(digits_only) == 11:
            # Validate as CPF
            if not UserRegistrationValidator.validate_cpf(cpf_cnpj):
                result.add_error("cpf_cnpj", "Invalid CPF number")
        elif len(digits_only) == 14:
            # Validate as CNPJ
            if not UserRegistrationValidator.validate_cnpj(cpf_cnpj):
                result.add_error("cpf_cnpj", "Invalid CNPJ number")
        else:
            result.add_error("cpf_cnpj", "CPF must have 11 digits or CNPJ must have 14 digits")

        return result

    @staticmethod
    def validate_username(username: str) -> ValidationResult:
        """Validate username format."""
        result = ValidationResult(is_valid=True, errors=[])

        if not username or not username.strip():
            result.add_error("username", "Username is required")
            return result

        username = username.strip()

        if len(username) < 3:
            result.add_error("username", "Username must be at least 3 characters long")
        elif len(username) > 50:
            result.add_error("username", "Username must be no more than 50 characters long")
        elif not re.match(r'^[a-z0-9]+$', username):
            result.add_error("username", "Username can only contain lowercase letters and numbers")

        return result

    @staticmethod
    def validate_password(password: str) -> ValidationResult:
        """Validate password strength."""
        result = ValidationResult(is_valid=True, errors=[])

        if not password:
            result.add_error("password", "Password is required")
            return result

        if len(password) < 8:
            result.add_error("password", "Password must be at least 8 characters long")
        elif len(password) > 128:
            result.add_error("password", "Password must be no more than 128 characters long")
        else:
            # Check for at least one uppercase, one lowercase, and one digit
            if not re.search(r'[A-Z]', password):
                result.add_error("password", "Password must contain at least one uppercase letter")
            if not re.search(r'[a-z]', password):
                result.add_error("password", "Password must contain at least one lowercase letter")
            if not re.search(r'\d', password):
                result.add_error("password", "Password must contain at least one number")

        return result

    @staticmethod
    def validate_enterprise_name(enterprise_name: Optional[str]) -> ValidationResult:
        """Validate enterprise name (optional field)."""
        result = ValidationResult(is_valid=True, errors=[])

        if enterprise_name and enterprise_name.strip():
            enterprise_name = enterprise_name.strip()
            if len(enterprise_name) < 2:
                result.add_error("enterprise_name", "Enterprise name must be at least 2 characters long")
            elif len(enterprise_name) > 100:
                result.add_error("enterprise_name", "Enterprise name must be no more than 100 characters long")

        return result

    @classmethod
    def validate_all_fields(cls, username: str, password: str, full_name: str,
                          enterprise_name: str, email: str, cellphone: str, cpf_cnpj: str) -> ValidationResult:
        """Validate all registration fields and return combined result."""
        overall_result = ValidationResult(is_valid=True, errors=[])

        # Validate each field
        validations = [
            cls.validate_username(username),
            cls.validate_password(password),
            cls.validate_full_name(full_name),
            cls.validate_enterprise_name(enterprise_name),
            cls.validate_email(email),
            cls.validate_cellphone(cellphone),
            cls.validate_cpf_cnpj(cpf_cnpj)
        ]

        # Combine all errors
        for validation in validations:
            if not validation.is_valid:
                overall_result.is_valid = False
                overall_result.errors.extend(validation.errors)

        return overall_result