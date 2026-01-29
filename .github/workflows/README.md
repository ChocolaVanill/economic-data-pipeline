# CI/CD Pipeline

This directory contains GitHub Actions workflows for continuous integration and deployment.

## Workflows

### 1. `ci.yml` - Main CI Pipeline
- **Trigger**: Push to main/develop branches, pull requests
- **Jobs**:
  - Lint and format checks (flake8, black, isort)
  - Type checking (mypy)
  - Unit tests with coverage
  - Integration tests with PostgreSQL
  - Build Docker images
  - Security scanning

### 2. `lint.yml` - Code Quality
- **Trigger**: All pushes and PRs
- **Jobs**:
  - Python linting (flake8)
  - Code formatting (black)
  - Import sorting (isort)
  - Type checking (mypy --strict)
  - YAML validation (yamllint)
  - Dockerfile linting (hadolint)
  - SQL linting (sqlfluff)

### 3. `test.yml` - Testing
- **Trigger**: All pushes and PRs, manual trigger
- **Jobs**:
  - Unit tests across Python versions (3.10, 3.11, 3.12)
  - Coverage reporting
  - dbt compilation checks
  - Integration tests

### 4. `deploy-staging.yml` - Staging Deployment
- **Trigger**: Push to develop branch, manual trigger
- **Jobs**:
  - Build and push Docker images
  - Deploy to staging environment
  - Run smoke tests

### 5. `deploy-production.yml` - Production Deployment
- **Trigger**: Push to main branch with version tag, manual trigger
- **Jobs**:
  - Build and push production images
  - Deploy to production with rollback capability
  - Post-deployment health checks

### 6. `schedule.yml` - Scheduled Jobs
- **Trigger**: Daily at 6 AM UTC
- **Jobs**:
  - Full pipeline dry run
  - Data freshness checks
  - Dependency updates check

## Environment Variables

Required secrets (add in GitHub repo settings):
- `DATABASE_URL` - PostgreSQL connection string for tests
- `DOCKER_USERNAME` - Docker Hub username
- `DOCKER_PASSWORD` - Docker Hub password
- `DEPLOY_KEY_STAGING` - SSH key for staging deployment
- `DEPLOY_KEY_PRODUCTION` - SSH key for production deployment
- `SLACK_WEBHOOK_URL` - Slack notifications

## Local Testing

Test workflows locally with `act`:
```bash
# Install act
brew install act

# Run all workflows
act

# Run specific workflow
act -W .github/workflows/test.yml
```

## Notes

- All Python code is checked with `mypy --strict` for type safety
- Dockerfile uses `--no-install-recommends` for minimal image size
- YAML files follow 120-character line limit
