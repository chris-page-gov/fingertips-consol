"""Command line entrypoint for report generation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from fingertips_consol.workflows.generate_reports import (
    build_results_from_payload,
    generate_reports,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Fingertips monitoring reports.")
    parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="Path to JSON array containing analyzed indicator rows.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("assets/output"),
        help="Directory for generated markdown reports.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    payload = json.loads(args.input.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("Input JSON must be a list of indicator rows")

    results = build_results_from_payload(payload)
    outputs = generate_reports(results, output_dir=args.output_dir)

    print("Generated reports:")
    for report_type, path in outputs.items():
        print(f"- {report_type}: {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
