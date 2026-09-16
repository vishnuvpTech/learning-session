# Feature Branching Strategy
## Development Team Guidelines

**Document Purpose:** Define a standard Git workflow for development, code review, testing, and deployment.

---

## 1. Overview

The team will follow a **Feature Branching Git workflow** to isolate development work, maintain code quality, and ensure that changes are reviewed and tested before being merged into the main / default codebase.

Each feature, bug fix, improvement, or technical task should be developed in a separate branch and merged through a Pull Request (PR).

### Core principle

> **One task = One short-lived branch = One Pull Request**

The `main / default` branch should always contain stable and reviewed code.

---

# 2. Branch Structure

The primary branch will be:

```text
main / default
```

Development work should be performed using short-lived branches.

Recommended branch types:

```text
feature/*
bugfix/*
hotfix/*
refactor/*
chore/*
```

Example:

```text
main / default
 ├── feature/TICKET-101-user-login
 ├── feature/TICKET-102-customer-search
 ├── bugfix/TICKET-103-invalid-token
 ├── hotfix/TICKET-104-production-error
 ├── refactor/TICKET-105-user-service
 └── chore/TICKET-106-update-dependencies
```

---

# 3. Branch Types

| Branch | Purpose | Example |
|---|---|---|
| `feature/*` | New functionality | `feature/TA-101-resource-mapping` |
| `bugfix/*` | Fix for a normal development bug | `bugfix/TA-102-invalid-status` |
| `hotfix/*` | Urgent production fix | `hotfix/TA-103-login-failure` |
| `refactor/*` | Code restructuring without functional change | `refactor/TA-104-user-service` |
| `chore/*` | Maintenance/configuration/dependency work | `chore/TA-105-update-dependencies` |

---

# 4. Branch Naming Convention

Branch names should be:

- Short and meaningful
- Lowercase
- Associated with the ticket/task where possible
- Written using hyphens
- Easy to identify from the branch name

### Recommended format

```text
<type>/<ticket-id>-<short-description>
```

### Examples

```text
feature/TA-101-resource-mapping
feature/TI-205-call-recording
bugfix/TA-145-invalid-resource-status
hotfix/TI-301-call-api-error
refactor/TA-155-user-service
chore/TI-180-update-dependencies
```

### Avoid

```text
feature/my-work
feature/test
feature/new-feature
vishnu-branch
changes
temp
final
final-new
final-new-2
```

The branch name should provide enough information to understand the purpose of the work.

---

# 5. Standard Development Workflow

The standard workflow is:

```text
          main / default
               |
               ↓
       Create Feature Branch
               |
               ↓
          Development
               |
               ↓
       Local Quality Checks
               |
               ↓
          Push Branch
               |
               ↓
        Create Pull Request
               |
               ↓
      Automated CI/CD Checks
               |
               ↓
          Code Review
               |
               ↓
        Review Corrections
               |
               ↓
        Approval + CI Passed
               |
               ↓
        Merge to main / default
               |
               ↓
        Deploy / Release
```

---

# 6. Step 1 – Update Local main / default Branch

Before creating a new branch, always make sure the local `main / default` branch is up to date.

```bash
git checkout main
git pull origin main
```

Verify the current status:

```bash
git status
```

The working tree should be clean before creating a new branch.

---

# 7. Step 2 – Create a Feature Branch

Create the branch from the latest `main / default`.

```bash
git checkout -b feature/TA-101-resource-mapping
```

Or:

```bash
git switch -c feature/TA-101-resource-mapping
```

Confirm the branch:

```bash
git branch
```

---

# 8. Step 3 – Development

Develop only the assigned task in the branch.

For example:

```text
feature/TA-101-resource-mapping
```

should contain changes related to:

```text
Resource Mapping
```

Avoid combining unrelated tasks.

### Avoid

```text
feature/TA-101-resource-mapping

Changes:
- Resource mapping
- Login UI changes
- Database cleanup
- Unrelated bug fix
- Dependency upgrade
```

### Prefer

```text
feature/TA-101-resource-mapping

Changes:
- Resource mapping API
- Resource mapping validation
- Resource mapping tests
```

This makes the PR easier to review and reduces the risk of unintended changes.

---

# 9. Step 4 – Commit Guidelines

Commits should be meaningful and related to the task.

### Good

```bash
git commit -m "type(scope): short description"

git commit -m "feat(auth): add JWT authentication"
git commit -m "fix(api): resolve pagination bug"
git commit -m "refactor(db): optimize query performance"
git commit -m "docs(readme): update installation guide"
```

### Avoid

```bash
git commit -m "changes"
git commit -m "update"
git commit -m "fix"
git commit -m "test"
git commit -m "final changes"
```

Where possible, include the ticket ID.

Example:

```bash
git commit -m "TA-101 Add resource mapping API"
```
[Read More]([Best Practices/git-management.md](https://github.com/vishnuvpTech/learning-session/blob/main/Best%20Practices/git-management.md)
---

# 10. Step 5 – Local Quality Checks

Before pushing the branch, developers should perform the required local checks.

For Python projects, the recommended checks include:

```text
Ruff
Pylint
Bandit
Semgrep
Unit Tests
Integration Tests
```

Example:

```bash
ruff check .
pylint .
bandit -r .
pytest
```

Additional project-specific checks may be required.

The developer should fix issues locally before creating the PR.

---

# 11. Step 6 – Push the Branch

Push the feature branch to the remote repository.

```bash
git push -u origin feature/TA-101-resource-mapping
```

After pushing, create a Pull Request.

---

# 12. Pull Request Guidelines

Every feature or bug fix should be merged through a Pull Request.

### PR should contain

- Ticket/reference number
- Clear title
- Description of changes
- Implementation details
- Testing performed
- Screenshots/logs where applicable
- API changes, if applicable
- Database migration details, if applicable
- Configuration/environment changes, if applicable
- Known limitations or blockers

### Example PR title

```text
TA-101: Add resource mapping API
```

### PR description

```text
## Summary

Implemented resource mapping functionality.

## Changes

- Added resource mapping API
- Added mapping validation
- Added duplicate mapping validation
- Added database migration
- Added unit tests

## Testing

- Unit tests passed
- Ruff passed
- Pylint passed
- Bandit passed
- Semgrep passed

## Database Changes

- Added resource_mapping table
- Added required indexes

## Related Ticket

TA-101
```

---

# 13. Pull Request Size

PRs should be reasonably small and focused.

### Preferred

```text
1 feature
    ↓
1 branch
    ↓
1 PR
```

Avoid creating very large PRs containing multiple unrelated features.

Large PRs are difficult to:

- Review
- Test
- Debug
- Approve
- Roll back

If a feature is large, break it into smaller tasks where possible.

---

# 14. Code Review Process

At least one appropriate reviewer should review the PR before merging.

For critical architectural, security, database, or production-impacting changes, additional review may be required.

### Reviewer should check

#### Functionality

- Does the implementation satisfy the requirement?
- Are edge cases handled?
- Is error handling appropriate?

#### Code Quality

- Is the code readable?
- Is the implementation maintainable?
- Is there unnecessary duplication?
- Are appropriate design patterns being used?

#### API

- Request/response structure
- Validation
- Error responses
- Authentication/authorization
- Backward compatibility

#### Database

- Schema changes
- Indexes
- Migration correctness
- Query performance
- Transaction handling

#### Security

- Authentication
- Authorization
- Sensitive information
- SQL injection
- Input validation
- Secrets/configuration
- Dependency vulnerabilities

#### Testing

- Unit tests
- Integration tests
- Regression tests
- Edge cases

---

# 15. Automated CI Checks

Pull Requests should automatically execute the project's quality and security pipeline.

Recommended Python pipeline:

```text
Pull Request
     |
     ├── Ruff
     ├── Pylint
     ├── Bandit
     ├── Semgrep
     ├── CodeQL
     ├── Dependency Scan
     ├── Unit Tests
     ├── Integration Tests
     └── Build Validation
              |
              ↓
        Pass / Fail
```

A PR should not be merged if mandatory CI checks are failing.

---

# 16. Updating a Feature Branch

If the `main / default` branch changes while development is in progress, the feature branch should be synchronized regularly.

Example:

```bash
git checkout main
git pull origin main

git checkout feature/TA-101-resource-mapping
git merge main
```

Resolve conflicts if required, then run the required tests again.

Alternatively, if the team standardizes on rebase:

```bash
git checkout feature/TA-101-resource-mapping
git fetch origin
git rebase origin/main
```

### Team recommendation

Choose **one standard approach** for branch synchronization.

For a team using Pull Requests, either merge or rebase can work, but the team should document the selected convention and use it consistently.

---

# 17. Merge Strategy

After:

- Code review is completed
- Required approvals are received
- CI checks are passed
- Testing is completed

the PR can be merged.

### Recommended

For normal feature branches:

```text
Squash and Merge
```

Example:

```text
feature/TA-101
       |
       | 10 development commits
       ↓
     Squash
       ↓
  main / default
       |
       └── TA-101: Add resource mapping
```

This keeps the `main / default` branch history clean and easier to understand.

---

# 18. Branch Deletion

After a successful merge, the feature branch should be deleted.

Remote:

```bash
git push origin --delete feature/TA-101-resource-mapping
```

Local:

```bash
git branch -d feature/TA-101-resource-mapping
```

The team should avoid keeping unnecessary stale branches.

---

# 19. Bug Fix Workflow

Normal development bug:

```text
main / default
 |
 └── bugfix/TA-201-invalid-status
              |
              ↓
             PR
              |
              ↓
        main / default
```

Example:

```bash
git checkout main
git pull origin main

git checkout -b bugfix/TA-201-invalid-status
```

Fix the issue, test it, create a PR, review it, and merge.

---

# 20. Production Hotfix Workflow

For urgent production issues:

```text
main / default
 |
 └── hotfix/TI-301-call-failure
              |
              ↓
        Fix + Test
              |
              ↓
             PR
              |
              ↓
        main / default
              |
              ↓
         Production
```

Example:

```bash
git checkout main
git pull origin main

git checkout -b hotfix/TI-301-call-failure
```

Hotfixes should be:

- Small
- Focused
- Thoroughly tested
- Reviewed quickly
- Documented

---

# 21. Database Migration Guidelines

Database changes should always be included in the same feature branch where applicable.

Example:

```text
feature/TA-101-resource-mapping

Code changes
+
Migration
+
Tests
```

Developers should verify:

- Migration can be applied
- Migration is reversible where appropriate
- Existing data is not unintentionally affected
- Indexes/constraints are correct
- Migration works in a clean environment

For Django:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py test
```

For Alembic:

```bash
alembic revision --autogenerate -m "Add resource mapping"
alembic upgrade head
```

---

# 22. Dependency Changes

Dependency upgrades should not be mixed into unrelated feature branches unless required.

Prefer:

```text
chore/TA-250-upgrade-fastapi
```

instead of:

```text
feature/TA-101-resource-mapping
```

containing both:

```text
Resource mapping
+
FastAPI upgrade
+
Other dependency upgrades
```

This makes testing and rollback easier.

---

# 23. Configuration and Secrets

Never commit:

```text
.env
passwords
API keys
private keys
tokens
database credentials
cloud credentials
```

Use the approved secret-management mechanism for the project.

Example:

```text
Local       → .env / local secret configuration
Staging     → Secret Manager / CI secrets
Production  → Secret Manager / CI secrets
```

---

# 24. Emergency Changes

Emergency production changes should still follow the PR process wherever technically possible.

Avoid:

```text
Developer → Direct push → main / default → Production
```

Prefer:

```text
Developer
    ↓
hotfix/*
    ↓
PR
    ↓
Review
    ↓
CI
    ↓
main / default
    ↓
Production
```

If an emergency requires an exceptional process, the change should be reviewed and documented afterward.

---

# 25. What Should NOT Be Done

### ❌ Direct development on main / default

```bash
git checkout main
# Make changes
git commit
git push
```

Avoid this unless the team explicitly permits it for exceptional cases.

### ❌ Long-running branches

Avoid keeping a feature branch for several weeks.

### ❌ Mixing unrelated changes

```text
Feature
+
Bug fix
+
Refactoring
+
Dependency upgrade
```

### ❌ Force pushing shared branches

Avoid force pushing branches that other developers are actively using.

### ❌ Merging with failed CI

Do not merge when mandatory quality, security, or test checks are failing.

### ❌ Ignoring review comments

All mandatory review comments should be addressed before merging.

---

# 26. Recommended Branch Lifecycle

```text
Create
  ↓
Develop
  ↓
Local Testing
  ↓
Push
  ↓
Pull Request
  ↓
Automated CI
  ↓
Code Review
  ↓
Fix Review Comments
  ↓
CI Pass
  ↓
Approval
  ↓
Squash Merge
  ↓
Deploy
  ↓
Delete Branch
```

---

# 27. Responsibilities

## Developer

The developer is responsible for:

- Creating the correct branch
- Keeping the branch focused
- Following coding standards
- Running local tests
- Creating a clear PR
- Addressing review comments
- Ensuring CI passes
- Updating documentation where required

## Reviewer

The reviewer is responsible for:

- Reviewing functionality
- Reviewing code quality
- Checking security concerns
- Checking database/API impact
- Checking tests
- Identifying potential production issues
- Approving only when the implementation meets the required standard

## Technical Lead

The Technical Lead should review:

- Architecture changes
- Major database changes
- Security-sensitive changes
- API contract changes
- Infrastructure/deployment changes
- Performance-sensitive implementations
- Cross-service changes

---

# 28. Recommended Repository Rules

The repository should configure branch protection for `main / default`.

Recommended settings:

```text
✓ Pull Request required
✓ At least 1 reviewer approval
✓ Required CI checks
✓ No direct push
✓ No force push
✓ Branch must be up to date before merge
✓ Resolve review conversations
✓ Delete merged branches
```

For critical repositories, consider:

```text
✓ 2 approvals for critical changes
✓ CODEOWNERS
✓ Required security checks
✓ Required test coverage
✓ Signed commits where required
```

---

# 29. Example End-to-End Workflow

Developer receives:

```text
TA-101
Implement Resource Mapping API
```

### Step 1

```bash
git checkout main
git pull origin main
```

### Step 2

```bash
git checkout -b feature/TA-101-resource-mapping
```

### Step 3

Developer implements:

```text
API
Validation
Database changes
Tests
Documentation
```

### Step 4

Run local checks:

```bash
ruff check .
pylint .
bandit -r .
pytest
```

### Step 5

Push:

```bash
git push -u origin feature/TA-101-resource-mapping
```

### Step 6

Create PR:

```text
TA-101: Add resource mapping API
```

### Step 7

CI executes:

```text
Ruff
Pylint
Bandit
Semgrep
CodeQL
Tests
Build
```

### Step 8

Reviewer reviews the implementation.

### Step 9

Developer addresses review comments.

### Step 10

All checks pass.

### Step 11

Reviewer approves.

### Step 12

Squash merge:

```text
feature/TA-101-resource-mapping
                 ↓
            main / default
```

### Step 13

Delete the branch.

---

# 30. Team Golden Rules

The following rules should be followed by all developers:

1. **Do not develop directly on `main / default`.**
2. **Create a branch for every task.**
3. **Use the ticket ID in the branch name.**
4. **Keep branches short-lived.**
5. **Keep one logical task per branch.**
6. **Create a Pull Request for every change.**
7. **Run local tests and quality checks before creating the PR.**
8. **Do not merge with mandatory CI failures.**
9. **Address all mandatory review comments.**
10. **Keep `main / default` stable and deployable.**
11. **Delete merged branches.**
12. **Never commit credentials, secrets, or sensitive configuration.**
13. **Use feature flags when a feature needs to be merged before it is ready for release.**
14. **Ask for Technical Lead review for architecture, security, database, or major API changes.**

---

# 31. Recommended Team Standard

The team's recommended Git strategy is:

```text
                 ┌── feature/TICKET-ID ──┐
                 │                        │
                 │     Development        │
                 │                        │
main / default ──●────────────────────────●──────── main / default
                 │                        │
                 │                    Pull Request
                 │                        │
                 │                    Code Review
                 │                        │
                 │                     CI/CD
                 │                        │
                 └────────────────────────┘
                                          │
                                          ↓
                                      Staging
                                          │
                                          ↓
                                     Production
```

### Standard

**Branch Strategy:** Feature Branching  
**Primary Branch:** `main / default`  
**Integration:** Pull Request  
**Review:** Mandatory  
**CI:** Mandatory  
**Merge:** Squash Merge  
**Branch Lifetime:** Short-lived  
**Release:** CI/CD driven  
**Production Fix:** `hotfix/*`  
**Feature Control:** Feature flags where required

---

# 32. Conclusion

Feature Branching provides a simple and controlled development process without the complexity of GitFlow.

The objective is to maintain a stable `main / default` branch while allowing developers to work independently and safely.

The expected development culture is:

```text
Small Change
    ↓
Short-Lived Branch
    ↓
Good Commits
    ↓
Automated Checks
    ↓
Code Review
    ↓
Squash Merge
    ↓
Stable main
    ↓
Continuous Delivery
```

Following this process consistently will improve:

- Code quality
- Collaboration
- Review effectiveness
- Release confidence
- Security
- Traceability
- Deployment reliability
- Overall development velocity
