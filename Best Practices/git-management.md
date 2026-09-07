# Git Management Best Practices

Team Git standards for branching, commits, code review, and repository hygiene.

---

## 1. Branching Strategy

We use a three-tier integration model with short-lived supporting branches.

| Branch | Purpose |
|---|---|
| `production` | Live, production-ready code deployed to the production environment |
| `uat` | User Acceptance Testing — final validation before production release |
| `develop` | Integration branch for ongoing development and QA testing |
| `feature/*` | New feature development |
| `bugfix/*` | Fixes for bugs found during development or testing |
| `hotfix/*` | Urgent production fixes requiring immediate deployment |

**Naming examples:**
```
feature/user-authentication
bugfix/login-error
hotfix/payment-failure
```

### PR Flow

```
feature/*  →  develop  →  uat  →  production
bugfix/*   →  develop  →  uat  →  production
hotfix/*   →  production  →  uat  and  develop   (backport after urgent fix)
```

Rules:
- `production` → always deployable, always stable.
- `uat` → mirrors what's about to ship; used for stakeholder/QA sign-off.
- `develop` → where feature and bugfix branches integrate first.
- `hotfix/*` branches off `production`, gets merged to `production` immediately, and is then backported into `uat` and `develop` so the fix isn't lost on the next release.

---

## 2. Never Commit Directly to Main/UAT/Production

Protect all three long-lived branches (`production`, `uat`, `develop`).

**Required:**
- All changes go through a **Pull Request (PR)** — no direct pushes.
- **Code review** required before merge.
- **Branch protection** enabled on `production`, `uat`, and `develop`.

**Example GitHub branch protection rule:**
- Require pull request before merging
- Require status checks to pass (CI/CD)
- Require at least one code review approval
- Restrict who can push directly (no one, for protected branches)

---

## 3. Use Meaningful Commit Messages

Follow **Conventional Commits**.

**Format:**
```
type(scope): short description
```

**Examples:**
```
feat(auth): add JWT authentication
fix(api): resolve pagination bug
refactor(db): optimize query performance
docs(readme): update installation guide
test(user): add login unit tests
```

**Common commit types:**

| Type | Purpose |
|---|---|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code improvement, no behavior change |
| `docs` | Documentation only |
| `test` | Adding or updating tests |
| `chore` | Maintenance (deps, config, tooling) |

---

## 4. Keep Commits Small and Atomic

One logical change per commit — it keeps history readable and makes reverts/bisects reliable.

```
❌ Bad:
update project

✅ Good:
feat(user): add user registration API
fix(user): handle duplicate email validation
```

---

## 5. Pull Before Push

Always sync with remote before pushing, to avoid unnecessary conflicts.

```bash
git pull origin develop
```

Safer (keeps history linear):
```bash
git pull --rebase origin develop
```

---

## 6. Feature Branch Workflow

```bash
git checkout develop
git pull origin develop
git checkout -b feature/payment-api

# work, then commit
git push origin feature/payment-api
```

Then open a **Pull Request into `develop`** (never straight into `uat` or `production`).

---

## 7. Use Pull Requests for Code Review

Never merge without review. Every PR should satisfy this checklist before merging:

- [ ] Code review completed and approved
- [ ] Tests passing
- [ ] CI/CD pipeline passed (formatting, lint, security scan, tests)
- [ ] Documentation updated (if behavior or API changed)

---

## 8. Use Git Tags for Versions

Use **Semantic Versioning**: `vMAJOR.MINOR.PATCH`

```
v1.0.0   → initial release
v1.1.0   → new backward-compatible feature
v1.1.1   → backward-compatible bug fix
```

```bash
git tag v1.0.0
git push origin v1.0.0
```

---

## 9. Write a Proper `.gitignore`

**Example for Python / Django / FastAPI projects:**

```gitignore
__pycache__/
*.pyc
*.pyo
*.env
.env
venv/
.idea/
.vscode/
dist/
build/
*.log
migrations/
```

**Never commit:**
- Secrets or credentials
- API keys
- Environment variable files (`.env`)

---

## 10. CI/CD Integration & Code Quality Tools

Run automated checks on every push/PR. Recommended pipeline tools: **GitHub Actions**, **GitLab CI**, or **Jenkins**.

Configure the following in **both local dev environment and CI/CD pipeline**:

| Tool | Purpose |
|---|---|
| `black` | Code formatting |
| `isort` | Import ordering |
| `bandit` | Security scanning |
| `pylint` | Advanced code quality / linting |
| `mypy` | Static type checking |
| `pytest` | Automated tests |

A PR should not be mergeable unless all of these pass in CI.

**Local pre-commit setup (recommended):**
```bash
pip install pre-commit
pre-commit install
```
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: stable
    hooks: [{id: black}]
  - repo: https://github.com/PyCQA/isort
    rev: stable
    hooks: [{id: isort}]
  - repo: https://github.com/PyCQA/bandit
    rev: stable
    hooks: [{id: bandit}]
```

---

## 11. Use Squash Merging

Keeps `production`/`uat`/`develop` history clean — one commit per feature/fix instead of a noisy trail of WIP commits.

**Before squash (on the feature branch):**
```
fix
fix again
update
typo fix
```

**After squash (on merge into develop):**
```
feat(auth): implement login API
```

---

## 12. Delete Merged Branches

Keep the repository clean once a branch is merged:

```bash
git branch -d feature/payment-api
git push origin --delete feature/payment-api
```

---

## 13. Protect Secrets

**Never commit:**
```
.env
credentials.json
private_key.pem
```

**Use instead:**
- Environment variables
- A secrets manager (AWS Secrets Manager, HashiCorp Vault, etc.)
- Platform-native secret storage (GitHub Actions Secrets, GitLab CI/CD Variables)

Add `detect-secrets` or `git-secrets` as a pre-commit hook to catch accidental leaks before they're pushed.

---

## 14. Maintain Clean History

Prefer rebasing your feature branch on top of `develop` over merging `develop` into your branch — it avoids unnecessary merge commits.

```bash
git rebase develop
```
instead of
```bash
git merge develop
```

⚠️ Only rebase branches that are **not shared** with others (e.g., your own feature branch before it's opened as a PR). Never rebase `production`, `uat`, or `develop`.

---

## 15. Use a Proper Repository Structure

**Example for a Python backend:**

```
project/
│
├── app/
├── tests/
├── docs/
├── scripts/
├── requirements.txt
├── pyproject.toml
├── README.md
└── .gitignore
```

---

## Quick Reference Summary

| Practice | Rule |
|---|---|
| Branching | `production` / `uat` / `develop` + `feature/*`, `bugfix/*`, `hotfix/*` |
| PR Flow | `feature/bugfix → develop → uat → production`; `hotfix → production → uat & develop` |
| Direct commits | Never to `production`, `uat`, or `develop` |
| Commit format | `type(scope): short description` (Conventional Commits) |
| Commit size | Small, atomic, one logical change |
| Before push | `git pull --rebase origin <branch>` |
| Code review | Mandatory PR + approval before merge |
| Versioning | `vMAJOR.MINOR.PATCH` tags |
| Secrets | Never committed — env vars / secret manager only |
| CI/CD checks | `black`, `isort`, `bandit`, `pylint`, `mypy`, `pytest` |
| Merge style | Squash merge into shared branches |
| Cleanup | Delete branch after merge (local + remote) |
| History | Rebase local feature branches; never rebase shared branches |

---

*Onboard new team members with this doc, and enforce it via branch protection rules + required CI checks rather than relying on manual discipline alone.*
