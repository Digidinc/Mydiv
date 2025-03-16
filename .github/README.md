# GitHub Configuration

This directory contains configuration files and templates for GitHub features used in the MyDivinations project.

## Contents

### Issue Templates

- `ISSUE_TEMPLATE/bug_report.md` - Template for reporting bugs
- `ISSUE_TEMPLATE/feature_request.md` - Template for requesting new features
- `ISSUE_TEMPLATE/documentation.md` - Template for documentation updates
- `ISSUE_TEMPLATE/config.yml` - Configuration for issue templates

### Pull Request Template

- `pull_request_template.md` - Template for all pull requests

### Branch Protection

- `BRANCH_PROTECTION.md` - Instructions for implementing branch protection rules

### Label Configuration

- `labels.json` - Definitions for issue labels
- `workflows/sync-labels.yml` - Workflow to synchronize labels with the repository

### Milestone Configuration

- `milestones.json` - Definitions for project milestones
- `workflows/sync-milestones.yml` - Workflow to synchronize milestones with the repository

### Workflows

- `workflows/astrology-engine-ci.yml` - CI workflow for the Astrology Engine Service
- `workflows/sync-labels.yml` - Workflow to sync labels with the repository
- `workflows/sync-milestones.yml` - Workflow to sync milestones with the repository

## Usage

### Adding New Labels

1. Add the new label definition to `labels.json`
2. Commit and push the changes
3. The `sync-labels.yml` workflow will automatically create the label

### Adding New Milestones

1. Add the new milestone definition to `milestones.json`
2. Commit and push the changes
3. The `sync-milestones.yml` workflow will automatically create the milestone

### Adding New Templates

1. Create a new template file in the appropriate directory
2. If it's an issue template, update `ISSUE_TEMPLATE/config.yml` as needed
3. Commit and push the changes

### Modifying Workflows

1. Edit the workflow file in the `workflows` directory
2. Commit and push the changes
3. The workflow will be updated automatically

## Maintenance

These configuration files should be reviewed and updated regularly to ensure they continue to meet the project's needs. Updates should follow the standard commit message format and include timestamps and signatures.

---

*Last Updated: March 16, 2025 | 06:35 PST*  
*MyDiv RIO*