# User Guide (Beginner)

## What This Tool Does

Fingertips Consol takes indicator data in JSON format and creates two markdown reports:

- `focus-report.md`: indicators that may need attention.
- `doing-well-report.md`: indicators showing positive status or direction.

## Before You Start

You need:

- macOS, Linux, or Windows with a shell
- Python 3.11+
- access to this repository folder

## One-Time Setup

From the project root:

```bash
make setup
```

This creates `.venv/` and installs the project plus developer tools.

## Generate Reports

Use the sample data to check everything works:

```bash
./.venv/bin/python -m fingertips_consol.cli \
  --input assets/sample-indicators.json \
  --output-dir assets/output
```

You should see output listing two files:

- `assets/output/focus-report.md`
- `assets/output/doing-well-report.md`

## Understand the Output

Each report includes:

- generation timestamp
- markdown table with indicator, profile, geography, local value, England value, trend, and benchmark status

An indicator goes to:

- focus report if trend is worsening or benchmark is worse than England
- doing-well report if trend is improving or benchmark is better than England

## Common Commands

- `make dev`: show CLI help
- `make tdd`: run tests quickly while developing
- `make test`: run full tests with coverage gate
- `make lint`: run lint and format checks

## Troubleshooting

- Error: `Input JSON must be a list`
  Fix: ensure the file is a JSON array (`[...]`) of indicator objects.
- Missing package or command errors
  Fix: rerun `make setup`.
- Reports not generated
  Fix: verify `--input` path exists and contains required fields.
