# Implementation Plan: [FEATURE_NAME]

**Branch**: [NNN-feature-name]
**Date**: [DATE]
**Spec Reference**: [link to spec.md]

---

## Technical Context

### Stack

- **Language/Version**: [e.g., Python 3.11, TypeScript 5.0]
- **Primary Framework**: [e.g., FastAPI, Next.js]
- **Secondary Libraries**: [e.g., SQLAlchemy, Pydantic]
- **Storage**: [e.g., PostgreSQL 15, Redis]
- **Testing Framework**: [e.g., pytest, Jest]
- **Target Platform**: [e.g., Linux server, Docker, AWS Lambda]

### Performance Requirements

- [e.g., <200ms p95 response time]
- [e.g., Support 1000 concurrent users]
- [e.g., <100MB memory per instance]

### Constraints

- [e.g., Must integrate with existing auth service]
- [e.g., Cannot modify existing user table schema]
- [e.g., Must work offline]

---

## Source Structure

```
# Adjust based on project type

# Option 1: Single project
src/
├── models/
│   └── [feature models]
├── services/
│   └── [business logic]
├── api/
│   └── [endpoints/routes]
└── lib/
    └── [utilities/helpers]
tests/
├── unit/
├── integration/
└── e2e/

# Option 2: Web application (frontend + backend)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/
frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/
```

**Structure Decision**: [Which option and why]

---

## Implementation Phases

### Phase 0: Research & Validation

- [ ] Validate technology choices
- [ ] Investigate unknowns: [list specific questions]
- [ ] Prototype critical components if needed
- [ ] Document findings in research.md

### Phase 1: Foundation

- [ ] Data models and schemas
- [ ] Database migrations
- [ ] Core service interfaces
- [ ] Basic configuration

### Phase 2: Core Features (by User Story)

**US1: [Story Title]**
- Implementation approach: [brief description]
- Key components: [list]
- Integration points: [list]

**US2: [Story Title]**
- Implementation approach: [brief description]
- Key components: [list]
- Integration points: [list]

### Phase 3: Integration

- [ ] API endpoints / routes
- [ ] External service integrations
- [ ] Event handlers / webhooks

### Phase 4: Polish

- [ ] Error handling improvements
- [ ] Logging and monitoring
- [ ] Documentation
- [ ] Performance optimization

---

## Data Model Summary

*See data-model.md for complete details*

### Key Entities

| Entity | Key Fields | Purpose |
|--------|------------|---------|
| [Entity1] | id, name, ... | [purpose] |
| [Entity2] | id, entity1_id, ... | [purpose] |

### Relationships

- Entity1 → Entity2: [one-to-many / many-to-many / etc.]
- Entity2 → Entity3: [relationship]

---

## API Contracts Summary

*See contracts/ directory for complete specifications*

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/resource | Create new resource |
| GET | /api/resource/{id} | Get resource by ID |
| PUT | /api/resource/{id} | Update resource |
| DELETE | /api/resource/{id} | Delete resource |

---

## Testing Strategy

### Unit Tests

- [What to unit test]
- [Mocking strategy]

### Integration Tests

- [What to integration test]
- [Test data setup]

### E2E Tests

- [Critical user flows to test]

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | Low/Med/High | Low/Med/High | [Strategy] |
| [Risk 2] | Low/Med/High | Low/Med/High | [Strategy] |

---

## Open Technical Questions

- [Question 1]
- [Question 2]

---

## Constitution Compliance Checklist

- [ ] Follows Article I (Tech Stack)
- [ ] Follows Article II (Code Quality)
- [ ] Follows Article III (Testing)
- [ ] Follows Article IV (Architecture)
- [ ] Follows Article V (Security)
- [ ] Follows Article VI (Documentation)
- [ ] Follows Article VII (Error Handling)
- [ ] Follows Article VIII (Performance)
