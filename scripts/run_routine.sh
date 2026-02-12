#!/usr/bin/env bash
set -euo pipefail

INPUT_PATH=${1:-assets/sample-indicators.json}
OUTPUT_DIR=${2:-assets/output}

.venv/bin/python -m fingertips_consol.cli --input "$INPUT_PATH" --output-dir "$OUTPUT_DIR"
