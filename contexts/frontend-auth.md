# Frontend Authentication Components

## File Structure
```
frontend/src/
├── pages/
│   ├── UserLogin.tsx                 # Login page component
│   └── UserRegister.tsx              # Registration page component
├── services/
│   └── userLoginAndRegisterService.ts # API service for auth
└── utils/
    └── auth.ts                       # Authentication utilities
```

## Key Components

### Login Component (`frontend/src/pages/UserLogin.tsx`)
- **Form handling**: Username/password input with validation
- **Authentication**: Calls UserService.login() with credentials
- **Success flow**: Stores token/user_id in localStorage, triggers storage event, redirects
- **Error handling**: Displays user-friendly error messages
- **UI**: AWS CloudScape Design System components

### Registration Component (`frontend/src/pages/UserRegister.tsx`)
- **Form handling**: Username/password input with validation
- **Registration**: Calls UserService.register() with credentials
- **Success flow**: Shows success message, redirects to login after delay
- **Error handling**: Displays user-friendly error messages
- **Navigation**: Links to login page for existing users

### Authentication Service (`frontend/src/services/userLoginAndRegisterService.ts`)
- **Login API**: POST to `/login` with form-encoded data
- **Register API**: POST to `/register` with JSON payload
- **Configuration**: Uses REACT_APP_API_BASE_URL environment variable
- **HTTP client**: Axios with proper content-type headers

### Authentication Utilities (`frontend/src/utils/auth.ts`)
- **`isAuthenticated()`**: Checks if user has valid token and user_id
- **`getToken()`**: Retrieves JWT token from localStorage
- **`getUserId()`**: Retrieves user ID from localStorage
- **`logout()`**: Clears authentication data from localStorage

## Authentication Flow
1. User fills login/register form
2. Frontend validates required fields
3. Service calls backend API
4. On success: token stored in localStorage
5. Storage event triggers navigation state update
6. User redirected to appropriate page