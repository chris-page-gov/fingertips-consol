#!/usr/bin/env bash
set -euo pipefail

OUTPUT_DIR=${1:-assets/output/live-prototype}
MAX_INDICATORS=${2:-120}

.venv/bin/python -m fingertips_consol.cli \
  --live-prototype \
  --output-dir "$OUTPUT_DIR" \
  --max-indicators "$MAX_INDICATORS"
