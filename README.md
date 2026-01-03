# SDD-Chat

**Spec-Driven Development via Chat Interface**

A workflow and CLI tool for practicing [GitHub Spec Kit](https://github.com/github/spec-kit)-style Spec-Driven Development (SDD) in constrained environments where agentic coding tools are unavailable.

## Overview

SDD-Chat adapts the structured development methodology from GitHub Spec Kit for use with any LLM chat interface. Instead of automated slash commands, you manually copy context bundles into your chat and save the generated artifacts.

### The Core Principle

> Specifications become executable. You define *what* you want to build and *why* before diving into *how*.

### The 6-Phase Workflow

| Phase | Name | Focus |
|-------|------|-------|
| 0 | Constitution | Project principles (once per project) |
| 1 | Specification | WHAT to build, WHY (no tech details) |
| 2 | Clarification | Resolve ambiguities |
| 3 | Planning | HOW to build (technical design) |
| 4 | Tasks | Break into actionable items |
| 5 | Implementation | Generate code task by task |

## Quick Start

### 1. Clone/Initialize this repo

```bash
git clone <this-repo> sdd-chat
cd sdd-chat
```

### 2. Install the CLI (optional but recommended)

```bash
pip install typer
# Then use: python sdd_chat.py <command>
# Or create an alias: alias sdd-chat='python /path/to/sdd_chat.py'
```

### 3. Initialize a project

```bash
python sdd_chat.py init my-analytics-project
```

### 4. Follow the workflow

```bash
# Create constitution (one time)
python sdd_chat.py phase 0

# Start a feature
python sdd_chat.py feature user-auth

# Work through phases
python sdd_chat.py phase 1  # Specification
python sdd_chat.py phase 2  # Clarification
python sdd_chat.py phase 3  # Planning
python sdd_chat.py phase 4  # Tasks
python sdd_chat.py phase 5  # Implementation
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `init <project>` | Initialize a new project |
| `feature <name>` | Create a new feature for current project |
| `use <project> [-f feature]` | Switch to a project/feature |
| `status` | Show current project and artifact status |
| `list` | List all projects and features |
| `phase <0-5>` | Get guidance for a specific phase |
| `bundle <0-5>` | Generate context bundle for copy/paste |
| `complete <task-id>` | Mark a task as complete |
| `setup` | Create initial directory structure |

## Directory Structure

```
sdd-chat/
├── sdd_chat.py              # CLI tool
├── templates/               # Document templates
│   ├── constitution-template.md
│   ├── spec-template.md
│   ├── plan-template.md
│   └── tasks-template.md
├── prompts/                 # LLM prompts for each phase
│   ├── constitution-prompt.md
│   ├── specify-prompt.md
│   ├── clarify-prompt.md
│   ├── plan-prompt.md
│   ├── tasks-prompt.md
│   └── implement-prompt.md
└── projects/                # Your projects
    └── my-project/
        ├── constitution.md
        └── specs/
            ├── 001-feature-a/
            │   ├── spec.md
            │   ├── plan.md
            │   ├── data-model.md
            │   ├── tasks.md
            │   └── contracts/
            └── 002-feature-b/
                └── ...
```

## Using Context Bundles

Each phase requires specific context to be provided to the LLM. The CLI assembles these "context bundles" for you:

```bash
# Generate bundle for Phase 3 (Planning)
python sdd_chat.py bundle 3

# Output goes to stdout - copy everything between the markers
# into your LLM chat
```

The bundle includes:
- Relevant prompts and templates
- Previously generated artifacts (constitution, spec, etc.)
- Instructions for what to add (your input, tech decisions, etc.)

## Workflow Details

See [SDD-CHAT-GUIDE.md](SDD-CHAT-GUIDE.md) for comprehensive documentation including:

- Detailed phase-by-phase instructions
- Complete template contents
- Brownfield project guidance
- Tips for success

## Why SDD-Chat?

Traditional "vibe coding" with LLMs produces inconsistent results because:
- Context is lost between sessions
- Requirements live only in chat history
- No shared understanding of project principles

SDD-Chat solves this by:
- Maintaining specifications as version-controlled artifacts
- Providing consistent context through templates and prompts
- Enforcing a structured workflow that catches issues early

## Credits

Based on [GitHub Spec Kit](https://github.com/github/spec-kit) and the Spec-Driven Development methodology.

## License

MIT
