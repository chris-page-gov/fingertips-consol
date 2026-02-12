# Tutorial: Create Your First Reports

This tutorial walks through a full run from setup to report review.

## Step 1: Open a Terminal in the Project

Go to the repository root:

```bash
cd /path/to/fingertips-consol
```

## Step 2: Install Dependencies

Run:

```bash
make setup
```

Wait until installation completes.

## Step 3: Run a Local Report Build

Use the sample indicator file:

```bash
./.venv/bin/python -m fingertips_consol.cli \
  --input assets/sample-indicators.json \
  --output-dir assets/output/tutorial-run
```

Expected terminal output includes:

- `Generated reports:`
- `focus: .../focus-report.md`
- `doing_well: .../doing-well-report.md`

## Step 4: Open the Generated Files

Check both report files:

- `assets/output/tutorial-run/focus-report.md`
- `assets/output/tutorial-run/doing-well-report.md`

Each file is plain markdown and can be viewed in your editor.

## Step 5: Run Quality Checks

Run lint:

```bash
make lint
```

Run tests:

```bash
make test
```

The test command enforces at least 95% total coverage.

## Step 6: Try Your Own Data

Create a new JSON file using the same shape as `assets/sample-indicators.json`, then run:

```bash
./.venv/bin/python -m fingertips_consol.cli \
  --input /path/to/your-data.json \
  --output-dir assets/output/my-run
```

If your JSON is not a list of objects, the CLI will stop with a validation error.
