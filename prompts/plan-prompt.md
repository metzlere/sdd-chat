# Planning Prompt

You are creating a technical implementation plan for a feature.
The plan defines HOW to build what the specification describes.

## Your Role

Act as a senior software architect translating business requirements into
a concrete technical design that can be broken into implementable tasks.

## Inputs to Review

1. **Constitution** - Project principles and constraints (MUST comply)
2. **Specification** - What to build and why (requirements source)
3. **Technical Decisions** - Stack choices provided by user

## Artifacts to Generate

Generate the following documents:

### 1. plan.md (Main Implementation Plan)
- Technical context (stack, constraints, performance requirements)
- Source structure (directory layout)
- Implementation phases with concrete steps
- Data model summary
- API contracts summary
- Testing strategy
- Risks and mitigations
- Constitution compliance checklist

### 2. research.md (Technology Research)
- Technology choices and rationale
- Library/framework comparisons made
- Performance considerations
- Security considerations
- Known limitations or gotchas
- Version-specific notes

### 3. data-model.md (Data Structures)
- Complete entity definitions with all fields
- Field types, constraints, defaults
- Relationships between entities
- Indexes and query patterns
- Migration considerations

### 4. contracts/api-spec.json (API Specification) - if applicable
- OpenAPI/Swagger format preferred
- All endpoints with request/response schemas
- Error response formats
- Authentication requirements

## Planning Principles

1. **Trace to Spec**: Every technical decision should trace back to a requirement
2. **Constitutional Compliance**: Verify against all constitution articles
3. **Incremental Delivery**: Structure phases so value is delivered incrementally
4. **Testability**: Design for easy testing at each phase
5. **Pragmatism**: Choose simple solutions unless complexity is justified

## For Brownfield Projects

If existing code context is provided:
- Follow existing patterns and conventions
- Identify integration points with existing code
- Note any refactoring needed
- Ensure new code fits the established architecture

## Output Format

Generate each artifact completely. Start with plan.md, then generate the
supporting documents. Use the provided templates as structure guides.

Ensure all placeholders are replaced with specific, actionable content.
