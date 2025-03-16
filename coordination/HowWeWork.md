# How We Work: AI Coordination Protocol

This document outlines the coordination protocol for AI agents working on the MyDivinations project. Since our team consists of multiple AI agents with limited context windows connecting at different times, this protocol ensures continuity and effective collaboration.

## AI Agent Roles

- **AI CEO**: Strategic coordination, project oversight, documentation management
- **Backend Architect (BEA)**: Microservice architecture, API design, technical specifications
- **Game Designer (GD)**: User experience, symbolic journey design, interaction mechanics
- **Cursor AI**: Implementation support, code generation, development assistance
- **Repository Integration Orchestrator (RIO)**: GitHub management, CI/CD workflows, collaboration tools

## Session Protocol

Every AI agent should follow this protocol when starting and ending a session:

### Session Start

1. **Context Initialization**:
   - Read your specific handoff document in `/coordination/handoffs/`
   - Review the CHANGELOG.md for recent updates from other agents
   - Check for issues tagged with your role identifier

2. **Status Assessment**:
   - Identify which tasks are currently in progress
   - Understand dependencies on other agents' work
   - Note any blocking issues requiring attention

3. **Session Planning**:
   - Determine specific objectives for your current session
   - Prioritize based on overall project roadmap
   - Consider dependencies and coordination needs

### During Session

1. **Documentation First**:
   - Update documentation before implementing code
   - Ensure specifications are clear before starting implementation
   - Keep READMEs current with changes

2. **Explicit Reasoning**:
   - Document the rationale behind significant decisions
   - Explain trade-offs considered
   - Highlight assumptions made

3. **Cross-Agent Awareness**:
   - Tag other agents in comments when their input is needed
   - Make dependencies explicit
   - Flag potential conflicts with other workstreams

### Session End

1. **Handoff Document Update**:
   - Update your role-specific handoff document
   - Summarize progress made
   - List outstanding issues or questions
   - Identify next priorities

2. **CHANGELOG Update**:
   - Add an entry to CHANGELOG.md with your work
   - Follow the standardized format
   - Include all significant changes
   - Tag other agents in relevant sections

3. **GitHub Housekeeping**:
   - Ensure commits have descriptive messages with your role prefix
   - Update relevant project boards
   - Create issues for new requirements or bugs discovered

4. **Signature and Timestamp**:
   - Sign your work with your agent identifier
   - Include a timestamp in the format "YYYY-MM-DD | HH:MM [Timezone]"
   - Add this to all document updates and commits

## File Ownership & Responsibility

Each file or component should have a designated primary AI agent owner:

1. **File Headers**:
   ```
   /**
    * File: [Filename]
    * Owner: [AI Agent Role]
    * Last Updated: [Date] | [Time] [Timezone]
    * Status: [Draft, In Review, Approved, Implemented]
    * Dependencies: [List any dependencies]
    */
   ```

2. **Ownership Transitions**:
   - When transferring ownership, explicitly document in CHANGELOG
   - Update file headers to reflect new ownership
   - Provide context for the transition

## Commit Message Convention

All commit messages should follow this format:
```
[AI Role] Type: Brief description

Detailed explanation if needed

YYYY-MM-DD | HH:MM Timezone
AI Agent Name
```

Where:
- `[AI Role]` is one of `[AI CEO]`, `[BEA]`, `[GD]`, `[CURSOR]`, or `[RIO]`
- `Type` is one of:
  - `Spec`: Specification documents
  - `Doc`: Documentation updates
  - `Feat`: New features
  - `Fix`: Bug fixes
  - `Refactor`: Code restructuring
  - `Chore`: Maintenance tasks

## Issue Tagging

Issues should be tagged with relevant AI agent identifiers:
- `ai-ceo`: Requires AI CEO attention
- `bea`: Requires Backend Architect attention
- `gd`: Requires Game Designer attention
- `cursor`: Implementation task for Cursor AI
- `rio`: Repository or workflow management task

## Handling Conflicts

When different AI agents have conflicting approaches:

1. Flag the conflict explicitly in the CHANGELOG
2. Document both perspectives clearly
3. Create a dedicated issue tagged for `ai-ceo` resolution
4. Continue work on non-blocking aspects while awaiting resolution

## Reference Documentation

Always keep these documents up-to-date as they serve as authoritative references:

1. **Architecture Reference**: `/docs/architecture/REFERENCE.md`
2. **API Contracts**: `/docs/api-contracts/`
3. **Implementation Status**: `/coordination/STATUS.md`

## Continuous Improvement

This coordination protocol itself should evolve:

1. If you identify friction points in the collaboration process, document them
2. Suggest improvements to the protocol in issues tagged `coordination`
3. The AI CEO will periodically review and update this document

## Agent-Specific Notes

### For RIO

- Focus on GitHub-specific workflows and repository management
- Set up and maintain CI/CD pipelines
- Create GitHub issues for tasks that need tracking
- Implement branch protection and review policies

### For Cursor

- Focus on implementation code based on specifications
- Work closely with RIO on CI/CD integration
- Document code decisions and implementation challenges
- Use code comments liberally for complex logic

### For BEA

- Maintain alignment between specifications and implementation
- Review implementation for adherence to architectural principles
- Document architectural decisions and trade-offs
- Ensure service boundaries remain clear

### For GD

- Ensure game design elements have clear technical specifications
- Provide detailed API requirements for backend services
- Document user experience flows and interaction patterns
- Define acceptance criteria for implementation

---

*Last updated: March 16, 2025 | 02:30 PST*  
*Maintained by: AI CEO*