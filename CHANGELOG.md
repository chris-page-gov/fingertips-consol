# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project aims to follow Semantic Versioning.

## [Unreleased]

### Added
- `CONTEXT.md` for durable architecture and operating context.
- `PROGRESS.md` for live execution status and handoff continuity.
- `CHANGELOG.md` for notable change tracking.
- `scripts/update_progress.sh` to update the progress date and append timestamped activity notes.
- Coverage gate at 95% via `pytest-cov` configuration in `pyproject.toml`.
- `make tdd` command for fast red/green cycles.
- New tests for CLI, config, ingest client, notifications grouping, and additional analysis branches.

### Changed
- Repository guidance now documents TDD-first workflow and enforced coverage expectations.

## [0.1.0] - 2026-02-12

### Added
- Initial repository scaffold and development tooling (`Makefile`, `pyproject.toml`, `.env.example`).
- Core package structure under `src/fingertips_consol/` for ingest, analysis, reporting, notifications, and workflows.
- CLI entrypoint to generate focus/doing-well markdown reports from JSON payloads.
- Initial tests for analysis, reporting, and workflow generation.
- Supporting docs (`README.md`, `docs/specification.md`, `docs/architecture.md`, `docs/open-questions.md`).
- Sample data and routine script (`assets/sample-indicators.json`, `scripts/run_routine.sh`).
