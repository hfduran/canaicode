# CanAICode Admin Panel

This is the internal admin panel frontend for CanAICode. It provides administrative functions to manage GitHub Copilot metrics and email reports.

## Features

- **Fetch Copilot Metrics**: Manually trigger fetching of GitHub Copilot usage metrics for all configured organizations
- **Send Email Reports**: Send metrics email reports to configured recipients with optional date selection

## Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Access to the backend API
- Admin authentication key

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

3. Configure environment variables in `.env`:
   - `REACT_APP_API_URL`: Backend API URL (e.g., `http://localhost:8000/api`)
   - `REACT_APP_ADMIN_KEY`: Admin authentication key (must match the backend's `ADMIN_KEY`)
   - `PUBLIC_URL`: Base path for deployment (e.g., `/admin` for subdirectory, `/` for root)

## Running the Application

### Development Mode

```bash
npm start
```

This runs the app in development mode at [http://localhost:3000](http://localhost:3000).

### Production Build

```bash
npm run build
```

This builds the app for production to the `build` folder.

### Deploying to a Subdirectory

The app base path is configured via the `PUBLIC_URL` environment variable in `.env`. Set it to `/admin` for subdirectory deployment or `/` for root deployment. When deploying with nginx to `/admin`:

```nginx
location /admin/ {
   auth_basic "Restricted";
   auth_basic_user_file /etc/nginx/.htpasswd;
   rewrite ^/admin(/.*)$ $1 break;
   proxy_pass http://127.0.0.1:3001;
   proxy_set_header Host $host;
   proxy_set_header X-Real-IP $remote_addr;
   proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
   proxy_set_header X-Forwarded-Proto $scheme;
}
```

All static assets will correctly load from `/admin/static/...`.

## Usage

### Fetch Copilot Metrics

1. Click the "Fetch Metrics" button
2. The system will retrieve GitHub Copilot usage data for all configured organizations
3. Metrics will be stored in the database for analysis

### Send Email Reports

1. Optionally select a date using the date picker (leave empty to use today's date)
2. Click "Send Email Report"
3. The system will send metrics reports to all configured recipients based on their report settings

## Security Notes

- This admin panel uses a constant secret key for authentication
- **DO NOT** deploy this application publicly
- Keep the `.env` file secure and never commit it to version control
- The admin key should be kept confidential and only shared with authorized administrators

## Authentication

The admin panel authenticates with the backend using a constant `ADMIN_KEY` stored in environment variables. All API requests include this token for authentication.

## API Endpoints Used

- `POST /admin/copilot_metrics/fetch`: Fetch GitHub Copilot metrics
- `POST /admin/report/send`: Send metrics email report

## Technology Stack

- React 19
- TypeScript
- Cloudscape Design (AWS design system)
- Axios (HTTP client)
- Create React App

## Development

The application follows a simple structure:
- `/src/components`: React components
- `/src/services`: API service layer
- `/public`: Static files

## Troubleshooting

### Authentication Errors

If you receive "Token invalid" errors:
1. Verify that `REACT_APP_ADMIN_KEY` in `.env` matches the backend's `ADMIN_KEY`
2. Ensure the backend is running and accessible
3. Check that the API URL is correct

### CORS Errors

If you encounter CORS errors:
1. Ensure the backend CORS settings include your frontend URL
2. Check that the backend is configured to accept requests from `http://localhost:3000`
