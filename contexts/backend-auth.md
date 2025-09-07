# Backend Authentication Architecture

## File Structure
```
src/
├── api/
│   └── routes.py                     # Authentication endpoints
├── domain/
│   ├── entities/
│   │   └── user.py                   # User domain entity
│   └── use_cases/
│       ├── create_user_use_case.py   # Registration business logic
│       ├── validate_user_use_case.py # Login business logic
│       └── dtos/
│           ├── user_response.py      # Registration response DTO
│           └── token.py              # Login response DTO
└── infrastructure/
    └── database/
        └── users/
            └── postgre/
                ├── users_repository.py # Data access layer
                ├── dtos/model.py       # Database schema
                └── mappers/            # Domain-DB mapping
```

## Key Components

### Authentication Endpoints (`src/api/routes.py`)
- **POST /register**: Creates new user account
- **POST /login**: Authenticates user and returns JWT token
- **Token validation**: `validate_token()` function for JWT verification
- **Access control**: `verify_user_access()` ensures users access only their data

### Business Logic Layer
- **CreateUserUseCase**: Handles user registration with duplicate username validation
- **ValidateUserUseCase**: Handles login authentication and JWT token generation

### Security Implementation
- **Password hashing**: bcrypt with automatic salt generation
- **JWT tokens**: HS256 algorithm with configurable expiration
- **Environment variables**: SECRET_KEY and ACCESS_TOKEN_EXPIRE_MINUTES

### Data Layer
- **UsersRepository**: Repository pattern for user data access
- **Database mapping**: SQLAlchemy ORM with PostgreSQL
- **Domain entities**: Clean separation between domain and database models