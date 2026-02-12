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

Generate a live-data prototype report from Fingertips API (Warwickshire + districts):

```bash
.venv/bin/python -m fingertips_consol.cli \
  --live-prototype \
  --output-dir assets/output/live-prototype \
  --max-indicators 120
```

Use `--max-indicators 0` to include all available indicators in the selected profile.

Equivalent helper script:

```bash
scripts/run_live_prototype.sh assets/output/live-prototype 120
```

Print the current implementation defaults for open product decisions:

```bash
.venv/bin/python -m fingertips_consol.cli --print-decision-defaults
```

## Notes

- This is intentionally a bootstrap. API integration and governance controls are stubbed with clear extension points.
- See `docs/open-questions.md` for decisions needed to complete implementation.
- See `docs/fingertips-api-intro-tutorial.md` for a researched Fingertips API intro + onboarding tutorial for this repo.
- See `docs/prototype.md` for live prototype endpoint and mapping details.
- Use `scripts/update_progress.sh "<note>"` to append timestamped updates to `PROGRESS.md`.
