> **Author:** [Vishnu VP](https://github.com/vishnuvpTech) · [vishnu.vp@techversantinfotech.com](mailto:vishnu.vp@techversantinfotech.com)

# Developer Prompting — Complete Practical Guide

A comprehensive reference for writing effective prompts when working with AI coding assistants.

---

## 1. The Basic Principle

A good developer prompt should answer these questions:

- **What do I have?** → Current context, code, error
- **What do I want?** → The desired outcome
- **What constraints exist?** → Boundaries and limitations
- **How should you do it?** → Approach and methodology
- **What should the result look like?** → Acceptance criteria

### Useful Structure

```
ROLE
CONTEXT
TASK
REQUIREMENTS
CONSTRAINTS
TECHNICAL DETAILS
EXPECTED OUTPUT
VALIDATION / DEFINITION OF DONE
```

### Example — Before and After

**Bad:**
> Fix this Python code.

**Good:**
> You are a senior Python developer.
>
> Context: This is a FastAPI service using SQLAlchemy and PostgreSQL. The existing API is working in production.
>
> Task: Fix the performance issue in the provided function.
>
> Requirements:
> - Preserve existing API behavior.
> - Do not change the database schema.
> - Do not introduce new dependencies.
> - Keep the existing function signature.
> - Handle empty and null inputs correctly.
>
> Constraints:
> - Modify only the required code.
> - Do not add tests unless requested.
> - Do not modify documentation.
> - Do not refactor unrelated code.
>
> Expected output:
> 1. Identify the root cause.
> 2. Explain the required change briefly.
> 3. Provide the corrected code.
> 4. List exactly what was changed.
>
> Definition of done:
> - Existing behavior is preserved.
> - The performance issue is addressed.
> - No unrelated files are modified.

The second prompt gives the AI a clear working boundary.

---

## 2. The Most Important Prompting Rule

**Don't ask AI to "do everything"**

**Bad:**
> Review this project and fix all issues.

This gives the AI too much freedom.

**Better:**
> Review the provided Python module only.
>
> Focus on:
> - Security vulnerabilities
> - Pylint issues
> - Performance problems
> - Incorrect exception handling
>
> Do not:
> - Change business logic unless required
> - Add new dependencies
> - Modify tests
> - Modify documentation
> - Refactor unrelated code
>
> For each issue:
> - Identify the problem
> - Explain why it is a problem
> - Provide the minimal required fix

### Principle

**Narrow scope → better result → fewer unintended changes.**

---

## 3. Context Is More Important Than Prompt Length

AI needs enough information to understand the problem. Provide project context like:

```
Project: Recruitment ERP
Backend: Python 3.12, Django 5.x, Django REST Framework, PostgreSQL
Architecture: Modular monolith
Authentication: JWT
Deployment: Docker + AWS ECS
Coding standard: PEP 8, Pylint, Black
```

You don't need to repeat this every time if your AI tool already has project instructions configured.

---

## 4. Use the "Task + Boundary" Pattern

One of the best patterns for coding tasks:

```
TASK: Fix the database query causing slow API response.

BOUNDARY:
- Do not change API response format.
- Do not change models.
- Do not change migrations.
- Do not change business logic.
- Do not add packages.
- Do not modify unrelated queries.
```

This is especially useful when using Claude Code, Cursor, Copilot, or other coding agents.

---

## 5. Define the Expected Behavior

Never assume the AI understands what "correct" means.

**Bad:**
> Fix pricing calculation.

**Good:**
> Expected behavior:
> 1. Apply eligible promotions.
> 2. If promotions are exclusive, select the highest percentage discount.
> 3. Apply the discount before tax.
> 4. Apply the configured cap after discount calculation.
> 5. Calculate tax on the final taxable amount.
> 6. Preserve the existing rounding rules.

This removes ambiguity.

---

## 6. Tell AI What NOT to Do

Use explicit negative constraints:

```
Do NOT:
- Add unnecessary abstraction.
- Rename existing public methods.
- Change API contracts.
- Add dependencies.
- Modify database schema.
- Add tests.
- Update documentation.
- Change configuration files.
- Refactor unrelated code.
```

This is particularly important when asking an AI coding agent to modify an existing repository.

---

## 7. Use "Minimal Change" When Fixing Existing Code

For production code, use:

```
Make the smallest possible change required to fix the issue.

Preserve:
- Existing architecture
- Existing interfaces
- Existing business logic
- Existing API responses
- Existing naming conventions

Do not perform unrelated refactoring.
```

This prevents AI over-engineering.

---

## 8. Separate Analysis from Implementation

For complex problems, don't immediately ask AI to modify code.

**Phase 1 — Analyze:**
```
Analyze the issue only. Do not modify any files.

Identify:
1. Root cause
2. Affected components
3. Why the issue occurs
4. Possible solutions
5. Recommended solution
6. Potential side effects

Wait for implementation instructions.
```

**Phase 2 — Implement:**
```
Implement only the recommended solution.
Follow the previously defined constraints.
```

This gives you much more control.

---

## 9. Use Phased Prompting for Large Tasks

Break large tasks into phases:

```
Phase 1 → Understand
Phase 2 → Analyze
Phase 3 → Plan
Phase 4 → Implement
Phase 5 → Validate
Phase 6 → Review
```

### Example

```
Phase 1: Understand the existing authentication flow.

Phase 2: Identify security weaknesses.

Phase 3: Create a minimal implementation plan.
         Do not modify files yet.

Phase 4: Implement the approved plan only.

Phase 5: Review the implementation against the requirements.
         Do not modify code.
         Report: Passed / Failed / Remaining risks
```

---

## 10. Give AI a Definition of Done

One of the most powerful techniques.

**Bad:**
> Implement user authentication.

**Good:**
> Definition of Done:
> - User can log in using email and password.
> - Passwords are never stored in plain text.
> - Access token is generated successfully.
> - Refresh token is supported.
> - Invalid credentials return HTTP 401.
> - Expired tokens are rejected.
> - Protected endpoints require authentication.
> - Existing APIs continue to work.
> - No secrets are hardcoded.
> - Pylint issues introduced by the change are resolved.

Now AI has a measurable target.

---

## 11. Prompt for Debugging Correctly

**Bad:**
> Why is this API failing?

**Good:**
> You are debugging a production FastAPI application.
>
> Problem: POST /api/orders occasionally returns HTTP 500.
>
> Observed error:
> ```
> <error>
> ```
>
> Expected behavior: The order should be created successfully.
>
> Environment:
> - Python 3.12
> - FastAPI
> - SQLAlchemy
> - PostgreSQL
> - Docker
>
> Investigate:
> 1. Root cause
> 2. Exact execution path
> 3. Why the error occurs
> 4. Whether it is deterministic or intermittent
> 5. Minimal fix
>
> Constraints:
> - Do not change API contract.
> - Do not change database schema.
> - Do not add dependencies.
> - Do not modify unrelated code.
>
> First analyze the issue. Do not modify files yet.

---

## 12. Give Error Messages Exactly

Don't paraphrase errors.

**Bad:**
> Database connection is failing.

**Good:**
> Error:
> ```
> sqlalchemy.exc.OperationalError:
> (psycopg2.OperationalError)
> could not connect to server:
> Connection timed out
> ```
>
> Also provide:
> - **When:** After establishing VPN
> - **Works:** VPN connection
> - **Fails:** Application server → Database server
> - **Expected:** Database connection should succeed
> - **Observed:** Connection timeout

This dramatically improves troubleshooting.

---

## 13. Prompt for Code Review

> You are a senior Python code reviewer.
>
> Review the provided code for:
> 1. Security
> 2. Correctness
> 3. Performance
> 4. Maintainability
> 5. Error handling
> 6. Database usage
> 7. Concurrency
> 8. Logging
> 9. Python best practices
> 10. PEP 8
> 11. Pylint
> 12. Type safety
>
> For every issue provide:
> - Severity: Critical / High / Medium / Low
> - File
> - Line/function
> - Problem
> - Why it matters
> - Recommended fix
>
> Do not modify the code. Do not report purely stylistic issues unless they affect maintainability.

---

## 14. Security Review Prompt

> Perform a security review of the provided Python application.
>
> Check specifically for:
> - Authentication weaknesses
> - Authorization / RBAC issues
> - Broken access control
> - SQL injection
> - Command injection
> - SSRF
> - XSS
> - CSRF
> - Path traversal
> - Unsafe deserialization
> - Sensitive data exposure
> - Hardcoded secrets
> - Insecure logging
> - Weak cryptography
> - Insecure file handling
> - Dependency risks
> - Missing input validation
> - Improper error handling
> - Session/token issues
> - Database security
> - API security
>
> For each finding provide:
> - Severity
> - CWE category if applicable
> - Location
> - Attack scenario
> - Impact
> - Recommended remediation
>
> Do not modify code.

---

## 15. Performance Prompting

Don't simply ask: "Optimize this code." Instead specify what performance means.

> Analyze this function for performance problems.
>
> Focus on:
> - Time complexity
> - Space complexity
> - Database queries
> - N+1 queries
> - Unnecessary loops
> - Duplicate calculations
> - Network calls
> - Serialization
> - Memory usage
> - Caching opportunities
>
> Current behavior: The endpoint processes approximately 100,000 records.
> Problem: Response takes approximately 8–12 seconds.
> Target: Response should ideally be below 2 seconds.
>
> Constraints:
> - Preserve output format.
> - Do not change business logic.
> - Do not introduce new infrastructure.
>
> Recommend the optimization before implementing it.

---

## 16. Database Prompting

For SQL/database work, provide:

> Database: PostgreSQL 16
> Table: orders
> Approximate rows: 10 million
>
> Query:
> ```
> <query>
> ```
>
> Problem: Query takes 4–8 seconds.
> Expected: <expected result>
>
> Review:
> - Query plan
> - Index usage
> - Sequential scans
> - Joins
> - Filtering
> - Sorting
> - Aggregation
> - Cardinality
> - Locking
>
> Provide:
> 1. Root cause
> 2. EXPLAIN/EXPLAIN ANALYZE interpretation
> 3. Recommended index/query change
> 4. Expected performance impact

---

## 17. API Development Prompting

Define the contract clearly.

> Implement: POST /api/interviews/schedule
>
> Request body:
> ```json
> {
>     "candidate_id": 123,
>     "interview_date": "2026-08-20",
>     "interview_link": "...",
>     "comments": "..."
> }
> ```
>
> Optional fields: `interview_link`, `comments`
> Required fields: `candidate_id`, `interview_date`
>
> Expected responses:
> - `201` — Interview scheduled successfully.
> - `400` — Invalid request.
> - `404` — Candidate not found.
> - `401` — Authentication required.
>
> Constraints:
> - Follow existing project patterns.
> - Use existing authentication.
> - Use existing serializer/schema conventions.
> - Do not introduce a new architecture.

---

## 18. Prompt for React Development

> You are a senior React developer.
>
> Context:
> - React
> - TypeScript
> - TanStack Query
> - Tailwind CSS
>
> Task: Implement the interview scheduling form.
>
> Fields:
> - Candidate (required)
> - Interview date (required)
> - Comments (optional)
> - Interview link (optional)
>
> Requirements:
> - Candidate and date are required.
> - Comments and interview link are optional.
> - Show validation errors.
> - Disable submit while saving.
> - Display API errors.
> - Refresh interview list after successful creation.
>
> Constraints:
> - Use existing components.
> - Use existing API hooks.
> - Do not introduce Redux.
> - Do not add dependencies.
> - Follow existing UI patterns.

---

## 19. Architecture Prompting

Provide constraints first.

> Act as a senior software architect.
>
> Design an architecture for:
> <system description>
>
> Expected scale:
> - 1 million users
> - 100,000 daily active users
> - 1,000 requests/sec peak
>
> Requirements:
> - High availability
> - Horizontal scalability
> - Secure authentication
> - Audit logging
> - Async processing
> - Monitoring
> - Disaster recovery
>
> Current stack:
> - FastAPI
> - PostgreSQL
> - Redis
> - AWS
> - Docker
>
> Evaluate:
> 1. Architecture
> 2. Service boundaries
> 3. Database design
> 4. Caching
> 5. Async processing
> 6. Scaling
> 7. Failure handling
> 8. Security
> 9. Observability
> 10. Cost
>
> Provide alternatives and explain trade-offs.

---

## 20. Don't Mix Multiple Objectives Unnecessarily

**Bad:**
> Fix the bug, refactor the code, improve performance, add tests, update documentation, change the architecture, and improve security.

This creates too many objectives.

**Better — Split into separate prompts:**

> Prompt 1: Fix the bug only.
> Prompt 2: Now review the changed code for performance.
> Prompt 3: Now review the changed code for security.
> Prompt 4: Now add tests for the modified behavior.

This makes AI output much more predictable.

---

## 21. Use Priority Levels

For complicated requirements:

```
Priority:
P0 - Must not break existing behavior
P1 - Fix the reported issue
P2 - Improve performance
P3 - Improve maintainability
P4 - Optional improvements
```

Then tell AI:

> Do not implement P3/P4 improvements unless they are required for P1.

This prevents unnecessary refactoring.

---

## 22. Tell AI How to Handle Ambiguity

Extremely useful for production code:

> If requirements conflict:
> 1. Identify the conflict.
> 2. Do not guess.
> 3. Explain the two interpretations.
> 4. Recommend the safer interpretation.
> 5. Ask for clarification before making a business-logic change.
>
> For example: If existing documentation conflicts with the current business requirement, do not silently choose one. Report the conflict first.

---

## 23. Tell AI What Sources of Truth to Use

In real projects, requirements can conflict. Define precedence:

```
Source-of-truth priority:
1. Explicit current user requirement
2. Approved technical specification
3. Existing tests
4. Existing implementation
5. Documentation
6. AI assumptions
```

Or for your project:

> When requirements conflict, do not make assumptions. Identify the conflict and ask for clarification.

This is safer.

---

## 24. Repository-Aware Prompting

When using Claude Code / Cursor / etc., ask AI to inspect the repository first.

```
Before making any changes:
1. Inspect the repository structure.
2. Identify the relevant module.
3. Find related models/services/views.
4. Trace the existing implementation.
5. Identify existing patterns.
6. Determine the smallest set of files that need modification.

Do not modify anything during this analysis phase.
```

This prevents the AI from immediately creating new files unnecessarily.

---

## 25. Prevent Unnecessary Files

A very useful constraint:

```
Before creating a new file:
- Check whether an existing file already handles this responsibility.
- Reuse the existing architecture if possible.
- Do not create a new service/module/helper unless necessary.
```

---

## 26. Prevent Dependency Bloat

```
Do not add a new dependency unless the requirement cannot reasonably be implemented using the existing dependencies.

If a new dependency is necessary:
- Explain why.
- Mention alternatives.
- Identify security/maintenance implications.
```

---

## 27. Prompt for Tests

Don't just say: "Write tests." Define scenarios.

> Create tests for the modified pricing logic.
>
> Cover:
> 1. Normal pricing
> 2. No promotion
> 3. Percentage promotion
> 4. Fixed promotion
> 5. Exclusive promotions
> 6. Promotion cap
> 7. Tax
> 8. Multiple promotions
> 9. Boundary values
> 10. Invalid input
>
> Do not modify production behavior just to make tests pass.

---

## 28. Ask AI to Verify Its Own Work

After implementation:

> Review your implementation against the original requirements.
>
> Create a checklist:
>
> | Requirement | Status | Evidence |
> |-------------|--------|----------|
>
> Do not make additional changes.
>
> Identify:
> - Missing requirements
> - Potential regressions
> - Unhandled edge cases
> - Unnecessary changes

This is better than simply asking: "Is it correct?"

---

## 29. Use a "Diff Discipline" Prompt

Very useful for existing projects:

> Before finishing:
> Review the final diff.
>
> Report:
> 1. Files modified
> 2. Files added
> 3. Files deleted
> 4. Business logic changed
> 5. API behavior changed
> 6. Database changes
> 7. Dependencies changed
> 8. Configuration changes
>
> Flag anything that was not explicitly required.

---

## 30. Use a "Do Not Assume" Rule

Add this to important prompts:

> Do not assume missing requirements.
>
> If the implementation depends on an unknown business rule, identify the missing information instead of inventing behavior.

This is especially important for:
- Pricing
- HR systems
- Financial calculations
- Permissions
- Recruitment workflows
- Tax
- Scheduling
- Approval workflows

---

## 31. Prompting for Production Fixes

For production issues, use a stricter format:

> This is a production issue.
>
> Rules:
> - Preserve backward compatibility.
> - Make the smallest safe change.
> - Do not refactor unrelated code.
> - Do not change database schema unless absolutely required.
> - Do not change API contracts.
> - Do not introduce dependencies.
> - Consider rollback impact.
> - Consider concurrency.
> - Consider existing production data.
>
> Before implementation: Identify the root cause and proposed fix.
> After implementation: Explain the exact production impact.

---

## 32. Prompting for Refactoring

Refactoring needs different rules from bug fixing.

> Refactor this module for maintainability.
>
> Goals:
> - Reduce duplication.
> - Improve readability.
> - Improve separation of concerns.
>
> Must preserve:
> - Public APIs
> - Existing behavior
> - Database behavior
> - Error behavior
>
> Do not:
> - Change business rules.
> - Introduce new dependencies.
> - Change architecture.
> - Modify unrelated modules.
>
> First identify the refactoring opportunities. Then implement only the approved changes.

---

## 33. Prompting for Code Modernization

> Modernize this Python module for Python 3.12.
>
> Review:
> - Deprecated APIs
> - Type hints
> - Exception handling
> - Modern Python syntax
> - Resource management
> - Standard library improvements
>
> Constraints:
> - Preserve behavior.
> - Do not change public APIs.
> - Do not add third-party dependencies.
> - Do not perform unrelated refactoring.

---

## 34. Prompting for Documentation

> Create documentation for this API.
>
> Include:
> 1. Purpose
> 2. Authentication
> 3. Endpoint
> 4. Request parameters
> 5. Request examples
> 6. Response examples
> 7. Error responses
> 8. Validation rules
> 9. Business rules
> 10. Known limitations
>
> Use information from the existing implementation. Do not invent behavior that is not present in the code.

---

## 35. Prompting for Jira Tasks

> Convert the following technical requirement into a Jira development task.
>
> Include:
> - Title
> - Description
> - Business context
> - Technical requirements
> - Acceptance criteria
> - Dependencies
> - Edge cases
> - Definition of done
>
> Keep the task implementation-focused and avoid unnecessary technical assumptions.

---

## 36. Prompting for Client-Facing Technical Improvements

Use improvement language instead of blame language:

**Bad:**
> Fix bugs.

**Good:**
> Enhance the existing validation and error-handling mechanism to improve system reliability and provide clearer feedback for invalid requests.
>
> Scope:
> - Improve input validation.
> - Improve API error responses.
> - Handle unexpected exceptions safely.
> - Preserve existing successful workflows.
>
> Expected outcome:
> More consistent API behavior and improved troubleshooting visibility.

This is useful when presenting technical work to clients.

---

## 37. A Powerful Universal Developer Prompt

You can use this as your base template:

```
You are a senior software engineer working on an existing production codebase.

## Context
Project: <project>
Technology: <technology>
Relevant module: <module>
Current behavior: <current behavior>
Problem / Requirement: <requirement>

## Task
<exact task>

## Requirements
- <requirement 1>
- <requirement 2>
- <requirement 3>

## Constraints
- Preserve existing behavior unless explicitly required.
- Do not modify unrelated code.
- Do not add dependencies unless necessary.
- Do not change public APIs unless explicitly required.
- Do not change database schema unless explicitly required.
- Follow existing project architecture and coding patterns.
- Reuse existing utilities/components where possible.
- Do not create unnecessary files.

## Implementation Rules
Before changing code:
1. Inspect the relevant implementation.
2. Identify the root cause or existing pattern.
3. Determine the minimum required changes.
4. Identify potential side effects.

Then implement the change.

## Validation
Verify:
- Functional correctness
- Error handling
- Security
- Performance
- Backward compatibility
- Code quality

## Final Response
Provide:
1. Summary
2. Root cause
3. Files changed
4. Changes made
5. Validation performed
6. Potential risks
7. Remaining issues

Do not make changes outside the requested scope.
```

---

## 38. A Better Prompt Specifically for AI Coding Agents

For tools such as Cursor / Claude Code, use this workflow:

```
You are working inside an existing repository.

RULES:
1. Inspect before modifying.
2. Understand existing architecture before creating new code.
3. Reuse existing patterns.
4. Make minimal changes.
5. Do not modify unrelated files.
6. Do not invent requirements.
7. Do not add dependencies without justification.
8. Do not change public interfaces unless required.
9. Do not silently change business logic.
10. Review the final diff before completing.

WORKFLOW:
Step 1: Analyze the requirement.
Step 2: Inspect the relevant code.
Step 3: Identify the root cause / implementation approach.
Step 4: List the files that need modification.
Step 5: Implement the minimum required changes.
Step 6: Review the diff.
Step 7: Validate against the requirements.
Step 8: Report the result.

If requirements are ambiguous or conflicting, stop and ask for clarification rather than guessing.
```

This is a good global instruction for your development workflow.

---

## 39. Prompt Quality Levels

| Level | Description | Example |
|-------|-------------|---------|
| **Level 1 — Basic** | Bare instruction | "Fix this bug." |
| **Level 2 — Context** | Adds environment | "Fix this bug in our FastAPI application using PostgreSQL." |
| **Level 3 — Constraints** | Adds boundaries | "Fix this bug in our FastAPI application. Do not change the API contract or database schema." |
| **Level 4 — Engineering-grade** | Adds full context + behavior + constraints + DoD | Includes current/expected behavior, constraints, and definition of done. |
| **Level 5 — Agent-grade** | Adds structured workflow | Analyze → inspect → plan → implement → validate → review diff. Stop when requirements are ambiguous. |

For professional development, aim for **Level 4–5**.

---

## 40. Common Prompting Mistakes

| Mistake | Problem | Better Approach |
|---------|---------|-----------------|
| "Fix everything" | Scope explosion | Define exact issue |
| Huge prompt | Important requirements get lost | Structured sections |
| No context | AI guesses | Provide architecture/context |
| No constraints | Unwanted changes | Define boundaries |
| No expected behavior | AI decides behavior | Define acceptance criteria |
| No error details | Poor debugging | Give exact error |
| Ask for implementation immediately | Wrong architecture | Analyze first |
| "Improve code" | Subjective | Define improvement criteria |
| No definition of done | Incomplete implementation | Add measurable criteria |
| Allow unlimited refactoring | Large risky diff | Minimal-change rule |
| No source of truth | Conflicting behavior | Define precedence |
| Multiple unrelated tasks | Confused output | Split into phases |
| No validation | Hidden regressions | Require verification |

---

## 41. The 10 Questions to Ask Before Writing a Developer Prompt

Before sending a complex coding request, ask yourself:

1. What exactly needs to change?
2. Why does it need to change?
3. What is the current behavior?
4. What should the new behavior be?
5. Which files/modules are involved?
6. What must not change?
7. Are there business rules involved?
8. What edge cases matter?
9. How will we know it is correct?
10. What should AI return after completing the task?

If you can answer these, your prompt will usually be significantly better.

---

## 42. Recommended Prompt Structure for Your Development Team

Standardize prompts around this format:

```
# ROLE
Who should the AI act as?

# CONTEXT
What project/system is this?

# PROBLEM
What is currently wrong?

# TASK
What exactly needs to be done?

# REQUIREMENTS
What must the solution satisfy?

# BUSINESS RULES
What rules must be preserved?

# CONSTRAINTS
What must not be changed?

# TECHNICAL CONTEXT
Framework, database, versions, architecture, etc.

# EDGE CASES
What unusual situations must work?

# VALIDATION
How should correctness be verified?

# DEFINITION OF DONE
What conditions mean the task is complete?

# OUTPUT
What should the AI report?
```

---

## 43. My Recommended "Developer AI Prompt Standard"

For your type of work, make this the team standard:

```
ROLE
Act as a senior software engineer familiar with the project's existing architecture and coding standards.

CONTEXT
<project / module / technology / relevant architecture>

TASK
<one clearly defined task>

CURRENT BEHAVIOR
<what happens now>

EXPECTED BEHAVIOR
<what should happen>

REQUIREMENTS
- <requirement>
- <requirement>
- <requirement>

BUSINESS RULES
- <rule>
- <rule>

CONSTRAINTS
- Preserve existing behavior outside this task.
- Do not modify unrelated code.
- Do not add dependencies unless necessary.
- Do not change APIs unless explicitly required.
- Do not change database schema unless explicitly required.
- Reuse existing project patterns.
- Avoid unnecessary refactoring.

EDGE CASES
- <case>
- <case>

WORKFLOW
1. Inspect the existing implementation.
2. Identify the root cause / approach.
3. Determine the minimum required changes.
4. Implement the changes.
5. Review the final diff.
6. Validate against the requirements.

DEFINITION OF DONE
- <measurable condition>
- <measurable condition>
- <measurable condition>

FINAL RESPONSE
Provide:
- Summary
- Root cause
- Files changed
- Changes made
- Validation
- Risks / limitations

If requirements are ambiguous or conflicting, do not guess. Explain the conflict and request clarification.
```

---

## Key Takeaway

The biggest improvement in developer prompting comes from moving from:

> *"Tell AI what to code."*

to:

> *"Give AI the engineering context, desired behavior, constraints, boundaries, validation criteria, and definition of done."*

For production development, the most important rules are:

**Context + Exact Task + Constraints + Business Rules + Expected Behavior + Validation + Definition of Done.**

---

*Last updated: 2026-08-13*
