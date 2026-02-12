# CONTEXT

## Purpose
Fingertips Consol is a public-health analytics app for Warwickshire monitoring. It ingests Fingertips indicator data, classifies trend and England benchmark status, and generates two outputs:
- indicators requiring focus
- indicators doing well

## Product Scope
- Geography: Warwickshire overall plus district/borough views
- Coverage: all relevant Fingertips indicators/profiles
- Modes: routine and on-demand report generation
- Audience: Public Health Intelligence and approved PH stakeholders

## Architecture Snapshot
- `src/fingertips_consol/ingest/`: API client and ingestion concerns
- `src/fingertips_consol/analysis/`: trend and benchmark classification logic
- `src/fingertips_consol/reporting/`: report composition and rendering
- `src/fingertips_consol/workflows/`: orchestration for routine/on-demand runs
- `src/fingertips_consol/notifications/`: profile/team highlight grouping

## Operational Commands
- `make setup`: create virtualenv and install dependencies
- `make lint`: run ruff checks and format validation
- `make test`: run pytest suite
- `make dev`: show CLI usage
- `scripts/update_progress.sh "<note>"`: update `PROGRESS.md` date and append an activity entry

## Governance and Security Constraints
- Data source is public Fingertips data, but governance still applies.
- Processing and dissemination must align with UK GDPR, Data Protection Act 2018, ONS PCMD rules, and local authority/ICS governance.
- Dissemination is restricted to approved PH staff.
- No secrets in git. Use `.env.local`; keep defaults in `.env.example`.

## Agent Working Agreement
- Update this file when core assumptions, architecture, or operating constraints change.
- Update `PROGRESS.md` for execution state and next actions.
- Update `CHANGELOG.md` for notable repo changes.
- Include validation evidence (`make lint`, `make test`) with significant code changes.
- Keep docs and code paths aligned; avoid stale references.

## Open Product Decisions
Canonical unresolved decisions live in:
- `docs/open-questions.md`

## Current Baseline (as of 2026-02-12)
- Python scaffold implemented with CLI, core modules, and tests.
- Report generation works from JSON payload input.
- Live prototype mode is implemented in CLI (`--live-prototype`) for Warwickshire + districts.
- API retry/backoff and full-profile mode (`--max-indicators 0`) are implemented.
- Remaining hardening: final polarity `99` benchmark rule and QA/approval pipeline.
