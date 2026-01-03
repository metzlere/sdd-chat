# SDD-Chat: Spec-Driven Development via Chat Interface

A comprehensive workflow for replicating GitHub Spec Kit's Spec-Driven Development (SDD) process using only an LLM chat interface. Designed for constrained environments where agentic coding tools are unavailable.

---

## Table of Contents

1. [Overview](#overview)
2. [Repository Structure](#repository-structure)
3. [Quick Reference: The 6-Phase Workflow](#quick-reference-the-6-phase-workflow)
4. [Setup: One-Time Configuration](#setup-one-time-configuration)
5. [Phase 0: Constitution](#phase-0-constitution)
6. [Phase 1: Specification](#phase-1-specification)
7. [Phase 2: Clarification](#phase-2-clarification)
8. [Phase 3: Planning](#phase-3-planning)
9. [Phase 4: Task Breakdown](#phase-4-task-breakdown)
10. [Phase 5: Implementation](#phase-5-implementation)
11. [Context Bundle Templates](#context-bundle-templates)
12. [Brownfield Projects: Working with Existing Codebases](#brownfield-projects-working-with-existing-codebases)
13. [Tips for Success](#tips-for-success)

---

## Overview

### What is SDD-Chat?

SDD-Chat adapts GitHub Spec Kit's structured development methodology for use in restricted environments where you only have access to an LLM via a chat interface (no Claude Code, Cursor, Copilot agents, etc.).

The core principle remains: **specifications become executable**. You define *what* you want to build and *why* before diving into *how*. The LLM generates structured artifacts that guide implementation.

### The Workflow at a Glance

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SDD-Chat Workflow                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│   │   Phase 0    │    │   Phase 1    │    │   Phase 2    │                  │
│   │ Constitution │───▶│Specification │───▶│ Clarification│                  │
│   │  (one-time)  │    │  (per feat)  │    │  (iterate)   │                  │
│   └──────────────┘    └──────────────┘    └──────────────┘                  │
│                                                  │                           │
│                                                  ▼                           │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│   │   Phase 5    │    │   Phase 4    │    │   Phase 3    │                  │
│   │Implementation│◀───│Task Breakdown│◀───│   Planning   │                  │
│   │  (execute)   │    │  (per feat)  │    │  (per feat)  │                  │
│   └──────────────┘    └──────────────┘    └──────────────┘                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Key Differences from Spec Kit

| Aspect | Spec Kit | SDD-Chat |
|--------|----------|----------|
| Execution | Automated via slash commands | Manual copy/paste workflow |
| Scripts | Shell scripts create branches/dirs | You manually create directories |
| Context | Agent reads files directly | You provide context bundles |
| Storage | In project `.specify/` folder | Separate `sdd-chat/` meta-repo |

---

## Repository Structure

You'll maintain two repositories:

### 1. The `sdd-chat/` Meta-Repository (Specs Storage)

```
sdd-chat/
├── README.md
├── templates/
│   ├── constitution-template.md
│   ├── spec-template.md
│   ├── plan-template.md
│   └── tasks-template.md
├── prompts/
│   ├── constitution-prompt.md
│   ├── specify-prompt.md
│   ├── clarify-prompt.md
│   ├── plan-prompt.md
│   ├── tasks-prompt.md
│   └── implement-prompt.md
└── projects/
    ├── projectA/
    │   ├── constitution.md
    │   └── specs/
    │       ├── 001-feature-name/
    │       │   ├── spec.md
    │       │   ├── plan.md
    │       │   ├── research.md
    │       │   ├── data-model.md
    │       │   ├── tasks.md
    │       │   └── contracts/
    │       │       └── api-spec.json
    │       └── 002-another-feature/
    │           └── ...
    └── projectB/
        ├── constitution.md
        └── specs/
            └── ...
```

### 2. Your Source Repository (The Actual Project)

```
your-project/
├── src/
│   ├── models/
│   ├── services/
│   └── ...
├── tests/
├── README.md
└── ...
```

---

## Quick Reference: The 6-Phase Workflow

| Phase | Action | Context to Provide | Output to Save |
|-------|--------|-------------------|----------------|
| **0. Constitution** | Define project principles | Template + your constraints | `projects/{project}/constitution.md` |
| **1. Specification** | Describe feature (WHAT/WHY) | Template + constitution + description | `specs/{NNN-name}/spec.md` |
| **2. Clarification** | Resolve ambiguities | Spec + clarify prompt | Updated `spec.md` with clarifications |
| **3. Planning** | Technical design (HOW) | Spec + constitution + plan template + tech stack | `plan.md`, `research.md`, `data-model.md`, `contracts/` |
| **4. Tasks** | Break into actionable tasks | Plan + spec + tasks template | `tasks.md` |
| **5. Implementation** | Generate code | Tasks + plan + source context | Code files in your source repo |

---

## Setup: One-Time Configuration

### Step 1: Create the `sdd-chat/` Repository

```bash
mkdir -p sdd-chat/templates
mkdir -p sdd-chat/prompts
mkdir -p sdd-chat/projects
cd sdd-chat
git init
```

### Step 2: Create Templates

Save the following templates from the [Context Bundle Templates](#context-bundle-templates) section:

- `templates/constitution-template.md`
- `templates/spec-template.md`
- `templates/plan-template.md`
- `templates/tasks-template.md`

### Step 3: Create Prompt Files

Save the prompts from the [Context Bundle Templates](#context-bundle-templates) section:

- `prompts/constitution-prompt.md`
- `prompts/specify-prompt.md`
- `prompts/clarify-prompt.md`
- `prompts/plan-prompt.md`
- `prompts/tasks-prompt.md`
- `prompts/implement-prompt.md`

### Step 4: Create a Project Directory

```bash
mkdir -p sdd-chat/projects/my-project/specs
```

---

## Phase 0: Constitution

The constitution establishes immutable principles that guide all development for a project.

### When to Use

- Once per project (at project inception)
- When project principles need amendment

### What You Provide to the LLM

**Context Bundle:**
```
1. Constitution template (templates/constitution-template.md)
2. Constitution prompt (prompts/constitution-prompt.md)
3. Your specific constraints and requirements (your input)
```

### Workflow

1. **Copy** the constitution template into the chat
2. **Copy** the constitution prompt
3. **Provide** your specific project constraints:
   - Tech stack preferences
   - Testing requirements
   - Coding standards
   - Architectural patterns
   - Compliance/security requirements

4. **Ask the LLM** to generate a constitution based on your inputs

5. **Save** the output to: `sdd-chat/projects/{project}/constitution.md`

### Example Prompt

```
I'm setting up a new project and need to establish its constitution.

Here is the constitution template:
[paste templates/constitution-template.md]

Here is the prompt:
[paste prompts/constitution-prompt.md]

My project constraints:
- Python 3.11+ for all code
- pytest for testing with >80% coverage
- FastAPI for REST APIs
- PostgreSQL for persistence
- Docker-first deployment
- Must follow PEP8 and use type hints
- Security: Input validation on all endpoints

Generate a complete constitution for this project.
```

---

## Phase 1: Specification

The specification captures WHAT you're building and WHY, without any implementation details.

### When to Use

- At the start of each new feature

### What You Provide to the LLM

**Context Bundle:**
```
1. Spec template (templates/spec-template.md)
2. Specify prompt (prompts/specify-prompt.md)
3. Constitution (projects/{project}/constitution.md)
4. Your feature description
```

### Workflow

1. **Create** the feature directory:
   ```bash
   mkdir -p sdd-chat/projects/{project}/specs/{NNN-feature-name}
   ```
   Where `NNN` is the next sequential number (001, 002, etc.)

2. **Copy** into the chat:
   - Spec template
   - Specify prompt
   - Your project's constitution
   - Your feature description

3. **Ask the LLM** to generate the specification

4. **Save** the output to: `specs/{NNN-feature-name}/spec.md`

### Critical Rules for Specifications

- **NO tech stack** (languages, frameworks, libraries)
- **NO implementation details** (APIs, databases, code structure)
- **Focus on** user stories, requirements, success criteria
- **Mark ambiguities** with `[NEEDS CLARIFICATION: question]`

### Example Prompt

```
I need to create a specification for a new feature.

CONSTITUTION:
[paste projects/{project}/constitution.md]

SPEC TEMPLATE:
[paste templates/spec-template.md]

SPECIFY PROMPT:
[paste prompts/specify-prompt.md]

FEATURE DESCRIPTION:
Build a user authentication system that allows users to register with 
email/password, log in, reset passwords via email, and manage sessions. 
Users should see their login history and be able to terminate sessions 
on other devices.

Generate a complete specification following the template. Remember: 
NO implementation details, NO tech stack mentions. Focus on WHAT 
users need and WHY.
```

---

## Phase 2: Clarification

Resolve any ambiguities in the specification before proceeding to planning.

### When to Use

- After Phase 1, if `[NEEDS CLARIFICATION]` markers exist
- When you notice gaps in the spec

### What You Provide to the LLM

**Context Bundle:**
```
1. Clarify prompt (prompts/clarify-prompt.md)
2. Current spec.md
```

### Workflow

1. **Copy** the clarify prompt and current spec into the chat

2. **Ask the LLM** to identify areas needing clarification

3. **Answer** the clarification questions

4. **Ask the LLM** to update the spec with resolved clarifications

5. **Save** the updated spec (overwrite `spec.md`)

### Example Prompt

```
Review this specification and identify any ambiguities or gaps that 
need clarification before I can proceed to technical planning.

CLARIFY PROMPT:
[paste prompts/clarify-prompt.md]

CURRENT SPEC:
[paste specs/{NNN-feature}/spec.md]

Identify up to 3 critical clarification questions, then I'll answer them.
```

---

## Phase 3: Planning

The plan captures HOW you'll build the feature technically.

### When to Use

- After specification is complete and clarified

### What You Provide to the LLM

**Context Bundle:**
```
1. Plan template (templates/plan-template.md)
2. Plan prompt (prompts/plan-prompt.md)
3. Constitution (projects/{project}/constitution.md)
4. Finalized spec.md
5. Your technical stack decisions
6. [BROWNFIELD] Existing project context (see Brownfield section)
```

### Workflow

1. **Copy** into the chat:
   - Plan template
   - Plan prompt
   - Constitution
   - Finalized spec
   - Your tech stack decisions

2. **Ask the LLM** to generate the technical plan

3. **Save** outputs to the feature directory:
   - `plan.md` - Main implementation plan
   - `research.md` - Technology research notes
   - `data-model.md` - Data structures and schemas
   - `contracts/api-spec.json` - API contracts (if applicable)
   - `quickstart.md` - Key validation scenarios

### Example Prompt

```
Generate a technical implementation plan for this feature.

CONSTITUTION:
[paste projects/{project}/constitution.md]

PLAN TEMPLATE:
[paste templates/plan-template.md]

PLAN PROMPT:
[paste prompts/plan-prompt.md]

SPECIFICATION:
[paste specs/{NNN-feature}/spec.md]

TECHNICAL DECISIONS:
- Language: Python 3.11
- Framework: FastAPI
- Database: PostgreSQL with SQLAlchemy
- Auth: JWT tokens with refresh tokens
- Email: SendGrid for transactional emails
- Testing: pytest with pytest-asyncio

Generate plan.md, research.md, data-model.md, and contracts/api-spec.json.
Start with plan.md.
```

---

## Phase 4: Task Breakdown

Break the plan into specific, actionable, dependency-ordered tasks.

### When to Use

- After planning is complete

### What You Provide to the LLM

**Context Bundle:**
```
1. Tasks template (templates/tasks-template.md)
2. Tasks prompt (prompts/tasks-prompt.md)
3. plan.md
4. spec.md (for user story references)
5. data-model.md (if exists)
6. contracts/ (if exists)
```

### Workflow

1. **Copy** into the chat:
   - Tasks template
   - Tasks prompt
   - All planning artifacts

2. **Ask the LLM** to generate the task breakdown

3. **Save** output to: `specs/{NNN-feature}/tasks.md`

### Task Format

Tasks should include:
- **[P]** marker for tasks that can run in parallel
- **[Story]** reference to related user story
- **Exact file paths** for where code should be created
- **Dependencies** on other tasks
- **Test-first** structure (if TDD is in constitution)

### Example Prompt

```
Generate an actionable task breakdown for implementing this feature.

TASKS TEMPLATE:
[paste templates/tasks-template.md]

TASKS PROMPT:
[paste prompts/tasks-prompt.md]

PLAN:
[paste specs/{NNN-feature}/plan.md]

SPECIFICATION:
[paste specs/{NNN-feature}/spec.md]

DATA MODEL:
[paste specs/{NNN-feature}/data-model.md]

API CONTRACTS:
[paste specs/{NNN-feature}/contracts/api-spec.json]

Generate tasks.md with dependency-ordered tasks grouped by user story. 
Include exact file paths and parallel execution markers [P] where applicable.
```

---

## Phase 5: Implementation

Execute tasks to generate actual code.

### When to Use

- After task breakdown is complete
- Execute one task or task group at a time

### What You Provide to the LLM

**Context Bundle:**
```
1. Implement prompt (prompts/implement-prompt.md)
2. tasks.md (current task to implement)
3. plan.md (for technical context)
4. data-model.md (for schema reference)
5. contracts/ (for API reference)
6. [BROWNFIELD] Existing source files (see Brownfield section)
```

### Workflow

1. **Identify** the next task(s) to implement from `tasks.md`

2. **Copy** into the chat:
   - Implement prompt
   - The specific task(s) being implemented
   - Relevant planning documents
   - Existing source files (for brownfield projects)

3. **Ask the LLM** to generate the code

4. **Save** the generated code to your source repository

5. **Test** the implementation

6. **Mark** the task as complete in `tasks.md`

7. **Repeat** for next task

### Example Prompt

```
Implement the following task from my task breakdown.

IMPLEMENT PROMPT:
[paste prompts/implement-prompt.md]

TASK TO IMPLEMENT:
### T001: Create User Model
- **File**: src/models/user.py
- **Story**: US1 - User Registration
- **Dependencies**: None
- **Description**: Create SQLAlchemy model for users with fields: 
  id, email, password_hash, created_at, updated_at, is_active

PLAN CONTEXT:
[paste relevant sections from plan.md]

DATA MODEL:
[paste specs/{NNN-feature}/data-model.md]

EXISTING CODE CONTEXT (if any):
[paste any existing relevant files like src/models/__init__.py]

Generate the complete implementation for src/models/user.py.
```

---

## Context Bundle Templates

### Constitution Template

Save to `templates/constitution-template.md`:

```markdown
# Project Constitution: [PROJECT_NAME]

## Preamble
[Brief description of the project's purpose and scope]

## Article I: Technology Stack
- **Language**: [e.g., Python 3.11+]
- **Framework**: [e.g., FastAPI]
- **Database**: [e.g., PostgreSQL]
- **Testing**: [e.g., pytest]

## Article II: Code Quality Standards
- [List non-negotiable code quality requirements]
- [e.g., Type hints required on all functions]
- [e.g., Docstrings required on all public methods]

## Article III: Testing Requirements
- [Minimum coverage requirements]
- [Required test types: unit, integration, e2e]
- [TDD requirements if applicable]

## Article IV: Architecture Principles
- [e.g., Modular design - features as standalone components]
- [e.g., Dependency injection for testability]
- [e.g., Repository pattern for data access]

## Article V: Security Requirements
- [Authentication/authorization requirements]
- [Input validation requirements]
- [Data protection requirements]

## Article VI: Documentation Requirements
- [Code documentation standards]
- [API documentation requirements]
- [README requirements]

## Article VII: Error Handling
- [Error handling patterns]
- [Logging requirements]
- [Monitoring requirements]

## Article VIII: Performance Standards
- [Response time requirements]
- [Scalability requirements]
- [Resource constraints]

## Article IX: Governance
- Constitution supersedes all other practices
- Amendments require documentation and approval
- Deviations require explicit documentation
```

### Spec Template

Save to `templates/spec-template.md`:

```markdown
# Feature Specification: [FEATURE_NAME]

**Feature Branch**: [NNN-feature-name]
**Created**: [DATE]
**Status**: Draft | In Review | Approved

## Overview

### Problem Statement
[What problem does this feature solve?]

### Goals
- [Primary goal]
- [Secondary goals]

### Non-Goals (Out of Scope)
- [Explicitly excluded functionality]

## User Stories

### US1: [Story Title]
**Priority**: P0 | P1 | P2

**As a** [user type]
**I want** [capability]
**So that** [benefit]

**Acceptance Criteria**:
- Given [initial state], When [action], Then [expected outcome]
- Given [initial state], When [action], Then [expected outcome]

**Independent Test**: [How this can be tested standalone]

### US2: [Story Title]
[Repeat format above]

## Functional Requirements

- **FR-001**: System MUST [specific capability]
- **FR-002**: System MUST [specific capability]
- **FR-003**: Users MUST be able to [key interaction]

## Non-Functional Requirements

- **NFR-001**: [Performance requirement]
- **NFR-002**: [Security requirement]
- **NFR-003**: [Reliability requirement]

## Key Entities

- **[Entity 1]**: [What it represents, key attributes - NO implementation]
- **[Entity 2]**: [What it represents, relationships]

## Success Criteria

- [Measurable outcome 1]
- [Measurable outcome 2]

## Assumptions

- [Assumption 1]
- [Assumption 2]

## Open Questions

- [NEEDS CLARIFICATION: specific question]

## Review Checklist

- [ ] No implementation details (languages, frameworks, APIs)
- [ ] Focused on user value and business needs
- [ ] All requirements are testable and unambiguous
- [ ] User stories have clear acceptance criteria
- [ ] Success criteria are measurable
```

### Plan Template

Save to `templates/plan-template.md`:

```markdown
# Implementation Plan: [FEATURE_NAME]

**Branch**: [NNN-feature-name]
**Date**: [DATE]
**Spec Reference**: [link to spec.md]

## Technical Context

### Stack
- **Language/Version**: [e.g., Python 3.11]
- **Primary Dependencies**: [e.g., FastAPI, SQLAlchemy]
- **Storage**: [e.g., PostgreSQL]
- **Testing**: [e.g., pytest]
- **Target Platform**: [e.g., Linux server, Docker]

### Performance Requirements
- [e.g., <200ms p95 response time]
- [e.g., Support 1000 concurrent users]

### Constraints
- [e.g., Must integrate with existing auth service]
- [e.g., Cannot modify existing user table schema]

## Source Structure

```
src/
├── models/
│   └── [feature models]
├── services/
│   └── [business logic]
├── api/
│   └── [endpoints]
└── lib/
    └── [utilities]
tests/
├── unit/
├── integration/
└── e2e/
```

## Implementation Phases

### Phase 0: Research
- [Technology decisions to validate]
- [Unknowns to investigate]

### Phase 1: Foundation
- Data models
- Database migrations
- Core services

### Phase 2: Core Features (per User Story)
- US1: [Implementation approach]
- US2: [Implementation approach]

### Phase 3: Integration
- API endpoints
- External integrations

### Phase 4: Polish
- Error handling
- Logging
- Documentation

## Data Model Summary

[Reference data-model.md for full details]

### Key Entities
- **Entity1**: [fields summary]
- **Entity2**: [fields summary]

### Relationships
- Entity1 → Entity2: [relationship type]

## API Contracts Summary

[Reference contracts/ for full specs]

### Endpoints
- `POST /api/resource` - Create resource
- `GET /api/resource/{id}` - Get resource

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| [Risk 1] | [Mitigation strategy] |

## Constitution Compliance

- [ ] Follows Article I (Tech Stack)
- [ ] Follows Article II (Code Quality)
- [ ] Follows Article III (Testing)
- [ ] Follows Article IV (Architecture)
```

### Tasks Template

Save to `templates/tasks-template.md`:

```markdown
# Task Breakdown: [FEATURE_NAME]

**Feature**: [NNN-feature-name]
**Plan Reference**: [link to plan.md]
**Created**: [DATE]

## Task Legend

- **[P]**: Can run in parallel with other [P] tasks in same phase
- **Story**: Which user story this task belongs to (US1, US2, etc.)
- **Depends**: Tasks that must complete first

## Phase 1: Foundation

### T001: [Task Title]
- **File**: [exact file path, e.g., src/models/user.py]
- **Story**: US1
- **Depends**: None
- **Description**: [What this task creates/modifies]
- **Acceptance**: [How to verify task is complete]

### T002: [Task Title] [P]
- **File**: [exact file path]
- **Story**: US1
- **Depends**: T001
- **Description**: [Description]
- **Acceptance**: [Verification]

## Phase 2: User Story Implementation

### User Story 1: [Title]

#### T003: [Task Title]
- **File**: [path]
- **Story**: US1
- **Depends**: T001, T002
- **Description**: [Description]
- **Acceptance**: [Verification]

### User Story 2: [Title]

#### T004: [Task Title] [P]
- **File**: [path]
- **Story**: US2
- **Depends**: T001
- **Description**: [Description]
- **Acceptance**: [Verification]

## Phase 3: Integration

### T005: [Task Title]
- **File**: [path]
- **Story**: All
- **Depends**: T003, T004
- **Description**: [Description]
- **Acceptance**: [Verification]

## Phase 4: Polish

### T006: [Task Title]
- **File**: [path]
- **Story**: All
- **Depends**: T005
- **Description**: [Description]
- **Acceptance**: [Verification]

## Progress Tracking

| Task | Status | Notes |
|------|--------|-------|
| T001 | ⬜ Not Started | |
| T002 | ⬜ Not Started | |
| T003 | ⬜ Not Started | |
```

### Prompts

#### Constitution Prompt

Save to `prompts/constitution-prompt.md`:

```markdown
# Constitution Generation Prompt

You are helping establish the foundational principles for a software project. 
Generate a constitution document that will guide all development decisions.

## Instructions

1. Review the provided constraints and requirements
2. Fill in the constitution template completely
3. Ensure all articles are specific and actionable (not vague)
4. Include concrete examples where helpful
5. Make requirements measurable where possible

## Output Format

Return a complete constitution.md file following the template structure.
All placeholders should be replaced with specific content.
```

#### Specify Prompt

Save to `prompts/specify-prompt.md`:

```markdown
# Specification Generation Prompt

You are helping create a feature specification using Spec-Driven Development.
The specification defines WHAT the feature does and WHY, NOT how it's implemented.

## Critical Rules

1. **NO IMPLEMENTATION DETAILS**:
   - ❌ No programming languages
   - ❌ No frameworks or libraries  
   - ❌ No database or API design
   - ❌ No code structure or architecture
   
2. **Focus On**:
   - ✅ User stories and journeys
   - ✅ Business requirements
   - ✅ Success criteria (measurable)
   - ✅ Acceptance scenarios

3. **Mark Ambiguities**: Use `[NEEDS CLARIFICATION: specific question]` 
   for critical decisions that need user input (max 3)

4. **Be Testable**: Every requirement should be verifiable

## Output Format

Return a complete spec.md following the template structure.
Ensure constitutional compliance (review the constitution provided).
```

#### Clarify Prompt

Save to `prompts/clarify-prompt.md`:

```markdown
# Clarification Prompt

You are reviewing a feature specification to identify and resolve ambiguities.

## Instructions

1. Review the specification for:
   - Vague requirements that could have multiple interpretations
   - Missing details critical to implementation
   - Conflicting statements
   - Assumptions that need validation

2. Identify maximum 3 critical clarification questions
   - Focus on decisions that significantly impact scope or UX
   - Skip minor details with reasonable defaults

3. Present questions in this format:
   ```
   **Question 1**: [The question]
   **Context**: [Why this matters]
   **Options**: [Possible answers if applicable]
   ```

4. After receiving answers, update the spec.md with:
   - A new "## Clarifications" section
   - Resolution of all [NEEDS CLARIFICATION] markers
```

#### Plan Prompt

Save to `prompts/plan-prompt.md`:

```markdown
# Planning Prompt

You are creating a technical implementation plan for a feature.
The plan defines HOW to build what the specification describes.

## Instructions

1. **Review Inputs**:
   - Constitution (for constraints and standards)
   - Specification (for requirements)
   - Technical decisions provided by user

2. **Generate Artifacts**:
   - `plan.md` - Main implementation plan
   - `research.md` - Technology research and decisions
   - `data-model.md` - Data structures, schemas, relationships
   - `contracts/api-spec.json` - API specifications (if applicable)

3. **Ensure**:
   - All spec requirements are addressed
   - Plan follows constitution principles
   - Dependencies are clearly identified
   - Phases are logical and buildable

## Output Format

Generate each artifact separately, starting with plan.md.
Use the provided templates as structure guides.
```

#### Tasks Prompt

Save to `prompts/tasks-prompt.md`:

```markdown
# Task Breakdown Prompt

You are breaking down an implementation plan into specific, actionable tasks.

## Instructions

1. **Review Inputs**:
   - plan.md (required)
   - spec.md (for user story references)
   - data-model.md (for entity details)
   - contracts/ (for API details)

2. **Create Tasks That Are**:
   - Specific enough for an LLM to implement without additional context
   - Ordered by dependencies
   - Grouped by user story for independent testing
   - Include exact file paths

3. **Use Markers**:
   - `[P]` for tasks that can run in parallel
   - Reference user stories (US1, US2, etc.)
   - List dependencies explicitly

4. **Task Size**: Each task should be completable in one implementation session
   (roughly: one file or one logical unit)

## Output Format

Return a complete tasks.md following the template structure.
```

#### Implement Prompt

Save to `prompts/implement-prompt.md`:

```markdown
# Implementation Prompt

You are implementing a specific task from a task breakdown.

## Instructions

1. **Review Context**:
   - The specific task to implement
   - The plan and data model for technical details
   - Any existing code files provided
   - The project constitution for standards

2. **Generate Code That**:
   - Completes the task acceptance criteria
   - Follows the constitution's code standards
   - Integrates with existing code (if provided)
   - Includes appropriate comments and docstrings
   - Includes type hints (if specified in constitution)

3. **Output**:
   - Complete, runnable code for the specified file path
   - Any necessary imports
   - Brief explanation of key decisions

## Output Format

Return the complete code file content ready to be saved to the specified path.
```

---

## Brownfield Projects: Working with Existing Codebases

When adding features to existing projects, you need to provide additional context.

### Additional Context for Brownfield Projects

For **Phase 3 (Planning)** and **Phase 5 (Implementation)**, include:

```
EXISTING PROJECT CONTEXT:

1. Project Structure (run: tree -L 3 src/)
[paste output]

2. Key Existing Files:
[paste contents of relevant existing files, e.g.:]
- src/models/__init__.py
- src/models/base.py
- src/services/base.py
- src/api/routes.py
- pyproject.toml or requirements.txt

3. Patterns and Conventions:
[paste 1-2 existing similar implementations as examples]

4. Configuration:
[paste relevant config files]
```

### What to Include from Source Repo

| Phase | Files to Provide |
|-------|------------------|
| Planning | `tree` output, base classes, config files, README |
| Implementation | Direct dependencies, similar existing implementations, test examples |

### Example: Adding Auth to Existing Project

```
EXISTING PROJECT CONTEXT:

PROJECT STRUCTURE:
src/
├── models/
│   ├── __init__.py
│   └── base.py
├── services/
│   ├── __init__.py
│   └── base_service.py
├── api/
│   ├── __init__.py
│   ├── routes.py
│   └── deps.py
└── core/
    ├── config.py
    └── database.py

EXISTING BASE MODEL (src/models/base.py):
[paste file content]

EXISTING ROUTES PATTERN (src/api/routes.py):
[paste file content]

DATABASE CONFIG (src/core/database.py):
[paste file content]

When generating the plan and code, follow these existing patterns
and integrate with the established structure.
```

---

## Tips for Success

### 1. Be Explicit About Context

The LLM doesn't have access to your files. Always provide:
- Complete file contents (not summaries)
- Exact paths
- All relevant context

### 2. One Phase at a Time

Don't try to rush through phases. Each phase builds on the previous:
- Spec issues compound in planning
- Planning issues compound in tasks
- Task issues compound in implementation

### 3. Save Everything

Version control your `sdd-chat/` repo just like code:
- Commit after each phase
- Use meaningful commit messages
- Track iterations on specs

### 4. Review LLM Output

Don't blindly copy-paste:
- Verify spec has no tech details
- Verify plan follows constitution
- Verify tasks have correct paths
- Test generated code

### 5. Iterate on Clarifications

If you find ambiguities during planning or implementation:
- Go back to the spec
- Add clarifications
- Update downstream artifacts

### 6. Keep Context Bundles Small

If context is too large:
- Split into multiple chat sessions
- Summarize completed work
- Focus on relevant sections only

### 7. Use the CLI Helper

The `sdd-chat` CLI tool (provided with this guide) automates:
- Context bundle assembly
- Directory creation
- Progress tracking

---

## Appendix: File Naming Conventions

### Feature Directories
```
NNN-short-feature-name/
```
- `NNN`: Three-digit number (001, 002, etc.)
- `short-feature-name`: Lowercase, hyphen-separated

### Examples
```
001-user-authentication/
002-password-reset/
003-session-management/
```

---

## Appendix: Checklist for Each Phase

### Before Phase 1 (Specification)
- [ ] Constitution exists for project
- [ ] Feature directory created
- [ ] Feature description written (WHAT/WHY, not HOW)

### Before Phase 3 (Planning)
- [ ] All [NEEDS CLARIFICATION] markers resolved
- [ ] Spec reviewed and approved
- [ ] Tech stack decisions made

### Before Phase 4 (Tasks)
- [ ] plan.md complete
- [ ] data-model.md complete (if needed)
- [ ] contracts/ complete (if needed)
- [ ] Plan follows constitution

### Before Phase 5 (Implementation)
- [ ] tasks.md complete
- [ ] Tasks have exact file paths
- [ ] Dependencies are clear
- [ ] Source repo context gathered (for brownfield)

---

*SDD-Chat Guide v1.0 - Based on GitHub Spec Kit principles*
