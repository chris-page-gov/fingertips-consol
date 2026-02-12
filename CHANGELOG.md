# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project aims to follow Semantic Versioning.

## [Unreleased]

### Added
- `CONTEXT.md` for durable architecture and operating context.
- `PROGRESS.md` for live execution status and handoff continuity.
- `CHANGELOG.md` for notable change tracking.
- `scripts/update_progress.sh` to update the progress date and append timestamped activity notes.
- Live Fingertips prototype workflow using official API endpoints.
- `scripts/run_live_prototype.sh` helper to execute the live prototype quickly.
- `docs/prototype.md` documenting endpoint usage, defaults, and prototype limitations.
- `docs/fingertips-api-intro-tutorial.md` with API design/function/history/future context and repo onboarding walkthrough.
- CLI live mode (`--live-prototype`) with configurable profile/area settings.
- Workflow tests for trend and benchmark mapping in live prototype logic.
- API client retry/backoff support for timeout, 429, and 5xx responses.
- CI-based England benchmark fallback when source significance is unavailable.
- Retry-behavior tests for Fingertips API client.
- Full-coverage mode with `--max-indicators 0`.

## [0.1.0] - 2026-02-12

### Added
- Initial repository scaffold and development tooling (`Makefile`, `pyproject.toml`, `.env.example`).
- Core package structure under `src/fingertips_consol/` for ingest, analysis, reporting, notifications, and workflows.
- CLI entrypoint to generate focus/doing-well markdown reports from JSON payloads.
- Initial tests for analysis, reporting, and workflow generation.
- Supporting docs (`README.md`, `docs/specification.md`, `docs/architecture.md`, `docs/open-questions.md`).
- Sample data and routine script (`assets/sample-indicators.json`, `scripts/run_routine.sh`).
