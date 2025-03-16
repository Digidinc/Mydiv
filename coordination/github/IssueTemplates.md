# Issue and PR Templates

This document explains the issue and pull request templates implemented for the MyDivinations project.

## Overview

Templates have been implemented to standardize the format of issues and pull requests, ensuring that contributors provide all necessary information and maintain consistent quality across the project.

## Issue Templates

Three issue templates have been implemented:

### 1. Bug Report Template

The bug report template is designed to capture all information necessary to understand, reproduce, and fix bugs:

- **Bug Description**: A clear description of what the bug is
- **Steps to Reproduce**: Detailed steps to reproduce the issue
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Environment**: Service, environment, and version information
- **Screenshots/Logs**: Visual evidence or log outputs
- **Additional Context**: Any other relevant information

This template is automatically tagged with the `bug` label.

### 2. Feature Request Template

The feature request template is designed to capture new feature ideas and enhancements:

- **Feature Description**: A clear description of the requested feature
- **Problem Statement**: The problem this feature would solve
- **Proposed Solution**: How the feature should work
- **Alternatives Considered**: Other solutions that were considered
- **User Impact**: Benefits to users and which personas would be affected
- **Technical Considerations**: Implementation details to consider
- **Service Impact**: Which services would be affected
- **Dependencies**: Prerequisites for this feature

This template is automatically tagged with the `enhancement` label.

### 3. Documentation Update Template

The documentation update template is designed for requesting new or improved documentation:

- **Documentation Request**: What documentation needs to be updated
- **Current Documentation**: Reference to existing documentation
- **Suggested Changes**: What should be added, changed, or removed
- **Reason for Change**: Why the documentation change is needed
- **Affected Areas**: Which parts of the codebase are affected
- **Supporting Materials**: Diagrams, code snippets, or references
- **Suggested Location**: Where the documentation should live

This template is automatically tagged with the `documentation` label.

## Pull Request Template

The pull request template ensures that contributors provide comprehensive information about their changes:

- **Description**: Summary of the changes
- **Related Issue**: Link to the issue being addressed
- **Type of Change**: Bug fix, new feature, breaking change, etc.
- **Service Impact**: Which services are affected
- **Implementation Details**: Technical explanation of changes
- **Testing Performed**: Description of testing done
- **Documentation**: Documentation updates needed or included
- **Checklist**: Verification of code quality and process adherence
- **Screenshots**: Visual representation of changes (if applicable)
- **Additional Notes**: Any other context about the changes

## Configuration

Issue templates are configured in `.github/ISSUE_TEMPLATE/config.yml` with the following settings:

- Blank issues are disabled, requiring the use of a template
- A contact link directs general discussions to the GitHub Discussions tab

## Best Practices

When using these templates:

1. **Be Specific**: Provide clear and detailed information
2. **Include Screenshots**: When relevant to understanding the issue or solution
3. **Link Related Issues**: Use the GitHub issue linking syntax (`Closes #123`)
4. **Follow the Checklist**: Ensure all quality checks are completed
5. **Include Timestamp and Signature**: Add your timestamp and role at the end

## Future Enhancements

Future enhancements to the templates may include:

1. Additional specialized templates for specific service components
2. Integration with GitHub Actions for automated issue triage
3. Custom labels based on template selections
4. Template updates as project needs evolve

## Maintenance

These templates should be reviewed periodically to ensure they remain effective and aligned with project needs. Suggestions for improvements should be raised as issues with the `documentation` label.

---

*Last Updated: March 16, 2025 | 05:25 PST*  
*MyDiv RIO*