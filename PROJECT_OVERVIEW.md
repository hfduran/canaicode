# CanAICode Project Overview

## Project Description

CanAICode is a GitHub Copilot analytics and reporting platform that tracks developer productivity metrics and Copilot usage across organizations.

## Architecture

The project consists of three main components:

### 1. Backend API (`./`)
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **Location**: Root directory
- **Port**: 8000
- **Base Path**: `/api`

### 2. Public Frontend (`./frontend/`)
- **Framework**: React 18+ with TypeScript
- **UI Library**: Cloudscape Design (AWS design system)
- **Features**: User dashboard, GitHub app integration, productivity analytics
- **Authentication**: GitHub OAuth

### 3. Admin Frontend (`./admin-frontend/`)
- **Framework**: React 18+ with TypeScript
- **UI Library**: Cloudscape Design
- **Features**: Admin operations (fetch metrics, send reports)
- **Authentication**: Constant secret key (environment variable)
- **Deployment**: Internal only, not publicly accessible

## Technology Stack

### Backend
- Python with FastAPI
- SQLAlchemy ORM
- PostgreSQL database
- JWT for GitHub App authentication
- Fernet encryption for secrets
- APScheduler for background jobs
- SMTP for email delivery

### Frontend (Both)
- React with TypeScript
- Cloudscape Design Components
- Axios for HTTP requests
- React Router (public frontend)
- Recharts/Victory for charts (public frontend)

## Key Features

### Backend Features
- GitHub App integration and OAuth flow
- Copilot metrics collection from GitHub API
- Productivity analytics (code contributions, PRs, commits)
- Language analytics
- User activity tracking
- Automated email reporting
- Background job scheduling
- Admin API endpoints

### Public Frontend Features
- GitHub authentication
- User productivity dashboards
- Language usage analytics
- Copilot metrics visualization
- Team activity monitoring

### Admin Frontend Features
- Manual metrics fetching from GitHub
- On-demand email report sending
- Date selection for historical reports

## Directory Structure

```
canaicode/
├── src/                          # Backend source code
│   ├── cmd/
│   │   ├── api/                  # API routes and controllers
│   │   └── scheduler/            # Background job scheduler
│   ├── domain/
│   │   ├── use_cases/            # Business logic
│   │   └── models/               # Database models
│   ├── auth/                     # Authentication logic
│   └── main.py                   # FastAPI application entry
├── frontend/                     # Public user-facing frontend
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── App.tsx
│   └── package.json
├── admin-frontend/               # Internal admin panel
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── App.tsx
│   └── package.json
└── tests/                        # Backend tests
```

## Admin Authentication

The admin panel uses a simple constant secret authentication:
- Environment variable: `ADMIN_KEY` (backend) and `REACT_APP_ADMIN_KEY` (admin frontend)
- All admin API requests include this token
- No OAuth or complex auth flow
- Meant for internal use only

## Admin API Endpoints

- `POST /api/admin/copilot_metrics/fetch` - Fetch GitHub Copilot metrics
  - Request: `{ "token": "<ADMIN_KEY>" }`
  - Response: `null` (HTTP 200)

- `POST /api/admin/report/send` - Send metrics email report
  - Request: `{ "date_string": "YYYY-MM-DD", "token": "<ADMIN_KEY>" }`
  - Response: `null` (HTTP 200)

## Environment Variables

### Backend
- `DATABASE_URL` - PostgreSQL connection string
- `ADMIN_KEY` - Admin authentication secret
- `FERNET_KEY` - Encryption key for secrets
- `MAIL_NAME` - Email sender address
- `MAIL_PASSWORD` - SMTP password
- `UNSUBSCRIBE_LINK` - Email unsubscribe link

### Admin Frontend
- `REACT_APP_API_URL` - Backend API URL
- `REACT_APP_ADMIN_KEY` - Admin authentication key (must match backend)

### Public Frontend
- `REACT_APP_API_URL` - Backend API URL

## Data Flow

1. **Metrics Collection**: Backend fetches data from GitHub API → stores in PostgreSQL
2. **User Dashboard**: Public frontend → Backend API → Database → Charts/Analytics
3. **Admin Operations**: Admin frontend → Admin API (with token) → Execute use cases
4. **Automated Jobs**: Scheduler → Use cases → GitHub API/Email sending

## Development

- Backend runs on port 8000
- Public frontend runs on port 3000 (development)
- Admin frontend runs on port 3000 (development, separate instance)
- Admin frontend should NOT be deployed publicly
