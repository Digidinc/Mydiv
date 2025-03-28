# Branch Protection Implementation

This document provides instructions for implementing the branch protection rules for the `main` branch. These settings must be applied manually in the GitHub UI since they require administrative permissions.

## Branch Protection Settings

### For the `main` branch:

1. Navigate to the repository settings: https://github.com/Digidinc/Mydiv/settings/branches
2. Click "Add branch protection rule"
3. Set "Branch name pattern" to `main`

### Configure the following settings:

#### Required settings:
- [x] Require a pull request before merging
  - [x] Require approvals: 1
  - [x] Dismiss stale pull request approvals when new commits are pushed
  - [ ] Require review from Code Owners (optional for future use)

- [x] Require status checks to pass before merging
  - [x] Require branches to be up to date before merging
  - Required status checks:
    - [x] lint
    - [x] test
    - [x] docker

- [x] Require conversation resolution before merging

- [x] Restrict who can push to matching branches
  - Add repository administrators

#### Recommended settings:
- [ ] Allow force pushes: Disabled
- [ ] Allow deletions: Disabled

## Implementation Verification

Once these settings are applied, verify them by:

1. Attempting to push directly to `main` (should fail)
2. Creating a PR with failing status checks (should prevent merging)
3. Creating a PR with passing status checks (should allow merging after approval)

## Documentation

This implementation is documented in detail in `coordination/github/BranchProtectionRules.md` for reference by all team members.

---

*These instructions were prepared by: MyDiv RIO*  
*March 16, 2025 | 04:30 PST*