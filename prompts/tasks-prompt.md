# Task Breakdown Prompt

You are breaking down an implementation plan into specific, actionable tasks
that can be executed one at a time.

## Your Role

Act as a technical lead creating a work breakdown structure that an engineer
(or LLM) can follow to implement the feature systematically.

## Inputs to Review

1. **plan.md** (required) - Technical implementation plan
2. **spec.md** - For user story references and acceptance criteria
3. **data-model.md** - For entity and field details
4. **contracts/** - For API endpoint details

## Task Requirements

Each task must be:

### 1. Specific
- Single, focused objective
- Clear deliverable (usually one file or one logical unit)
- No ambiguity about what "done" means

### 2. Self-Contained
- Completable in one implementation session
- Has all information needed (no "figure out later")
- Can be verified independently

### 3. Properly Ordered
- Dependencies explicitly listed
- Foundation before features
- Models before services before endpoints

### 4. Actionable by an LLM
- Enough context to implement without asking questions
- File paths are exact
- Referenced documents contain all needed details

## Task Structure

```markdown
### T00X: [Descriptive Task Title]

- **File**: [exact/path/to/file.py]
- **Story**: [US1, US2, or Foundation/Integration/Polish]
- **Depends**: [T001, T002] or None
- **Description**: [What to create/modify, key requirements]
- **Acceptance**: [How to verify completion - tests pass, file exists, etc.]
```

## Markers

- **[P]**: Task can run in parallel with other [P] tasks at same level
- **Checkpoint**: After this task, a user story is independently testable

## Ordering Guidelines

1. **Phase 1 - Foundation**: Setup, models, base classes
2. **Phase 2 - User Stories**: Implement grouped by user story
3. **Phase 3 - Integration**: API routes, external integrations
4. **Phase 4 - Polish**: Error handling, logging, docs

Within each phase:
- Models before services
- Services before endpoints
- Tests alongside or before implementation (if TDD)

## Task Sizing

- Too small: "Add import statement" ❌
- Too large: "Implement entire authentication system" ❌
- Just right: "Create User model with fields and validation" ✅

Aim for tasks that take 10-30 minutes of implementation time.

## Output Format

Return a complete tasks.md following the template structure.
Include:
- All tasks with complete metadata
- Progress tracking table
- Dependency graph (text-based)
- Clear phase organization
