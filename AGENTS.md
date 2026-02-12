# Repository Guidelines

## Project Structure & Module Organization
This repository is currently a clean bootstrap with no committed source files yet. Keep the root minimal and organize new work by purpose:
- `src/` application or library code
- `tests/` automated tests mirroring `src/` structure
- `scripts/` repeatable developer/CI utilities
- `docs/` design notes, runbooks, and architecture decisions
- `assets/` static files (images, fixtures, sample data)

Prefer small, focused modules and avoid deep nesting unless it improves clarity.

## Build, Test, and Development Commands
There is no build system configured yet. When adding one, expose a small standard command set and document it in both `README.md` and this file.

Suggested baseline commands to add:
- `make setup` installs dependencies and local tooling
- `make test` runs the full test suite
- `make lint` runs format/lint checks
- `make dev` starts local development mode

Until then, use simple repo checks like `ls -la` and `git status` before opening PRs.

## Coding Style & Naming Conventions
Adopt formatter-first workflows and commit formatter config with the first language/toolchain PR.
- Use descriptive names (`user_profile_service`, not `ups`)
- Files/directories: lowercase with hyphens or underscores, consistent per language
- Keep functions small and side effects explicit
- Prefer explicit imports and avoid unused code

## Testing Guidelines
No testing framework is configured yet. Add tests in the same PR as new behavior.
- Mirror source layout under `tests/`
- Name tests by behavior (examples: `user-profile.test.ts`, `test_user_profile.py`)
- Include at least one success case and one failure/edge case per feature

## Commit & Pull Request Guidelines
Git history is not established here yet; adopt Conventional Commits from the start:
- `feat: add initial parser`
- `fix: handle empty input`
- `chore: add lint config`

PRs should include:
- clear summary and scope
- linked issue (if available)
- test evidence (command + result)
- screenshots for UI/visual changes

## Security & Configuration Tips
Do not commit secrets. Keep local values in `.env.local` and provide safe defaults in `.env.example`.
