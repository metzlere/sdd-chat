# QuickSpec Prompt

You are helping implement a small feature using the QuickSpec workflow - a lightweight, streamlined 3-phase approach (spec → plan → build).

## When to Use QuickSpec

Use QuickSpec for:
- Features touching <5-7 files
- Simple, well-understood requirements
- Bug fixes, small enhancements, UI tweaks
- Quick iterations without heavy documentation

Use the full 6-phase workflow for:
- Complex features touching 5+ files
- Features with multiple stakeholders
- New features requiring significant planning
- API changes or architecture work

## Instructions

Follow this 3-phase workflow:

### Phase 1: Spec

Create a lightweight specification with:
- **What**: 1-2 sentences describing what you're building
- **Why**: 1 sentence explaining user/business value
- **Acceptance Criteria**: 3-5 specific, testable criteria
- **Out of Scope**: Explicitly excluded items

Keep it minimal. If you need clarification, ask 1-2 questions before proceeding.

**Wait for user confirmation before proceeding to Phase 2.**

### Phase 2: Plan

After reviewing the spec and scanning the codebase, create a plan with:
- **Files**: Concrete file paths with brief descriptions of changes
- **Approach**: 2-4 sentences on implementation strategy
- **Risks**: Any potential issues or dependencies

Flag if the scope seems larger than quickspec is designed for (>5-7 files).

**Wait for user confirmation before proceeding to Phase 3.**

### Phase 3: Build

Implement the feature:
1. Follow the plan
2. Respect existing code conventions
3. Write tests if the project has them
4. Check off acceptance criteria as you complete them
5. Run existing tests/linting and fix issues

When done, summarize:
- Files changed
- Any deviations from plan
- How to verify it works

## Guidelines

- Be direct, no filler
- If the plan was wrong, update it and explain why
- If scope creeps, note it in "Out of Scope" for follow-up
- Keep momentum — this is for small, quick features
- Refer to constitution.md (if exists) and CLAUDE.md for project standards
