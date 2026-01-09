# QuickSpec: Lightweight Spec-Driven Development

A streamlined 3-phase workflow for small features and quick iterations using an LLM chat interface. QuickSpec provides the structure of Spec-Driven Development without the overhead of the full 6-phase workflow.

---

## Table of Contents

1. [Overview](#overview)
2. [When to Use QuickSpec](#when-to-use-quickspec)
3. [Repository Structure](#repository-structure)
4. [Quick Reference: The 3-Phase Workflow](#quick-reference-the-3-phase-workflow)
5. [Phase 1: Spec](#phase-1-spec)
6. [Phase 2: Plan](#phase-2-plan)
7. [Phase 3: Build](#phase-3-build)
8. [Context Bundle Template](#context-bundle-template)
9. [Tips for Success](#tips-for-success)

---

## Overview

### What is QuickSpec?

QuickSpec is a lightweight alternative to the full 6-phase SDD-Chat workflow, designed for small features that need structure but not heavy documentation. It maintains the core principle of spec-driven development - defining WHAT and WHY before HOW - but streamlines the process into three focused phases.

### The Workflow at a Glance

```
┌─────────────────────────────────────────────────────────┐
│                  QuickSpec Workflow                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐          │
│   │  Phase 1 │───▶│  Phase 2 │───▶│  Phase 3 │          │
│   │   Spec   │    │   Plan   │    │  Build   │          │
│   │ (WHAT)   │    │  (HOW)   │    │ (CODE)   │          │
│   └──────────┘    └──────────┘    └──────────┘          │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Key Differences from Full Workflow

| Aspect | Full 6-Phase Workflow | QuickSpec |
|--------|----------------------|-----------|
| Phases | 6 (Constitution → Spec → Clarify → Plan → Tasks → Implement) | 3 (Spec → Plan → Build) |
| Artifacts | constitution.md, spec.md, plan.md, tasks.md, research.md, data-model.md, contracts/ | spec.md, plan.md |
| Best For | Complex features, 5+ files, multiple stakeholders | Simple features, <5-7 files, quick iterations |
| Time Investment | Hours to days | Minutes to hours |
| Documentation Depth | Comprehensive | Minimal but sufficient |

---

## When to Use QuickSpec

### Use QuickSpec For:

- **Small Features**: Touching fewer than 5-7 files
- **Bug Fixes**: That require some design thinking
- **UI Tweaks**: Small enhancements to existing interfaces
- **Quick Iterations**: Prototyping or experimental features
- **Well-Understood Requirements**: Clear, straightforward changes
- **Single Developer Work**: No need for stakeholder alignment

### Use Full Workflow For:

- **Complex Features**: Touching 5+ files or multiple subsystems
- **New Architecture**: Significant new patterns or infrastructure
- **Multiple Stakeholders**: Requiring alignment and review
- **API Changes**: Public interfaces or breaking changes
- **Critical Features**: High-risk or business-critical functionality
- **Team Coordination**: Work requiring parallel development

### Decision Framework

```
Is the feature touching >5 files? ──YES──▶ Full Workflow
         │
        NO
         │
         ▼
Does it require stakeholder alignment? ──YES──▶ Full Workflow
         │
        NO
         │
         ▼
Is it a new architecture pattern? ──YES──▶ Full Workflow
         │
        NO
         │
         ▼
    QuickSpec ✓
```

---

## Repository Structure

QuickSpec features live in a `.quickspec/` directory within your project (or in the `sdd-chat/` meta-repo).

### Option 1: In-Project (Recommended)

```
your-project/
├── .quickspec/
│   ├── 001-feature-name/
│   │   ├── spec.md
│   │   └── plan.md
│   └── 002-another-feature/
│       ├── spec.md
│       └── plan.md
├── src/
├── tests/
└── README.md
```

### Option 2: Meta-Repository

```
sdd-chat/
├── templates/
│   └── quickspec-template.md
├── prompts/
│   └── quickspec-prompt.md
└── projects/
    └── your-project/
        └── .quickspec/
            ├── 001-feature-name/
            └── 002-another-feature/
```

**Recommendation**: Use Option 1 (in-project) for quickspec features since they're lightweight and benefit from being tracked with the code.

---

## Quick Reference: The 3-Phase Workflow

| Phase | Focus | Duration | Input | Output | Approval Required |
|-------|-------|----------|-------|--------|-------------------|
| **1. Spec** | WHAT & WHY | 5-10 min | Feature description | spec.md (What/Why/Criteria/OutOfScope) | ✅ Yes |
| **2. Plan** | HOW | 10-15 min | spec.md + codebase scan | plan.md (Files/Approach/Risks) | ✅ Yes |
| **3. Build** | CODE | Varies | plan.md + spec.md | Implementation + tests | No |

---

## Phase 1: Spec

Define WHAT you're building and WHY it matters.

### What You Provide to the LLM

**Context Bundle:**
```
1. QuickSpec template (templates/quickspec-template.md)
2. QuickSpec prompt (prompts/quickspec-prompt.md)
3. Your feature description (1-3 sentences)
4. [Optional] Project constitution or CLAUDE.md
```

### Workflow

1. **Create** the feature directory:
   ```bash
   mkdir -p .quickspec/001-feature-name
   ```

2. **Describe** your feature to the LLM:
   ```
   I need a quickspec for:
   [Your 1-3 sentence description of the feature]

   [Paste quickspec-prompt.md]
   ```

3. **Review** the generated spec for:
   - Clear WHAT (1-2 sentences)
   - Clear WHY (business/user value)
   - Testable acceptance criteria (3-5 items)
   - Explicit out-of-scope items

4. **Ask clarifying questions** (1-2 max) if needed

5. **Approve** and save to: `.quickspec/001-feature-name/spec.md`

### Example Prompt

```
Create a quickspec for this feature:

Add a "dark mode" toggle to the user settings page that persists
the user's preference and applies the theme across all pages.

Here is the quickspec prompt:
[paste prompts/quickspec-prompt.md]

Generate the spec.md content.
```

### What a Good Spec Looks Like

**✅ Good - Clear and Focused:**
```markdown
## What
Add a dark mode toggle switch to the settings page that saves the
user's theme preference and applies it site-wide.

## Why
Users working in low-light environments need a darker UI to reduce
eye strain and improve readability.

## Acceptance Criteria
- [ ] Toggle switch appears on /settings page
- [ ] Clicking toggle changes theme immediately
- [ ] Theme preference persists across sessions
- [ ] Theme applies to all pages after refresh
- [ ] Default theme is light mode for new users

## Out of Scope
- System theme detection (respecting OS preference)
- Multiple theme options beyond light/dark
- Custom color customization
```

**❌ Bad - Too Vague or Too Technical:**
```markdown
## What
Implement dark mode using CSS variables and localStorage

## Why
Everyone wants dark mode these days

## Acceptance Criteria
- [ ] Works
- [ ] Looks good
- [ ] Saves preference
```

---

## Phase 2: Plan

Define HOW you'll implement the feature.

### What You Provide to the LLM

**Context Bundle:**
```
1. The approved spec.md
2. Codebase context (structure, patterns)
3. [Optional] Constitution or CLAUDE.md
```

### Workflow

1. **Scan** your codebase for context:
   ```bash
   # Get project structure
   tree -L 3 src/

   # Find similar patterns
   grep -r "similar_pattern" src/
   ```

2. **Provide** context to the LLM:
   ```
   Review this spec and generate a technical plan:

   SPEC:
   [paste spec.md]

   PROJECT STRUCTURE:
   [paste tree output]

   SIMILAR EXISTING CODE:
   [paste 1-2 similar implementations if relevant]

   Generate a plan.md with: Files to change, Approach, and Risks.
   ```

3. **Review** the plan for:
   - Concrete file paths (not vague descriptions)
   - Clear implementation approach (2-4 sentences)
   - Identified risks or dependencies

4. **Flag** if scope seems too large (>5-7 files = use full workflow)

5. **Approve** and save to: `.quickspec/001-feature-name/plan.md`

### Example Prompt

```
Generate an implementation plan for this quickspec:

SPEC:
[paste .quickspec/001-dark-mode/spec.md]

PROJECT STRUCTURE:
src/
├── components/
│   ├── Settings/
│   │   └── SettingsPage.tsx
│   └── Layout/
│       └── ThemeProvider.tsx
├── hooks/
│   └── useLocalStorage.ts
└── styles/
    ├── themes.css
    └── variables.css

EXISTING PATTERN (src/hooks/useLocalStorage.ts):
[paste file content]

Generate plan.md following the quickspec template.
```

### What a Good Plan Looks Like

**✅ Good - Specific and Actionable:**
```markdown
## Files
- `src/components/Settings/SettingsPage.tsx` — Add toggle switch component
- `src/components/Layout/ThemeProvider.tsx` — Add theme state and logic
- `src/hooks/useTheme.ts` — New hook for theme management
- `src/styles/themes.css` — Add dark theme CSS variables
- `tests/hooks/useTheme.test.ts` — Unit tests for theme hook

## Approach
Create a custom `useTheme` hook that wraps `useLocalStorage` to persist
the theme preference. The ThemeProvider component will consume this hook
and apply a `data-theme` attribute to the document root. CSS variables
in `themes.css` will define light/dark color schemes. The settings page
will render a toggle that calls the theme setter.

## Risks
- Existing inline styles may not respect CSS variables and need updates
- Theme flash on page load if not handled in SSR context
```

**❌ Bad - Vague or Incomplete:**
```markdown
## Files
- Some component files
- CSS files

## Approach
Add dark mode using React context and CSS

## Risks
- None
```

---

## Phase 3: Build

Implement the feature following the plan.

### What You Provide to the LLM

**Context Bundle:**
```
1. spec.md (for acceptance criteria)
2. plan.md (for implementation details)
3. Existing source files being modified
4. [Optional] Test patterns
```

### Workflow

1. **Implement** file by file from the plan:
   ```
   Implement this file from the plan:

   PLAN:
   [paste plan.md]

   ACCEPTANCE CRITERIA:
   [paste criteria from spec.md]

   FILE TO IMPLEMENT: src/hooks/useTheme.ts

   EXISTING PATTERN (useLocalStorage):
   [paste src/hooks/useLocalStorage.ts]

   Generate the complete file content.
   ```

2. **Test** as you go:
   - Manually verify each file works
   - Run existing tests
   - Check acceptance criteria

3. **Update** the plan if you deviate:
   - Note why in plan.md
   - Update affected files list

4. **Handle** scope creep:
   - If feature grows beyond 5-7 files, pause
   - Consider splitting into multiple quickspecs
   - Or migrate to full workflow

5. **Complete** by checking off all acceptance criteria in spec.md

### Implementation Tips

**Work Incrementally:**
```
Session 1: Implement core hook (useTheme.ts)
Session 2: Add ThemeProvider logic
Session 3: Add Settings toggle
Session 4: Add tests and polish
```

**Stay Focused:**
- Only implement what's in the plan
- Defer out-of-scope items for future quickspecs
- Don't refactor unrelated code

**Document Deviations:**
Update plan.md if you change approach:
```markdown
## Implementation Notes

Changed `useTheme` to use Context instead of prop drilling
because Settings and Layout components share no common parent.
Added ThemeContext.tsx (not originally planned).
```

---

## Context Bundle Template

### QuickSpec Template

Save to `templates/quickspec-template.md`:

```markdown
# [Feature Name]

## What
[1-2 sentences - what you're building]

## Why
[1 sentence - user/business value]

## Acceptance Criteria
- [ ] [criterion 1]
- [ ] [criterion 2]
- [ ] [criterion 3]

## Out of Scope
- [excluded item]

---

# Plan

## Files
- `path/to/file.py` — [change description]
- `path/to/new.py` — [create, purpose]

## Approach
[2-4 sentences on implementation strategy]

## Risks
- [potential issue, if any]

---

# Implementation Notes
[Optional - add deviations, learnings, follow-up items as you build]
```

### QuickSpec Prompt

Save to `prompts/quickspec-prompt.md`:

```markdown
# QuickSpec Prompt

You are helping implement a small feature using the QuickSpec workflow -
a lightweight, streamlined 3-phase approach (spec → plan → build).

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
```

---

## Tips for Success

### 1. Know When to Upgrade to Full Workflow

If you find yourself needing:
- More than 7 files changed
- Multiple clarification rounds
- Stakeholder input or alignment
- Detailed data modeling or API contracts

**Stop and switch to the full 6-phase workflow.** QuickSpec is for speed, not complexity.

### 2. Use Acceptance Criteria as Your North Star

During Phase 3, constantly refer back to the acceptance criteria:
```markdown
- [x] Toggle switch appears on /settings page ✓
- [x] Clicking toggle changes theme immediately ✓
- [ ] Theme preference persists across sessions ← YOU ARE HERE
- [ ] Theme applies to all pages after refresh
- [ ] Default theme is light mode for new users
```

Check them off as you complete them. This keeps you focused.

### 3. Document Deviations

Plans are wrong sometimes. When reality diverges:

```markdown
## Implementation Notes

**Deviation from Plan**:
Originally planned to use localStorage directly, but discovered
the project already has a useStorage hook that handles SSR edge
cases. Used that instead. Added src/hooks/useStorage.ts to context.
```

### 4. Batch Small Related Features

Instead of one large feature, break into multiple quickspecs:

```
001-dark-mode-toggle     (core functionality)
002-theme-persistence    (if complex)
003-theme-animations     (polish)
```

Each quickspec stays small and focused.

### 5. Keep It Moving

QuickSpec is about momentum. If you're stuck:
- **Time-box** decisions (5 minutes max)
- **Make a choice** and document it in plan.md
- **Move forward** - you can refactor later

Avoid perfectionism. Ship, learn, iterate.

### 6. Learn from Full Workflow Practices

Even though QuickSpec is lightweight, borrow good practices:
- Review spec before planning
- Review plan before building
- Test as you implement
- Keep artifacts in version control

### 7. Combine with Constitution

If your project has a constitution.md (from full workflow), reference it in Phase 1:

```
Create a quickspec following these project standards:

CONSTITUTION:
[paste relevant sections]

FEATURE:
[your description]
```

This ensures consistency across both workflows.

---

## Workflow Comparison Cheat Sheet

| Question | Full Workflow | QuickSpec |
|----------|--------------|-----------|
| How many files? | 5+ files | <5-7 files |
| How many phases? | 6 phases | 3 phases |
| How many artifacts? | 6+ documents | 2 documents |
| Time to start coding? | Hours | Minutes |
| Stakeholder review needed? | Yes, multiple points | Optional, end only |
| When to use? | Complex, risky, or team features | Simple, quick, solo features |
| Example features | New auth system, API redesign | Bug fix, UI tweak, small enhancement |

---

## Appendix: Feature Naming Convention

```
NNN-short-feature-name/
```

- `NNN`: Three-digit number (001, 002, etc.)
- `short-feature-name`: Lowercase, hyphen-separated
- Keep it brief (3-5 words max)

### Examples

```
001-dark-mode-toggle
002-export-csv-button
003-fix-login-timeout
004-add-search-filter
```

---

## Appendix: Migration Path

### From QuickSpec to Full Workflow

If a quickspec grows too complex:

1. Create full workflow directory:
   ```bash
   mkdir -p specs/001-feature-name
   ```

2. Convert artifacts:
   - Expand spec.md to full template (add user stories, NFRs)
   - Expand plan.md (add research.md, data-model.md)
   - Add tasks.md

3. Continue with full workflow phases

### From Full Workflow to QuickSpec

For small follow-up features to a major feature:

```
specs/001-user-auth/              (full workflow)
.quickspec/001-auth-remember-me/  (quickspec extension)
.quickspec/002-auth-2fa-toggle/   (quickspec extension)
```

Use quickspec for small additions to completed full-workflow features.

---

*QuickSpec Guide v1.0 - Lightweight alternative to SDD-Chat's 6-phase workflow*
