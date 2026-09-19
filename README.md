# Darukaa Earth

Darukaa Earth is a full-stack web application with separate frontend and backend components. The project is maintained in a public GitHub repository and deployed online for review.

## Project Links

- **GitHub Repository:** https://github.com/MOUNIKAC9353/darukaa-earth
- **Live Frontend:** https://darukaa-frontend-sskj.onrender.com
- **Backend API Documentation (Swagger):** https://darukaa-backend-do03.onrender.com/docs

## Repository Structure

```text
darukaa-earth/
├── .github/workflows/     # GitHub Actions workflow configuration
├── .husky/                # Git hooks
├── backend/               # Backend/API application
├── frontend/              # Frontend application
├── .gitignore
├── .pre-commit-config.yaml
├── docker-compose.yml     # Container orchestration configuration
├── package.json
├── package-lock.json
└── render.yaml            # Render deployment configuration
```

## Architecture

The application is organized as a full-stack system:

**User → Frontend → Backend/API → Application Data Layer**

The frontend provides the user-facing web interface. The backend exposes application/API functionality, and the deployed API documentation is available through Swagger UI.

## Technology and Project Configuration

The repository includes separate `frontend` and `backend` applications and configuration for:

- Web frontend
- Backend/API services
- Docker Compose
- Render deployment
- GitHub Actions workflows
- Husky Git hooks
- Pre-commit configuration
- Node package management

The exact framework/library versions and backend data models are defined in the corresponding source and configuration files in the repository.

## Database / Schema

Database configuration and schema details, if enabled by the deployed backend, are maintained within the `backend/` source and its environment/deployment configuration. No passwords, API keys, tokens, or other secrets are stored in this README.

## Local Setup

1. Clone the repository.
2. Open the project directory.
3. Install the dependencies required by the frontend/backend components according to their package or dependency files.
4. Configure required environment variables locally.
5. Start the frontend and backend services using the project's configured commands.
6. Open the local frontend URL in a browser.

### Docker

The repository includes `docker-compose.yml`, which can be used to run the configured services together when Docker is installed.

```bash
docker compose up --build
```

If environment variables are required, configure them locally before starting the services.

## Deployment

The repository includes `render.yaml` for Render deployment configuration. The currently deployed services are:

- Frontend: https://darukaa-frontend-sskj.onrender.com
- Backend API documentation: https://darukaa-backend-do03.onrender.com/docs

## CI/CD

The repository contains `.github/workflows/`, indicating GitHub Actions workflow configuration. Deployment-related configuration is also maintained through `render.yaml`. The exact workflow steps should be reviewed in the workflow file before modifying deployment settings.

## API Documentation

The deployed backend exposes Swagger/OpenAPI documentation at:

https://darukaa-backend-do03.onrender.com/docs

## Security / Credentials

Do not commit passwords, API keys, access tokens, database credentials, or private secrets to the repository. Required deployment secrets should be configured through the hosting platform/environment configuration.

## Review Notes

The repository is public, so no GitHub repository access invitation is required for reviewers.

For review, use the GitHub repository and the live frontend link above. The backend API can be inspected through the Swagger documentation link.
