#!/usr/bin/env python3
"""
SDD-Chat CLI: Interactive guide for Spec-Driven Development via chat interface.

This CLI helps you follow the SDD-Chat workflow by:
- Guiding you through each phase step-by-step
- Assembling context bundles for copy/paste into your LLM chat
- Tracking progress on features
- Managing project structure

Usage:
    sdd-chat init <project-name>      Initialize a new project
    sdd-chat phase <phase-number>     Start a specific phase
    sdd-chat bundle <phase-number>    Generate context bundle for a phase
    sdd-chat status                   Show current project/feature status
    sdd-chat list                     List all projects and features
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer

app = typer.Typer(
    name="sdd-chat",
    help="Interactive guide for Spec-Driven Development via chat interface.",
    add_completion=False,
)

# Configuration
SDD_CHAT_ROOT = Path.cwd()
PROJECTS_DIR = SDD_CHAT_ROOT / "projects"
TEMPLATES_DIR = SDD_CHAT_ROOT / "templates"
PROMPTS_DIR = SDD_CHAT_ROOT / "prompts"
STATE_FILE = SDD_CHAT_ROOT / ".sdd-chat-state.json"

# Phase definitions
PHASES = {
    0: {
        "name": "Constitution",
        "description": "Define project principles and standards",
        "artifacts": ["constitution.md"],
        "templates": ["constitution-template.md"],
        "prompts": ["constitution-prompt.md"],
    },
    1: {
        "name": "Specification",
        "description": "Define WHAT to build and WHY (no implementation details)",
        "artifacts": ["spec.md"],
        "templates": ["spec-template.md"],
        "prompts": ["specify-prompt.md"],
    },
    2: {
        "name": "Clarification",
        "description": "Resolve ambiguities in the specification",
        "artifacts": ["spec.md (updated)"],
        "templates": [],
        "prompts": ["clarify-prompt.md"],
    },
    3: {
        "name": "Planning",
        "description": "Define HOW to build (technical design)",
        "artifacts": ["plan.md", "research.md", "data-model.md", "contracts/"],
        "templates": ["plan-template.md"],
        "prompts": ["plan-prompt.md"],
    },
    4: {
        "name": "Task Breakdown",
        "description": "Break plan into actionable, ordered tasks",
        "artifacts": ["tasks.md"],
        "templates": ["tasks-template.md"],
        "prompts": ["tasks-prompt.md"],
    },
    5: {
        "name": "Implementation",
        "description": "Generate code for each task",
        "artifacts": ["(code files in source repo)"],
        "templates": [],
        "prompts": ["implement-prompt.md"],
    },
}


def load_state() -> dict:
    """Load the current state from the state file."""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"current_project": None, "current_feature": None, "current_quickspec": None}


def save_state(state: dict) -> None:
    """Save the current state to the state file."""
    STATE_FILE.write_text(json.dumps(state, indent=2))


def get_project_path(project: str) -> Path:
    """Get the path to a project directory."""
    return PROJECTS_DIR / project


def get_feature_path(project: str, feature: str) -> Path:
    """Get the path to a feature directory."""
    return PROJECTS_DIR / project / "specs" / feature


def list_projects() -> list[str]:
    """List all projects in the projects directory."""
    if not PROJECTS_DIR.exists():
        return []
    return [d.name for d in PROJECTS_DIR.iterdir() if d.is_dir()]


def list_features(project: str) -> list[str]:
    """List all features for a project."""
    specs_dir = PROJECTS_DIR / project / "specs"
    if not specs_dir.exists():
        return []
    return sorted([d.name for d in specs_dir.iterdir() if d.is_dir()])


def get_next_feature_number(project: str) -> int:
    """Get the next feature number for a project."""
    features = list_features(project)
    if not features:
        return 1
    numbers = []
    for f in features:
        if f[:3].isdigit():
            numbers.append(int(f[:3]))
    return max(numbers) + 1 if numbers else 1


def read_file_safe(path: Path) -> Optional[str]:
    """Safely read a file, returning None if it doesn't exist."""
    if path.exists():
        return path.read_text()
    return None


def get_quickspec_dir(project: str) -> Path:
    """Get the quickspec directory for a project."""
    return PROJECTS_DIR / project / ".quickspec"


def list_quickspec_features(project: str) -> list[str]:
    """List all quickspec features for a project."""
    quickspec_dir = get_quickspec_dir(project)
    if not quickspec_dir.exists():
        return []
    return sorted([d.name for d in quickspec_dir.iterdir() if d.is_dir()])


def get_next_quickspec_number(project: str) -> int:
    """Get the next quickspec feature number for a project."""
    features = list_quickspec_features(project)
    if not features:
        return 1
    numbers = []
    for f in features:
        if f[:3].isdigit():
            numbers.append(int(f[:3]))
    return max(numbers) + 1 if numbers else 1


def create_slug(description: str) -> str:
    """Create a kebab-case slug from a description."""
    import re
    # Convert to lowercase and replace spaces/underscores with hyphens
    slug = description.lower().replace("_", "-").replace(" ", "-")
    # Remove any characters that aren't alphanumeric or hyphens
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    # Remove consecutive hyphens
    slug = re.sub(r'-+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    return slug


def print_header(text: str) -> None:
    """Print a formatted header."""
    typer.echo()
    typer.secho("=" * 70, fg=typer.colors.CYAN)
    typer.secho(f"  {text}", fg=typer.colors.CYAN, bold=True)
    typer.secho("=" * 70, fg=typer.colors.CYAN)
    typer.echo()


def print_step(number: int, text: str) -> None:
    """Print a formatted step."""
    typer.secho(f"  [{number}] ", fg=typer.colors.GREEN, bold=True, nl=False)
    typer.echo(text)


def print_info(text: str) -> None:
    """Print info text."""
    typer.secho(f"  ℹ  {text}", fg=typer.colors.BLUE)


def print_warning(text: str) -> None:
    """Print warning text."""
    typer.secho(f"  ⚠  {text}", fg=typer.colors.YELLOW)


def print_error(text: str) -> None:
    """Print error text."""
    typer.secho(f"  ✗  {text}", fg=typer.colors.RED)


def print_success(text: str) -> None:
    """Print success text."""
    typer.secho(f"  ✓  {text}", fg=typer.colors.GREEN)


def print_file_content(label: str, content: str) -> None:
    """Print file content with a label."""
    typer.echo()
    typer.secho(f"─── {label} ───", fg=typer.colors.MAGENTA)
    typer.echo(content)
    typer.secho("─" * (len(label) + 8), fg=typer.colors.MAGENTA)


@app.command()
def init(project_name: str = typer.Argument(..., help="Name of the project to initialize")):
    """
    Initialize a new project with the SDD-Chat structure.
    
    Creates the project directory and constitution template.
    """
    print_header(f"Initializing Project: {project_name}")
    
    # Create directories
    project_path = get_project_path(project_name)
    specs_path = project_path / "specs"
    
    if project_path.exists():
        print_warning(f"Project '{project_name}' already exists.")
        if not typer.confirm("  Continue anyway?"):
            raise typer.Abort()
    
    # Create structure
    specs_path.mkdir(parents=True, exist_ok=True)
    print_success(f"Created: {project_path}")
    print_success(f"Created: {specs_path}")
    
    # Update state
    state = load_state()
    state["current_project"] = project_name
    state["current_feature"] = None
    save_state(state)
    
    print_info(f"Current project set to: {project_name}")
    typer.echo()
    typer.echo("  Next steps:")
    print_step(1, "Run 'sdd-chat phase 0' to create the project constitution")
    print_step(2, "Run 'sdd-chat feature <name>' to start a new feature")
    typer.echo()


@app.command()
def feature(
    name: str = typer.Argument(..., help="Short name for the feature (e.g., 'user-auth')"),
    project: Optional[str] = typer.Option(None, "--project", "-p", help="Project name (uses current if not specified)"),
):
    """
    Create a new feature and set it as current.
    
    Creates a numbered feature directory (e.g., 001-user-auth).
    """
    state = load_state()
    project = project or state.get("current_project")
    
    if not project:
        print_error("No project specified. Run 'sdd-chat init <project>' first.")
        raise typer.Abort()
    
    project_path = get_project_path(project)
    if not project_path.exists():
        print_error(f"Project '{project}' does not exist. Run 'sdd-chat init {project}' first.")
        raise typer.Abort()
    
    # Create feature directory
    feature_num = get_next_feature_number(project)
    feature_dir = f"{feature_num:03d}-{name}"
    feature_path = get_feature_path(project, feature_dir)
    
    print_header(f"Creating Feature: {feature_dir}")
    
    feature_path.mkdir(parents=True, exist_ok=True)
    print_success(f"Created: {feature_path}")
    
    # Update state
    state["current_project"] = project
    state["current_feature"] = feature_dir
    save_state(state)
    
    print_info(f"Current feature set to: {feature_dir}")
    typer.echo()
    typer.echo("  Next steps:")
    print_step(1, "Run 'sdd-chat phase 1' to create the specification")
    typer.echo()


@app.command()
def use(
    project: str = typer.Argument(..., help="Project name to switch to"),
    feature: Optional[str] = typer.Option(None, "--feature", "-f", help="Feature to switch to"),
):
    """
    Switch to a different project or feature.
    """
    project_path = get_project_path(project)
    if not project_path.exists():
        print_error(f"Project '{project}' does not exist.")
        raise typer.Abort()
    
    state = load_state()
    state["current_project"] = project
    
    if feature:
        feature_path = get_feature_path(project, feature)
        if not feature_path.exists():
            print_error(f"Feature '{feature}' does not exist in project '{project}'.")
            raise typer.Abort()
        state["current_feature"] = feature
    else:
        # Set to most recent feature if any
        features = list_features(project)
        state["current_feature"] = features[-1] if features else None
    
    save_state(state)
    
    print_success(f"Switched to project: {project}")
    if state["current_feature"]:
        print_success(f"Current feature: {state['current_feature']}")


@app.command()
def status():
    """
    Show current project and feature status.
    """
    state = load_state()
    
    print_header("SDD-Chat Status")
    
    project = state.get("current_project")
    feature = state.get("current_feature")
    
    if not project:
        print_warning("No project selected. Run 'sdd-chat init <project>' to start.")
        return
    
    typer.echo(f"  Project: {typer.style(project, fg=typer.colors.GREEN, bold=True)}")
    
    # Check constitution
    const_path = get_project_path(project) / "constitution.md"
    if const_path.exists():
        print_success("Constitution: ✓ exists")
    else:
        print_warning("Constitution: ✗ not created (run 'sdd-chat phase 0')")
    
    if feature:
        typer.echo(f"  Feature:  {typer.style(feature, fg=typer.colors.GREEN, bold=True)}")
        feature_path = get_feature_path(project, feature)
        
        # Check artifacts
        artifacts = {
            "spec.md": "Specification",
            "plan.md": "Plan",
            "research.md": "Research",
            "data-model.md": "Data Model",
            "tasks.md": "Tasks",
        }
        
        typer.echo()
        typer.echo("  Artifacts:")
        for filename, label in artifacts.items():
            path = feature_path / filename
            if path.exists():
                print_success(f"  {label}: ✓")
            else:
                typer.echo(f"    {label}: ✗")
    else:
        print_warning("No feature selected. Run 'sdd-chat feature <name>' to start one.")
    
    typer.echo()


@app.command("list")
def list_cmd():
    """
    List all projects and their features.
    """
    print_header("Projects and Features")
    
    projects = list_projects()
    
    if not projects:
        print_warning("No projects found. Run 'sdd-chat init <project>' to create one.")
        return
    
    state = load_state()
    current_project = state.get("current_project")
    current_feature = state.get("current_feature")
    
    for project in projects:
        marker = " ◀ current" if project == current_project else ""
        typer.secho(f"  {project}{marker}", fg=typer.colors.GREEN, bold=True)
        
        # Check constitution
        const_path = get_project_path(project) / "constitution.md"
        const_status = "✓" if const_path.exists() else "✗"
        typer.echo(f"    Constitution: {const_status}")
        
        features = list_features(project)
        if features:
            typer.echo("    Features:")
            for feat in features:
                feat_marker = " ◀" if project == current_project and feat == current_feature else ""
                typer.echo(f"      • {feat}{feat_marker}")
        else:
            typer.echo("    Features: (none)")
        typer.echo()


@app.command()
def phase(
    phase_number: int = typer.Argument(..., help="Phase number (0-5)"),
    project: Optional[str] = typer.Option(None, "--project", "-p", help="Project name"),
    feature: Optional[str] = typer.Option(None, "--feature", "-f", help="Feature name"),
):
    """
    Start a specific phase with step-by-step guidance.
    
    Phases:
      0 - Constitution (project-level)
      1 - Specification
      2 - Clarification
      3 - Planning
      4 - Task Breakdown
      5 - Implementation
    """
    if phase_number not in PHASES:
        print_error(f"Invalid phase number. Must be 0-5.")
        raise typer.Abort()
    
    state = load_state()
    project = project or state.get("current_project")
    feature = feature or state.get("current_feature")
    
    if not project:
        print_error("No project specified. Run 'sdd-chat init <project>' first.")
        raise typer.Abort()
    
    if phase_number > 0 and not feature:
        print_error("No feature specified. Run 'sdd-chat feature <name>' first.")
        raise typer.Abort()
    
    phase_info = PHASES[phase_number]
    print_header(f"Phase {phase_number}: {phase_info['name']}")
    
    typer.echo(f"  {phase_info['description']}")
    typer.echo()
    
    # Phase-specific guidance
    if phase_number == 0:
        _guide_phase_0(project)
    elif phase_number == 1:
        _guide_phase_1(project, feature)
    elif phase_number == 2:
        _guide_phase_2(project, feature)
    elif phase_number == 3:
        _guide_phase_3(project, feature)
    elif phase_number == 4:
        _guide_phase_4(project, feature)
    elif phase_number == 5:
        _guide_phase_5(project, feature)


@app.command()
def bundle(
    phase_number: int = typer.Argument(..., help="Phase number to generate bundle for"),
    project: Optional[str] = typer.Option(None, "--project", "-p", help="Project name"),
    feature: Optional[str] = typer.Option(None, "--feature", "-f", help="Feature name"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file for bundle"),
):
    """
    Generate a context bundle for copy/paste into your LLM chat.
    
    The bundle contains all necessary context for the specified phase.
    """
    if phase_number not in PHASES:
        print_error(f"Invalid phase number. Must be 0-5.")
        raise typer.Abort()
    
    state = load_state()
    project = project or state.get("current_project")
    feature = feature or state.get("current_feature")
    
    if not project:
        print_error("No project specified.")
        raise typer.Abort()
    
    if phase_number > 0 and not feature:
        print_error("No feature specified for phases 1-5.")
        raise typer.Abort()
    
    phase_info = PHASES[phase_number]
    print_header(f"Context Bundle: Phase {phase_number} ({phase_info['name']})")
    
    bundle_content = _generate_bundle(phase_number, project, feature)
    
    if output:
        output.write_text(bundle_content)
        print_success(f"Bundle saved to: {output}")
    else:
        typer.echo()
        typer.secho("─" * 70, fg=typer.colors.CYAN)
        typer.secho("COPY EVERYTHING BELOW THIS LINE INTO YOUR LLM CHAT:", fg=typer.colors.YELLOW, bold=True)
        typer.secho("─" * 70, fg=typer.colors.CYAN)
        typer.echo(bundle_content)
        typer.secho("─" * 70, fg=typer.colors.CYAN)
        typer.secho("COPY EVERYTHING ABOVE THIS LINE", fg=typer.colors.YELLOW, bold=True)
        typer.secho("─" * 70, fg=typer.colors.CYAN)


def _guide_phase_0(project: str):
    """Guide for Phase 0: Constitution."""
    project_path = get_project_path(project)
    const_path = project_path / "constitution.md"
    
    typer.echo("  Steps:")
    print_step(1, "Run 'sdd-chat bundle 0' to generate the context bundle")
    print_step(2, "Copy the bundle into your LLM chat")
    print_step(3, "Add your specific project constraints to the prompt")
    print_step(4, "Ask the LLM to generate the constitution")
    print_step(5, f"Save the output to: {const_path}")
    
    typer.echo()
    
    if const_path.exists():
        print_warning("Constitution already exists. It will be overwritten.")
    
    if typer.confirm("  Generate context bundle now?"):
        bundle_content = _generate_bundle(0, project, None)
        typer.echo()
        typer.secho("─" * 70, fg=typer.colors.CYAN)
        typer.echo(bundle_content)
        typer.secho("─" * 70, fg=typer.colors.CYAN)
        
        typer.echo()
        print_info("Copy the above into your LLM chat, add your constraints, and request the constitution.")
        print_info(f"Save the response to: {const_path}")


def _guide_phase_1(project: str, feature: str):
    """Guide for Phase 1: Specification."""
    feature_path = get_feature_path(project, feature)
    spec_path = feature_path / "spec.md"
    const_path = get_project_path(project) / "constitution.md"
    
    if not const_path.exists():
        print_error("Constitution not found. Run 'sdd-chat phase 0' first.")
        raise typer.Abort()
    
    typer.echo("  Steps:")
    print_step(1, "Run 'sdd-chat bundle 1' to generate the context bundle")
    print_step(2, "Copy the bundle into your LLM chat")
    print_step(3, "Add your feature description (WHAT and WHY, no tech details)")
    print_step(4, "Ask the LLM to generate the specification")
    print_step(5, f"Save the output to: {spec_path}")
    
    typer.echo()
    print_info("Remember: NO implementation details in specs!")
    print_info("Focus on user stories, requirements, and success criteria.")
    
    if typer.confirm("  Generate context bundle now?"):
        bundle_content = _generate_bundle(1, project, feature)
        typer.echo()
        typer.secho("─" * 70, fg=typer.colors.CYAN)
        typer.echo(bundle_content)
        typer.secho("─" * 70, fg=typer.colors.CYAN)


def _guide_phase_2(project: str, feature: str):
    """Guide for Phase 2: Clarification."""
    feature_path = get_feature_path(project, feature)
    spec_path = feature_path / "spec.md"
    
    if not spec_path.exists():
        print_error("Specification not found. Run 'sdd-chat phase 1' first.")
        raise typer.Abort()
    
    typer.echo("  Steps:")
    print_step(1, "Run 'sdd-chat bundle 2' to generate the context bundle")
    print_step(2, "Copy the bundle into your LLM chat")
    print_step(3, "Answer any clarification questions from the LLM")
    print_step(4, "Ask the LLM to update the spec with clarifications")
    print_step(5, f"Save the updated spec to: {spec_path}")
    
    typer.echo()
    
    # Check for [NEEDS CLARIFICATION] markers
    spec_content = spec_path.read_text()
    if "[NEEDS CLARIFICATION" in spec_content:
        print_warning("Found [NEEDS CLARIFICATION] markers in spec - clarification recommended.")
    else:
        print_info("No obvious clarification markers found. You may skip this phase.")
    
    if typer.confirm("  Generate context bundle now?"):
        bundle_content = _generate_bundle(2, project, feature)
        typer.echo()
        typer.secho("─" * 70, fg=typer.colors.CYAN)
        typer.echo(bundle_content)
        typer.secho("─" * 70, fg=typer.colors.CYAN)


def _guide_phase_3(project: str, feature: str):
    """Guide for Phase 3: Planning."""
    feature_path = get_feature_path(project, feature)
    spec_path = feature_path / "spec.md"
    plan_path = feature_path / "plan.md"
    
    if not spec_path.exists():
        print_error("Specification not found. Run 'sdd-chat phase 1' first.")
        raise typer.Abort()
    
    typer.echo("  Steps:")
    print_step(1, "Run 'sdd-chat bundle 3' to generate the context bundle")
    print_step(2, "Copy the bundle into your LLM chat")
    print_step(3, "Add your technical stack decisions")
    print_step(4, "Ask the LLM to generate: plan.md, research.md, data-model.md")
    print_step(5, f"Save outputs to: {feature_path}/")
    
    typer.echo()
    print_info("Provide: language, framework, database, testing approach, etc.")
    print_info("For brownfield projects, also include existing code context.")
    
    typer.echo()
    typer.echo("  Expected outputs:")
    typer.echo(f"    • {plan_path}")
    typer.echo(f"    • {feature_path}/research.md")
    typer.echo(f"    • {feature_path}/data-model.md")
    typer.echo(f"    • {feature_path}/contracts/api-spec.json (if applicable)")
    
    if typer.confirm("  Generate context bundle now?"):
        bundle_content = _generate_bundle(3, project, feature)
        typer.echo()
        typer.secho("─" * 70, fg=typer.colors.CYAN)
        typer.echo(bundle_content)
        typer.secho("─" * 70, fg=typer.colors.CYAN)


def _guide_phase_4(project: str, feature: str):
    """Guide for Phase 4: Task Breakdown."""
    feature_path = get_feature_path(project, feature)
    plan_path = feature_path / "plan.md"
    tasks_path = feature_path / "tasks.md"
    
    if not plan_path.exists():
        print_error("Plan not found. Run 'sdd-chat phase 3' first.")
        raise typer.Abort()
    
    typer.echo("  Steps:")
    print_step(1, "Run 'sdd-chat bundle 4' to generate the context bundle")
    print_step(2, "Copy the bundle into your LLM chat")
    print_step(3, "Ask the LLM to generate the task breakdown")
    print_step(4, f"Save the output to: {tasks_path}")
    
    typer.echo()
    print_info("Tasks should have exact file paths and clear dependencies.")
    print_info("Use [P] markers for tasks that can run in parallel.")
    
    if typer.confirm("  Generate context bundle now?"):
        bundle_content = _generate_bundle(4, project, feature)
        typer.echo()
        typer.secho("─" * 70, fg=typer.colors.CYAN)
        typer.echo(bundle_content)
        typer.secho("─" * 70, fg=typer.colors.CYAN)


def _guide_phase_5(project: str, feature: str):
    """Guide for Phase 5: Implementation."""
    feature_path = get_feature_path(project, feature)
    tasks_path = feature_path / "tasks.md"
    
    if not tasks_path.exists():
        print_error("Tasks not found. Run 'sdd-chat phase 4' first.")
        raise typer.Abort()
    
    typer.echo("  Steps:")
    print_step(1, "Identify the next task to implement from tasks.md")
    print_step(2, "Run 'sdd-chat bundle 5' to generate the base context bundle")
    print_step(3, "Add the specific task and any relevant existing code")
    print_step(4, "Ask the LLM to generate the implementation")
    print_step(5, "Save the code to your source repository")
    print_step(6, "Test the implementation")
    print_step(7, "Mark the task complete in tasks.md")
    print_step(8, "Repeat for each task")
    
    typer.echo()
    print_info("Implementation is iterative - do one task at a time.")
    print_info("For brownfield projects, include relevant existing code as context.")
    
    # Show tasks preview
    tasks_content = tasks_path.read_text()
    incomplete = []
    for line in tasks_content.split("\n"):
        if line.startswith("### T") or line.startswith("#### T"):
            incomplete.append(line.strip())
    
    if incomplete:
        typer.echo()
        typer.echo("  Tasks found:")
        for task in incomplete[:5]:
            typer.echo(f"    {task}")
        if len(incomplete) > 5:
            typer.echo(f"    ... and {len(incomplete) - 5} more")
    
    if typer.confirm("  Generate base context bundle now?"):
        bundle_content = _generate_bundle(5, project, feature)
        typer.echo()
        typer.secho("─" * 70, fg=typer.colors.CYAN)
        typer.echo(bundle_content)
        typer.secho("─" * 70, fg=typer.colors.CYAN)
        typer.echo()
        print_info("Add the specific task details and any existing code context to complete the bundle.")


def _generate_bundle(phase_number: int, project: str, feature: Optional[str]) -> str:
    """Generate the context bundle for a specific phase."""
    parts = []
    phase_info = PHASES[phase_number]
    
    parts.append(f"# SDD-Chat Context Bundle: Phase {phase_number} - {phase_info['name']}")
    parts.append(f"Project: {project}")
    if feature:
        parts.append(f"Feature: {feature}")
    parts.append(f"Generated: {datetime.now().isoformat()}")
    parts.append("")
    parts.append("---")
    parts.append("")
    
    # Add prompts
    for prompt_file in phase_info["prompts"]:
        prompt_path = PROMPTS_DIR / prompt_file
        if prompt_path.exists():
            parts.append(f"## PROMPT: {prompt_file}")
            parts.append("")
            parts.append(prompt_path.read_text())
            parts.append("")
            parts.append("---")
            parts.append("")
        else:
            parts.append(f"## PROMPT: {prompt_file}")
            parts.append("")
            parts.append(f"[File not found: {prompt_path}]")
            parts.append("[Create this file from the SDD-Chat guide]")
            parts.append("")
    
    # Add templates
    for template_file in phase_info["templates"]:
        template_path = TEMPLATES_DIR / template_file
        if template_path.exists():
            parts.append(f"## TEMPLATE: {template_file}")
            parts.append("")
            parts.append(template_path.read_text())
            parts.append("")
            parts.append("---")
            parts.append("")
        else:
            parts.append(f"## TEMPLATE: {template_file}")
            parts.append("")
            parts.append(f"[File not found: {template_path}]")
            parts.append("[Create this file from the SDD-Chat guide]")
            parts.append("")
    
    # Add existing artifacts based on phase
    project_path = get_project_path(project)
    
    # Constitution (needed for phases 1, 3, 4, 5)
    if phase_number in [1, 3, 4, 5]:
        const_path = project_path / "constitution.md"
        if const_path.exists():
            parts.append("## CONSTITUTION")
            parts.append("")
            parts.append(const_path.read_text())
            parts.append("")
            parts.append("---")
            parts.append("")
    
    if feature:
        feature_path = get_feature_path(project, feature)
        
        # Spec (needed for phases 2, 3, 4, 5)
        if phase_number in [2, 3, 4, 5]:
            spec_path = feature_path / "spec.md"
            if spec_path.exists():
                parts.append("## SPECIFICATION (spec.md)")
                parts.append("")
                parts.append(spec_path.read_text())
                parts.append("")
                parts.append("---")
                parts.append("")
        
        # Plan (needed for phases 4, 5)
        if phase_number in [4, 5]:
            plan_path = feature_path / "plan.md"
            if plan_path.exists():
                parts.append("## PLAN (plan.md)")
                parts.append("")
                parts.append(plan_path.read_text())
                parts.append("")
                parts.append("---")
                parts.append("")
            
            # Data model
            dm_path = feature_path / "data-model.md"
            if dm_path.exists():
                parts.append("## DATA MODEL (data-model.md)")
                parts.append("")
                parts.append(dm_path.read_text())
                parts.append("")
                parts.append("---")
                parts.append("")
            
            # Contracts
            contracts_path = feature_path / "contracts"
            if contracts_path.exists():
                for contract_file in contracts_path.iterdir():
                    parts.append(f"## CONTRACT: {contract_file.name}")
                    parts.append("")
                    parts.append(contract_file.read_text())
                    parts.append("")
                    parts.append("---")
                    parts.append("")
        
        # Tasks (needed for phase 5)
        if phase_number == 5:
            tasks_path = feature_path / "tasks.md"
            if tasks_path.exists():
                parts.append("## TASKS (tasks.md)")
                parts.append("")
                parts.append(tasks_path.read_text())
                parts.append("")
                parts.append("---")
                parts.append("")
    
    # Add instruction footer
    parts.append("## YOUR INPUT")
    parts.append("")
    
    if phase_number == 0:
        parts.append("[Add your specific project constraints here:]")
        parts.append("- Tech stack preferences")
        parts.append("- Testing requirements")
        parts.append("- Coding standards")
        parts.append("- Architectural patterns")
        parts.append("- Security/compliance requirements")
        parts.append("")
        parts.append("Then ask: 'Generate a complete constitution for this project.'")
    elif phase_number == 1:
        parts.append("[Add your feature description here - WHAT and WHY, no HOW:]")
        parts.append("")
        parts.append("Then ask: 'Generate a complete specification following the template.'")
    elif phase_number == 2:
        parts.append("Ask: 'Review this specification and identify any ambiguities or gaps that need clarification.'")
    elif phase_number == 3:
        parts.append("[Add your technical decisions here:]")
        parts.append("- Language/version:")
        parts.append("- Framework:")
        parts.append("- Database:")
        parts.append("- Testing approach:")
        parts.append("- Other dependencies:")
        parts.append("")
        parts.append("[For brownfield projects, also add:]")
        parts.append("- Project structure (tree output)")
        parts.append("- Relevant existing files")
        parts.append("")
        parts.append("Then ask: 'Generate plan.md, research.md, and data-model.md.'")
    elif phase_number == 4:
        parts.append("Ask: 'Generate an actionable task breakdown with dependency ordering.'")
    elif phase_number == 5:
        parts.append("[Add the specific task to implement here:]")
        parts.append("")
        parts.append("[Add any existing code context here:]")
        parts.append("")
        parts.append("Then ask: 'Generate the complete implementation for this task.'")
    
    return "\n".join(parts)


@app.command()
def setup():
    """
    Set up the sdd-chat directory structure with templates and prompts.
    
    Run this once to create the initial structure.
    """
    print_header("Setting Up SDD-Chat")
    
    # Create directories
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
    
    print_success(f"Created: {PROJECTS_DIR}")
    print_success(f"Created: {TEMPLATES_DIR}")
    print_success(f"Created: {PROMPTS_DIR}")
    
    typer.echo()
    print_info("Directory structure created.")
    print_info("Now copy the templates and prompts from the SDD-Chat guide:")
    typer.echo()
    typer.echo("  Templates to create:")
    typer.echo(f"    • {TEMPLATES_DIR}/constitution-template.md")
    typer.echo(f"    • {TEMPLATES_DIR}/spec-template.md")
    typer.echo(f"    • {TEMPLATES_DIR}/plan-template.md")
    typer.echo(f"    • {TEMPLATES_DIR}/tasks-template.md")
    typer.echo()
    typer.echo("  Prompts to create:")
    typer.echo(f"    • {PROMPTS_DIR}/constitution-prompt.md")
    typer.echo(f"    • {PROMPTS_DIR}/specify-prompt.md")
    typer.echo(f"    • {PROMPTS_DIR}/clarify-prompt.md")
    typer.echo(f"    • {PROMPTS_DIR}/plan-prompt.md")
    typer.echo(f"    • {PROMPTS_DIR}/tasks-prompt.md")
    typer.echo(f"    • {PROMPTS_DIR}/implement-prompt.md")


@app.command()
def complete(
    task_id: str = typer.Argument(..., help="Task ID to mark complete (e.g., T001)"),
    project: Optional[str] = typer.Option(None, "--project", "-p"),
    feature: Optional[str] = typer.Option(None, "--feature", "-f"),
):
    """
    Mark a task as complete in tasks.md.
    """
    state = load_state()
    project = project or state.get("current_project")
    feature = feature or state.get("current_feature")
    
    if not project or not feature:
        print_error("No project/feature selected.")
        raise typer.Abort()
    
    tasks_path = get_feature_path(project, feature) / "tasks.md"
    if not tasks_path.exists():
        print_error("tasks.md not found.")
        raise typer.Abort()
    
    content = tasks_path.read_text()
    
    # Update progress tracking table
    old_pattern = f"| {task_id} | ⬜ Not Started |"
    new_pattern = f"| {task_id} | ✅ Complete |"
    
    if old_pattern in content:
        content = content.replace(old_pattern, new_pattern)
        tasks_path.write_text(content)
        print_success(f"Marked {task_id} as complete.")
    else:
        print_warning(f"Could not find {task_id} in progress tracking table.")
        print_info("You may need to update tasks.md manually.")


@app.command()
def quickspec(
    description: str = typer.Argument(..., help="Feature description"),
    project: Optional[str] = typer.Option(None, "--project", "-p", help="Project name (uses current if not specified)"),
):
    """
    QuickSpec workflow: Lightweight spec-driven development for small features.

    This is a streamlined 3-phase workflow (spec → plan → build) for features
    that don't require the full 6-phase process. Best for features touching <5-7 files.
    """
    print_header("QuickSpec: Lightweight Spec-Driven Development")

    # Get current project
    state = load_state()
    project = project or state.get("current_project")

    if not project:
        print_error("No project specified. Run 'sdd-chat init <project>' or 'sdd-chat use <project>' first.")
        raise typer.Abort()

    project_path = get_project_path(project)
    if not project_path.exists():
        print_error(f"Project '{project}' does not exist. Run 'sdd-chat init {project}' first.")
        raise typer.Abort()

    # Setup
    feature_num = get_next_quickspec_number(project)
    slug = create_slug(description)
    feature_dir = f"{feature_num:03d}-{slug}"
    quickspec_dir = get_quickspec_dir(project)
    feature_path = quickspec_dir / feature_dir

    feature_path.mkdir(parents=True, exist_ok=True)
    print_success(f"Created: {feature_path}")

    # Update state
    state["current_quickspec"] = feature_dir
    state["current_project"] = project
    save_state(state)

    typer.echo()
    print_info(f"Feature: {feature_dir}")
    typer.echo()

    # Phase 1: Spec
    print_header("Phase 1: Spec")
    typer.echo("  Creating specification...")
    typer.echo()

    spec_content = f"""# {description.title()}

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
"""

    spec_path = feature_path / "spec.md"
    spec_path.write_text(spec_content)
    print_success(f"Created: {spec_path}")

    typer.echo()
    print_info("Please fill in the spec.md with your feature details.")
    print_info("Keep to 3-5 acceptance criteria max.")

    if not typer.confirm("\n  Ready to proceed to Phase 2 (Plan)?"):
        typer.echo()
        print_info(f"Paused. Edit {spec_path} and run 'sdd-chat quickspec {description}' again.")
        return

    # Phase 2: Plan
    typer.echo()
    print_header("Phase 2: Plan")
    typer.echo("  Scanning codebase and creating plan...")
    typer.echo()

    plan_content = """# Plan

## Files
- `path/to/file.py` — [change description]
- `path/to/new.py` — [create, purpose]

## Approach
[2-4 sentences on implementation strategy]

## Risks
- [potential issue, if any]
"""

    plan_path = feature_path / "plan.md"
    plan_path.write_text(plan_content)
    print_success(f"Created: {plan_path}")

    typer.echo()
    print_info(f"Please fill in {plan_path} with:")
    print_info("  - Concrete file paths")
    print_info("  - Implementation approach")
    print_info("  - Any risks or dependencies")

    if not typer.confirm("\n  Ready to proceed to Phase 3 (Build)?"):
        typer.echo()
        print_info(f"Paused. Edit {plan_path} and continue when ready.")
        return

    # Phase 3: Build
    typer.echo()
    print_header("Phase 3: Build")
    typer.echo("  Implementation phase:")
    typer.echo()
    print_step(1, "Follow the plan")
    print_step(2, "Respect existing code conventions")
    print_step(3, "Write tests if the project has them")
    print_step(4, f"Check off acceptance criteria in {spec_path}")
    print_step(5, "Run existing tests/linting and fix issues")

    typer.echo()
    print_info("Implement the feature according to your plan.")
    print_info(f"Update {spec_path} to check off acceptance criteria as you complete them.")


@app.command()
def quickspec_status(
    project: Optional[str] = typer.Option(None, "--project", "-p", help="Project name (uses current if not specified)"),
):
    """
    Show status of all quickspec features for a project.
    """
    print_header("QuickSpec Features")

    # Get current project
    state = load_state()
    project = project or state.get("current_project")

    if not project:
        print_error("No project specified. Run 'sdd-chat init <project>' or 'sdd-chat use <project>' first.")
        raise typer.Abort()

    typer.echo(f"  Project: {typer.style(project, fg=typer.colors.GREEN, bold=True)}")
    typer.echo()

    features = list_quickspec_features(project)

    if not features:
        print_warning("No quickspec features found for this project.")
        print_info("Run 'sdd-chat quickspec \"feature description\"' to start one.")
        return

    current = state.get("current_quickspec")
    quickspec_dir = get_quickspec_dir(project)

    for feature in features:
        feature_path = quickspec_dir / feature
        marker = " ◀ current" if feature == current else ""
        typer.secho(f"  {feature}{marker}", fg=typer.colors.GREEN, bold=True)

        # Check artifacts
        spec_path = feature_path / "spec.md"
        plan_path = feature_path / "plan.md"

        spec_status = "✓" if spec_path.exists() else "✗"
        plan_status = "✓" if plan_path.exists() else "✗"

        typer.echo(f"    spec.md: {spec_status}")
        typer.echo(f"    plan.md: {plan_status}")

        # Check if acceptance criteria are complete
        if spec_path.exists():
            spec_content = spec_path.read_text()
            total_criteria = spec_content.count("- [ ]") + spec_content.count("- [x]") + spec_content.count("- [X]")
            completed_criteria = spec_content.count("- [x]") + spec_content.count("- [X]")
            if total_criteria > 0:
                typer.echo(f"    Progress: {completed_criteria}/{total_criteria} criteria complete")

        typer.echo()


if __name__ == "__main__":
    app()
