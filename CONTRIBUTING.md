# Contributing to MyDivinations

Thank you for your interest in contributing to the MyDivinations project! This document provides guidelines and instructions for contributing to our repository.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Branching Strategy](#branching-strategy)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Timestamp and Signature Protocol](#timestamp-and-signature-protocol)

## Code of Conduct

Our project is committed to providing a welcoming and inclusive environment for all contributors. We expect all participants to treat each other with respect and adhere to professional standards of communication.

## Getting Started

1. **Fork the repository**: Create your own fork of the repository to work on.
2. **Clone your fork**: `git clone https://github.com/your-username/Mydiv.git`
3. **Add the upstream repository**: `git remote add upstream https://github.com/Digidinc/Mydiv.git`
4. **Create a branch**: Follow our [branching strategy](#branching-strategy)
5. **Make your changes**: Implement your feature or fix
6. **Submit a pull request**: Follow our [pull request process](#pull-request-process)

## Development Workflow

We follow a microservices-based architecture with the following components:

1. **Astrology Engine Service**: Astrological calculations and chart generation
2. **API Gateway**: Unified API access point (planned)
3. **Archetypal Mapping**: Mapping astrological data to archetypal patterns (planned)
4. **Fractal Visualization**: Generating fractal parameters (planned)
5. **Content Generation**: Creating personalized guidance (planned)
6. **Audio Generation**: Creating consciousness-aligned audio (planned)

Each service follows a layered architecture with clear separation of concerns. When working on a service, maintain this separation and follow the established patterns.

## Branching Strategy

We follow GitHub Flow with some customizations:

- `main` branch is always deployable and contains production-ready code
- Create feature branches directly from `main` using the naming convention: `feature/descriptive-name`
- For bug fixes, create branches with the naming convention: `hotfix/issue-description`
- Reference issue numbers in branch names when applicable: `feature/user-auth-#42`

## Commit Message Guidelines

All commit messages should follow this format:
```
[Role] Type: Brief description (max 72 chars)

Detailed explanation if needed (optional)

YYYY-MM-DD | HH:MM Timezone
Your Name/Role
```

Where:
- `[Role]` is one of `[AI CEO]`, `[BEA]`, `[GD]`, `[CURSOR]`, or `[RIO]`
- `Type` is one of:
  - `Spec`: Specification documents
  - `Doc`: Documentation updates
  - `Feat`: New features
  - `Fix`: Bug fixes
  - `Refactor`: Code restructuring
  - `Chore`: Maintenance tasks

Example:
```
[BEA] Feat: Add endpoint for retrieving birth chart positions

This adds a new endpoint that returns planetary positions
for a given date, time, and location.

2025-03-16 | 14:30 PST
Backend Architect
```

## Pull Request Process

1. **Create an issue**: Before starting work, create an issue describing the feature or bug
2. **Use the PR template**: Fill out all sections of the pull request template
3. **Link related issues**: Reference the issue in your PR using "Closes #issue_number"
4. **Pass CI checks**: Ensure all automated tests and checks pass
5. **Request review**: Assign at least one reviewer to your PR
6. **Address feedback**: Respond to and address all reviewer comments
7. **Include timestamp and signature**: Add your timestamp and role signature at the end

PRs will only be merged after receiving required approvals and passing all status checks.

## Coding Standards

### Python

- Follow PEP 8 style guide
- Use black for formatting (max line length: 88)
- Use isort for import sorting
- Use flake8 for linting (max complexity: 10)
- Use docstrings for all public methods and classes
- Type hints are encouraged

### JavaScript/TypeScript (for future services)

- Follow ESLint with Airbnb configuration
- Use Prettier for formatting
- Use JSDoc comments for all public functions and components

## Testing

All code contributions should include appropriate tests:

- **Unit tests**: For individual functions and classes
- **Integration tests**: For API endpoints and service interactions
- **End-to-end tests**: For critical user flows

We aim for minimum 70% code coverage for core business logic.

## Documentation

Documentation is a crucial part of our project:

- **Code Documentation**: Add comments and docstrings to explain complex logic
- **API Documentation**: Document all endpoints with examples
- **README Updates**: Update README files when adding features
- **Architecture Documentation**: For significant changes, update architecture docs

## Timestamp and Signature Protocol

All contributors must follow this key protocol:

- **Every** code change, pull request, commit, and document update must include:
  - A timestamp in format: `YYYY-MM-DD | HH:MM [Timezone]`
  - Your role signature (e.g., "MyDiv RIO", "AI CEO", "BEA", etc.)

This protocol ensures accountability and helps track changes over time.

## Getting Help

If you need help or have questions:

- **For technical questions**: Create an issue with the "question" label
- **For process questions**: Contact the repository administrators
- **For bug reports**: Use the bug report issue template

---

*Last Updated: March 16, 2025 | 05:45 PST*  
*MyDiv RIO*