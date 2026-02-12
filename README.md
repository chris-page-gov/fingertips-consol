# Fingertips Consol

Lightweight analytics and monitoring scaffold for Fingertips public health indicators focused on Warwickshire and its districts/boroughs.

## What this skeleton covers

- Ingestion layer for Fingertips API data access
- Analysis layer for trend and England benchmark classification
- Reporting layer that splits outputs into:
  - indicators doing well
  - indicators requiring focus
- Workflow entrypoints for routine and on-demand reporting
- Initial tests and development tooling

## Repository layout

- `src/fingertips_consol/` core package
- `tests/` automated tests mirroring `src/`
- `scripts/` repeatable utilities
- `docs/` specification, architecture, and open questions
- `assets/` fixtures and static resources

## Quick start

```bash
make setup
make test
make lint
```

Generate reports from local JSON input:

```bash
.venv/bin/python -m fingertips_consol.cli \
  --input assets/sample-indicators.json \
  --output-dir assets/output
```

## Notes

- This is intentionally a bootstrap. API integration and governance controls are stubbed with clear extension points.
- See `docs/open-questions.md` for decisions needed to complete implementation.
- Use `scripts/update_progress.sh "<note>"` to append timestamped updates to `PROGRESS.md`.
