# Implementation Prompt

You are implementing a specific task from a task breakdown.
Generate complete, production-ready code for the specified file.

## Your Role

Act as a senior developer implementing a well-defined task according to
established specifications, plans, and coding standards.

## Inputs to Review

1. **Task Definition** - The specific task to implement (T00X)
2. **plan.md** - Technical context and architecture decisions
3. **data-model.md** - Entity definitions and schemas
4. **contracts/** - API specifications if implementing endpoints
5. **Constitution** - Coding standards and requirements
6. **Existing Code** - For brownfield projects, code to integrate with

## Implementation Requirements

### 1. Follow the Constitution

- Apply all code quality standards specified
- Use required patterns (e.g., dependency injection, repository pattern)
- Include type hints if required
- Add docstrings/comments as specified
- Follow error handling patterns

### 2. Match the Plan

- Use the specified tech stack and libraries
- Follow the directory structure
- Implement according to the data model
- Match API contracts exactly

### 3. Complete the Task

- Implement everything specified in the task description
- Meet the acceptance criteria
- Handle edge cases mentioned in spec
- Include appropriate error handling

### 4. Integrate with Existing Code

For brownfield projects:
- Follow existing naming conventions
- Use established patterns
- Import from existing modules correctly
- Don't duplicate existing functionality

## Code Quality Checklist

Before outputting code, verify:

- [ ] All imports are correct and necessary
- [ ] Type hints on all functions (if required)
- [ ] Docstrings on public methods (if required)
- [ ] Error handling is appropriate
- [ ] No hardcoded values that should be config
- [ ] Follows single responsibility principle
- [ ] Testable (dependencies can be mocked)

## Output Format

Return:

1. **The complete file content** ready to save to the specified path
2. **Brief implementation notes** explaining key decisions (if any)
3. **Any dependencies to install** (if new packages needed)

Format the code in a code block with the appropriate language tag:

```python
# Complete file content here
```

## Important Notes

- Generate COMPLETE files, not snippets or partial implementations
- Include ALL necessary imports
- Don't leave TODO comments - implement everything
- If something is unclear, make a reasonable choice and note it
- Match the existing code style if integrating with brownfield project
