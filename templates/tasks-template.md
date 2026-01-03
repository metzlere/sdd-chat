# Task Breakdown: [FEATURE_NAME]

**Feature**: [NNN-feature-name]
**Plan Reference**: [link to plan.md]
**Created**: [DATE]

---

## Task Legend

- **[P]**: Can run in parallel with other [P] tasks in same phase
- **Story**: Which user story this task belongs to (US1, US2, etc.)
- **Depends**: Tasks that must complete first

---

## Phase 1: Foundation

### T001: [Task Title]

- **File**: [exact file path, e.g., src/models/user.py]
- **Story**: Foundation (all stories)
- **Depends**: None
- **Description**: [What this task creates/modifies]
- **Acceptance**: [How to verify task is complete]

### T002: [Task Title] [P]

- **File**: [exact file path]
- **Story**: Foundation
- **Depends**: T001
- **Description**: [Description]
- **Acceptance**: [Verification]

### T003: [Task Title] [P]

- **File**: [exact file path]
- **Story**: Foundation
- **Depends**: T001
- **Description**: [Description]
- **Acceptance**: [Verification]

---

## Phase 2: User Story Implementation

### User Story 1: [Title from spec]

#### T004: [Task Title]

- **File**: [path]
- **Story**: US1
- **Depends**: T001, T002
- **Description**: [Description]
- **Acceptance**: [Verification]

#### T005: [Task Title] [P]

- **File**: [path]
- **Story**: US1
- **Depends**: T004
- **Description**: [Description]
- **Acceptance**: [Verification]

**Checkpoint US1**: After T005, US1 should be independently testable.

---

### User Story 2: [Title from spec]

#### T006: [Task Title] [P]

- **File**: [path]
- **Story**: US2
- **Depends**: T001, T002
- **Description**: [Description]
- **Acceptance**: [Verification]

#### T007: [Task Title]

- **File**: [path]
- **Story**: US2
- **Depends**: T006
- **Description**: [Description]
- **Acceptance**: [Verification]

**Checkpoint US2**: After T007, US2 should be independently testable.

---

## Phase 3: Integration

### T008: [Task Title]

- **File**: [path]
- **Story**: All
- **Depends**: T005, T007
- **Description**: [Description - typically API endpoints, routes]
- **Acceptance**: [Verification]

### T009: [Task Title] [P]

- **File**: [path]
- **Story**: All
- **Depends**: T008
- **Description**: [Description]
- **Acceptance**: [Verification]

---

## Phase 4: Polish

### T010: [Task Title]

- **File**: [path]
- **Story**: All
- **Depends**: T008, T009
- **Description**: [Error handling, logging, etc.]
- **Acceptance**: [Verification]

### T011: [Task Title]

- **File**: [path]
- **Story**: All
- **Depends**: T010
- **Description**: [Documentation, cleanup]
- **Acceptance**: [Verification]

---

## Progress Tracking

| Task | Status | Notes |
|------|--------|-------|
| T001 | ⬜ Not Started | |
| T002 | ⬜ Not Started | |
| T003 | ⬜ Not Started | |
| T004 | ⬜ Not Started | |
| T005 | ⬜ Not Started | |
| T006 | ⬜ Not Started | |
| T007 | ⬜ Not Started | |
| T008 | ⬜ Not Started | |
| T009 | ⬜ Not Started | |
| T010 | ⬜ Not Started | |
| T011 | ⬜ Not Started | |

---

## Dependency Graph

```
T001 (Foundation)
 ├── T002 [P]
 │    └── T004 (US1)
 │         └── T005 [P]
 │              └── T008 (Integration)
 └── T003 [P]
      └── T006 (US2) [P]
           └── T007
                └── T008 (Integration)
                     └── T009 [P]
                          └── T010 (Polish)
                               └── T011
```

---

## Implementation Notes

- Tasks marked [P] can be worked on in parallel if resources allow
- Each User Story checkpoint should result in testable functionality
- Update Progress Tracking table as tasks are completed
- If a task is blocked, note the blocker in the Notes column
- Consider creating a git commit after each task or phase
