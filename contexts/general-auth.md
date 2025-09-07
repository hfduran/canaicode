# Canaicode Authentication System

## Overview
This project implements a full-stack authentication system with a Python FastAPI backend and React TypeScript frontend. The system provides user registration and login functionality with JWT-based authentication.

## Architecture

### Backend (Python FastAPI)
- **Framework**: FastAPI with SQLAlchemy ORM
- **Database**: PostgreSQL
- **Authentication**: JWT tokens with bcrypt password hashing
- **Architecture Pattern**: Clean Architecture (Domain-driven design)

### Frontend (React TypeScript)
- **Framework**: React with TypeScript
- **UI Library**: AWS CloudScape Design System
- **State Management**: Local state with localStorage for token persistence
- **Routing**: React Router

## Authentication Flow

### Registration Process
1. **Frontend** (`frontend/src/pages/UserRegister.tsx:25-44`):
   - User enters username and password
   - Form validation ensures both fields are filled
   - Calls `UserService.register()` with credentials
   - On success, redirects to login page after 1.2 seconds

2. **Backend** (`src/api/routes.py:48-56`):
   - POST `/register` endpoint accepts username and password
   - Delegates to `CreateUserUseCase` for business logic
   - Returns `UserResponse` with user_id and username

3. **Business Logic** (`src/domain/use_cases/create_user_use_case.py:17-25`):
   - Checks if username already exists (returns 400 if duplicate)
   - Hashes password using bcrypt
   - Creates new User entity with UUID
   - Persists to database via UsersRepository
   - Returns UserResponse DTO

### Login Process
1. **Frontend** (`frontend/src/pages/UserLogin.tsx:25-48`):
   - User enters username and password
   - Form validation ensures both fields are filled
   - Calls `UserService.login()` with credentials
   - On success:
     - Stores JWT token and user_id in localStorage
     - Triggers storage event for navigation state update
     - Redirects to home page

2. **Backend** (`src/api/routes.py:59-63`):
   - POST `/login` endpoint uses OAuth2PasswordRequestForm
   - Delegates to `ValidateUserUseCase` for authentication
   - Returns JWT `Token` with access_token, user_id, and token_type

3. **Business Logic** (`src/domain/use_cases/validate_user_use_case.py:22-28`):
   - Finds user by username
   - Verifies password against bcrypt hash
   - Creates JWT token with user info and expiration
   - Returns Token DTO with access token

## Security Features

### Password Security
- **Hashing**: bcrypt algorithm with automatic salt generation
- **Storage**: Only hashed passwords stored in database
- **Verification**: bcrypt verify function for login

### JWT Token Security
- **Algorithm**: HS256 (HMAC with SHA-256)
- **Secret**: Environment variable `SECRET_KEY`
- **Expiration**: Configurable via `ACCESS_TOKEN_EXPIRE_MINUTES` (default: 60 minutes)
- **Payload**: Contains username (`sub`) and user_id for authorization

### Authorization
- **Token Validation** (`src/api/routes.py:173-178`):
  - JWT signature and expiration verification
  - Returns 401 for invalid/expired tokens

- **User Access Control** (`src/api/routes.py:181-189`):
  - Verifies token contains valid user_id
  - Ensures users can only access their own data
  - Returns 403 for unauthorized access attempts

### Frontend Security
- **Token Storage**: localStorage (consider httpOnly cookies for production)
- **Auto-logout**: Tokens expire server-side
- **Authentication State**: Utility functions in `frontend/src/utils/auth.ts`

## API Endpoints

### Authentication Endpoints
- `POST /register` - User registration
- `POST /login` - User login (returns JWT token)

### Protected Endpoints (require valid JWT)
- All other endpoints require `Authorization: Bearer <token>` header
- Token validation via `oauth2_scheme` dependency
- User-specific data access controlled by `verify_user_access()`

## Data Models

### User Entity (`src/domain/entities/user.py`)
```python
class User(Entity):
    username: str
    hashed_password: str
    created_at: Optional[datetime] = None
```

### DTOs
- **UserResponse**: Returns user_id and username (registration response)
- **Token**: Returns access_token, user_id, and token_type (login response)

## Database Layer
- **Repository Pattern**: `UsersRepository` for data access
- **Mapping**: Database schema to domain entity mapping
- **ORM**: SQLAlchemy with PostgreSQL

## Frontend Services

### UserService (`frontend/src/services/userLoginAndRegisterService.ts`)
- **Login**: POST to `/login` with form-encoded credentials
- **Register**: POST to `/register` with JSON payload
- **Base URL**: Configurable via `REACT_APP_API_BASE_URL`

### Auth Utils (`frontend/src/utils/auth.ts`)
- `isAuthenticated()`: Checks for token and user_id in localStorage
- `getToken()`: Retrieves stored JWT token
- `getUserId()`: Retrieves stored user ID
- `logout()`: Clears stored authentication data

## Configuration
- **Backend**: Environment variables for SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
- **Frontend**: REACT_APP_API_BASE_URL for API endpoint configuration
- **CORS**: Configured for localhost:3000 (React development server)