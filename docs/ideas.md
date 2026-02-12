# Ideas Backlog

This file tracks candidate enhancements only.  
Canonical product requirements remain in `docs/specification.md`.

## Data and Ingestion

- Add retry/backoff policy for live Fingertips API requests.
- Cache metadata endpoints (profiles and indicators) to reduce repeated calls.
- Add input schema validation for ingest payloads before analysis.

## Analysis and Quality

- Add significance-aware benchmark classification using confidence intervals.
- Add configurable rules for category ordering and priority scoring.
- Add integration tests against representative live-like API fixtures.

## Reporting and Delivery

- Add optional HTML export alongside markdown.
- Add a compact summary section at the top of each report.
- Add profile/team notification templates from grouped focus indicators.

## Operations

- Add a release checklist document and automation script.
- Add CI workflow for lint/test/coverage gate on pull requests.
- Add structured logging and error codes for scheduled runs.
