# CI Workflow for Astrology Engine Service

This document explains the GitHub Actions workflow implemented for the Astrology Engine Service.

## Overview

The CI workflow runs automatically on:
- All pushes to the `main` branch that affect the Astrology Engine Service
- All pull requests to the `main` branch that affect the Astrology Engine Service

The workflow consists of three parallel jobs:
1. **lint**: Code quality checks using flake8, black, and isort
2. **test**: Running tests with pytest and collecting code coverage
3. **docker**: Verifying Docker image builds correctly

## Detailed Configuration

### Linting Job

The linting job runs the following code quality checks:

- **flake8**: Checks for code errors and style issues
  - Critical errors (E9, F63, F7, F82) cause the build to fail
  - Other style issues are reported but don't cause failure
  - Maximum complexity is set to 10
  - Maximum line length is 127 characters

- **black**: Ensures consistent code formatting
  - Verifies that all files follow the Black code style
  - Fails if any file doesn't match Black's formatting

- **isort**: Checks import ordering
  - Configured with Black compatibility
  - Ensures imports follow the standard grouping pattern

### Testing Job

The testing job:

- Runs the test suite using pytest
- Collects code coverage data using pytest-cov
- Generates XML and terminal coverage reports
- Uploads coverage data to Codecov
- Uses hypothesis for property-based testing where applicable

### Docker Build Job

The Docker build job:

- Uses Docker Buildx for efficient builds
- Builds the image with the tag `mydiv/astrology-engine:test`
- Utilizes GitHub Actions cache for faster builds
- Verifies the image builds successfully and can be inspected

## Configuration Files

The workflow is defined in `.github/workflows/astrology-engine-ci.yml` and relies on the existing:
- `Dockerfile` in the service directory
- `requirements.txt` for Python dependencies

## Extending the Workflow

To add additional checks or tests to the workflow:

1. For Python-specific tools, add them to the lint job
2. For additional testing frameworks, add them to the test job
3. For Docker validation, modify the docker job

## Current Limitations

- Coverage thresholds are not enforced yet (future enhancement)
- Integration tests with other services will be added later
- No automated deployment steps are included in this workflow

## Troubleshooting

If the workflow fails:

1. Check the specific job that failed for detailed error messages
2. For linting failures, run the linting tools locally to fix issues
3. For test failures, run the tests locally with the `--verbose` flag
4. For Docker issues, try building the Docker image locally

---

*Last Updated: March 16, 2025 | 04:00 PST*  
*MyDiv RIO*