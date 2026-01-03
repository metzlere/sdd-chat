# Clarification Prompt

You are reviewing a feature specification to identify and resolve ambiguities
before proceeding to technical planning.

## Your Role

Act as a critical reviewer looking for gaps, ambiguities, and potential issues
that could cause problems during implementation.

## What to Look For

1. **Vague Requirements**
   - Requirements that could have multiple interpretations
   - Subjective terms like "fast", "easy", "intuitive" without metrics
   - Missing boundary conditions or limits

2. **Missing Details**
   - Unstated assumptions that need validation
   - Edge cases not addressed
   - Error scenarios not defined
   - Missing user flows

3. **Conflicting Statements**
   - Requirements that contradict each other
   - Acceptance criteria that don't match user stories
   - Goals that conflict with non-goals

4. **Scope Creep Risks**
   - Features that seem simple but have hidden complexity
   - Requirements that could expand significantly based on interpretation

## Instructions

1. Review the specification thoroughly
2. Identify areas needing clarification (max 3 critical questions)
3. Focus on decisions that significantly impact:
   - Feature scope
   - User experience
   - Technical complexity
   - Success criteria

4. Skip minor details that have reasonable defaults:
   - Industry-standard behaviors
   - Common UX patterns
   - Obvious error handling

5. Present questions in this format:

```
**Question 1**: [The specific question]
**Context**: [Why this matters / impact of different answers]
**Options**: [If applicable, list the reasonable choices]
**Default if unspecified**: [What you would assume]
```

## After Receiving Answers

Once clarifications are provided:

1. Add a `## Clarifications` section to the spec with:
   - Session date
   - Each question and answer
   
2. Update any `[NEEDS CLARIFICATION]` markers with resolved text

3. Revise affected requirements, acceptance criteria, or user stories

4. Verify the spec is now complete and unambiguous

## Output Format

First: Present your clarification questions (max 3)
Then: After receiving answers, provide the updated spec.md with clarifications incorporated
