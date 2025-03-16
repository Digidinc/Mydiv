# Branch Protection Rules

This document outlines the branch protection rules implemented for the MyDivinations project repositories.

## Main Branch Protection

The `main` branch is protected with the following rules to ensure code quality and stability:

### Required Settings

- **Require pull request reviews before merging**: Enabled
  - **Required approving reviews**: 1
  - **Dismiss stale pull request approvals when new commits are pushed**: Enabled
  - **Require review from Code Owners**: Disabled (may be enabled in the future)

- **Require status checks to pass before merging**: Enabled
  - **Require branches to be up to date before merging**: Enabled
  - **Required status checks**:
    - `lint` (Code Quality Checks)
    - `test` (Run Tests)
    - `docker` (Docker Build)

- **Require conversation resolution before merging**: Enabled
  - Ensures all comment threads are resolved before merging

- **Restrict who can push to matching branches**: Enabled
  - Only administrators can push directly to `main`

### Additional Settings

- **Allow force pushes**: Disabled
  - Prevents history rewriting on the `main` branch

- **Allow deletions**: Disabled
  - Prevents accidental deletion of the `main` branch

## Feature Branch Naming Convention

While not enforced through GitHub settings, we follow these naming conventions for branches:

- **Feature branches**: `feature/descriptive-name`
- **Hotfix branches**: `hotfix/issue-description`

## Implementation Details

These branch protection rules were implemented on March 16, 2025, according to the GitHub Flow branching strategy recommended by the AI CEO.

## Enforcement

These rules are enforced through GitHub's branch protection settings and apply to all team members. Only repository administrators have the ability to bypass these restrictions in emergency situations.

## Future Considerations

As the project grows, we may consider additional branch protection measures:

1. Increasing the number of required reviewers for critical code areas
2. Implementing a CODEOWNERS file to automatically assign reviewers
3. Adding additional required status checks as our CI/CD pipeline expands
4. Creating protected environment configurations for deployment branches

## Troubleshooting

If you're experiencing issues with branch protection rules:

1. Ensure your branch is up to date with `main` before creating a pull request
2. Check that all required status checks are passing
3. Make sure your pull request has received the required number of approving reviews
4. Resolve all conversation threads in the pull request

If issues persist, contact a repository administrator for assistance.

---

*Last Updated: March 16, 2025 | 04:20 PST*  
*MyDiv RIO*