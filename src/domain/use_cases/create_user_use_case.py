import uuid
from fastapi import HTTPException

from src.domain.entities.user import User
from src.domain.use_cases.dtos.user_response import UserResponse
from src.domain.validators.user_registration_validator import UserRegistrationValidator
from src.infrastructure.database.users.postgre.users_repository import UsersRepository
from passlib.context import CryptContext

class CreateUserUseCase:
    def __init__(
        self,
        users_repository: UsersRepository,
    ) -> None:
        self.users_repository = users_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def execute(self, username: str, password: str, full_name: str,
                enterprise_name: str, email: str, cellphone: str, cpf_cnpj: str) -> UserResponse:
        # Validate all input fields
        validation_result = UserRegistrationValidator.validate_all_fields(
            username, password, full_name, enterprise_name, email, cellphone, cpf_cnpj
        )

        if not validation_result.is_valid:
            # Combine all validation errors into a single message
            error_messages = [f"{error.field}: {error.message}" for error in validation_result.errors]
            raise HTTPException(status_code=400, detail="Validation failed: " + "; ".join(error_messages))

        # Check for existing username
        persisted_user = self.users_repository.find_by_username(username)
        if persisted_user:
            raise HTTPException(status_code=400, detail="This username already exists")

        # Check for existing email
        persisted_email = self.users_repository.find_by_email(email)
        if persisted_email:
            raise HTTPException(status_code=400, detail="This email already exists")

        # Check for existing CPF/CNPJ
        persisted_cpf_cnpj = self.users_repository.find_by_cpf_cnpj(cpf_cnpj)
        if persisted_cpf_cnpj:
            raise HTTPException(status_code=400, detail="This CPF/CNPJ already exists")

        hashed_password = self.get_password_hash(password)
        new_user = User(
            id=str(uuid.uuid4()),
            username=username,
            hashed_password=hashed_password,
            full_name=full_name,
            enterprise_name=enterprise_name if enterprise_name else None,
            email=email,
            cellphone=cellphone,
            cpf_cnpj=cpf_cnpj
        )
        self.users_repository.create(new_user)
        return UserResponse(user_id=new_user.id, username=new_user.username)
    

    def get_password_hash(self, password: str) -> str:
      return self.pwd_context.hash(password) # type: ignore
