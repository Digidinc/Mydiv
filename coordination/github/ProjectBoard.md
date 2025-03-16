# GitHub Project Board Configuration

This document describes the GitHub Project board setup for the MyDivinations project, explaining its structure, workflow, and best practices.

## Overview

The GitHub Project board serves as the central task management system for the MyDivinations project. It provides visibility into work items, their status, and assignment, enabling effective coordination across the team.

## Project Board Structure

The MyDivinations project uses a Kanban-style board with the following columns:

### 1. Backlog
- Tasks that have been identified but are not yet ready for implementation
- Requires basic information but doesn't need full specification
- No time commitment for implementation

### 2. Ready
- Fully specified tasks ready for implementation
- Clear acceptance criteria defined
- Prioritized based on project needs
- Assigned to specific milestones when applicable

### 3. In Progress
- Tasks currently being worked on
- Assigned to specific team members
- Limited to avoid context switching and multitasking
- Should have an associated branch/PR when code-related

### 4. Review
- Tasks completed by the implementer and awaiting review
- Associated with pull requests
- Requires approval from at least one reviewer
- May include testing/QA validation requirements

### 5. Done
- Tasks that have been completed and merged to `main`
- Meets all acceptance criteria
- Passed all required tests and reviews
- Properly documented

## Issue Organization

Issues in the project board are organized using:

### Labels

Primary label categories include:

1. **Type labels**:
   - `bug`: For defects and unexpected behavior
   - `enhancement`: For new features and improvements
   - `documentation`: For documentation-related tasks
   - `infrastructure`: For CI/CD and repository setup
   - `refactoring`: For code improvements without functional changes
   - `security`: For security-related issues
   - `performance`: For performance improvements

2. **Service labels**:
   - `astrology-engine`: For the Astrology Engine Service
   - `api-gateway`: For the API Gateway
   - `archetypal-mapping`: For the Archetypal Mapping Service
   - `content-generation`: For the Content Generation Service
   - `fractal-visualization`: For the Fractal Visualization Service
   - `audio-generation`: For the Audio Generation Service

3. **Priority labels**:
   - `priority-high`: Urgent issues requiring immediate attention
   - `priority-medium`: Important but not urgent issues
   - `priority-low`: Issues that can be addressed later

4. **Role labels**:
   - `ai-ceo`: Requires AI CEO attention
   - `bea`: Requires Backend Architect attention
   - `gd`: Requires Game Designer attention
   - `cursor`: Implementation task for Cursor AI
   - `rio`: Repository or workflow management task

### Milestones

Milestones group issues by delivery timeframes:

1. **MVP Phase 1**: Core infrastructure and Astrology Engine
2. **MVP Phase 2**: Archetypal Mapping and basic visualization
3. **MVP Phase 3**: Content generation and user experience
4. **Beta Release**: Production-ready implementation

## Automation Rules

The project board uses automation to reduce manual task management:

1. **New issues** are automatically added to the **Backlog** column
2. **Newly assigned issues** move to **Ready** when properly labeled
3. **Issues with PRs** move to **In Progress** when the PR is created
4. **PRs ready for review** move the issue to **Review** when review is requested
5. **Merged PRs** move the issue to **Done** when the PR is merged

## Board Views

The project board offers multiple views:

1. **Kanban**: The default board view showing work status
2. **Table**: For sorting and filtering issues by various attributes
3. **Calendar**: For milestone and deadline tracking
4. **Roadmap**: For long-term planning and dependencies

## Best Practices

When using the project board:

1. **Keep the board current**: Update issue status regularly
2. **Limit WIP**: Avoid having too many items in "In Progress"
3. **Link PRs to issues**: Always connect code changes to issues
4. **Use labels consistently**: Apply appropriate labels to all issues
5. **Write clear acceptance criteria**: Ensure tasks have clear completion definitions
6. **Include timestamps and signatures**: Follow the project's timestamp protocol
7. **Add context**: Ensure issues have sufficient information for implementation
8. **Review regularly**: Use the board during sync meetings and planning

## Access and Permissions

The project board is accessible to all team members with the following permissions:

- **Administrators**: Full control over board configuration
- **Write access**: Team members can create, edit, and move issues
- **Read access**: External collaborators can view the board

## Initial Setup Tasks

The initial board setup will include:

1. Creating the board structure and columns
2. Setting up automation rules
3. Defining labels and applying them to existing issues
4. Creating initial milestones
5. Importing existing issues into the board
6. Creating baseline views for different team needs

## Maintenance

The project board configuration will be reviewed monthly to ensure it continues to meet the project's needs. Adjustments will be made based on team feedback and evolving requirements.

---

*Last Updated: March 16, 2025 | 06:10 PST*  
*MyDiv RIO*