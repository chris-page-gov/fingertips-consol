"""Command line entrypoint for report generation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from fingertips_consol.decision_defaults import decision_defaults_as_dict
from fingertips_consol.workflows.generate_reports import (
    build_results_from_payload,
    generate_reports,
)
from fingertips_consol.workflows.live_prototype import PrototypeConfig, run_live_prototype


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Fingertips monitoring reports.")
    parser.add_argument(
        "--print-decision-defaults",
        action="store_true",
        help="Print decision defaults from docs/open-questions.md mapping as JSON and exit.",
    )
    parser.add_argument(
        "--live-prototype",
        action="store_true",
        help="Fetch data live from Fingertips API and generate prototype reports.",
    )
    parser.add_argument(
        "--input",
        type=Path,
        help="Path to JSON array containing analyzed indicator rows (non-live mode).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("assets/output"),
        help="Directory for generated markdown reports.",
    )
    parser.add_argument(
        "--profile-key",
        default="public-health-outcomes-framework",
        help="Fingertips profile key for live prototype mode.",
    )
    parser.add_argument(
        "--parent-area-code",
        default="E10000031",
        help="Parent area code for live prototype mode.",
    )
    parser.add_argument(
        "--parent-area-name",
        default="Warwickshire",
        help="Parent area display name for live prototype mode.",
    )
    parser.add_argument(
        "--child-area-type-id",
        type=int,
        default=501,
        help="Child area type ID for live prototype mode.",
    )
    parser.add_argument(
        "--parent-area-type-id",
        type=int,
        default=502,
        help="Parent area type ID for live prototype mode.",
    )
    parser.add_argument(
        "--england-area-type-id",
        type=int,
        default=15,
        help="England area type ID for live prototype mode.",
    )
    parser.add_argument(
        "--max-indicators",
        type=int,
        default=120,
        help="Maximum number of indicators to include in live prototype mode.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.print_decision_defaults:
        print(json.dumps(decision_defaults_as_dict(), indent=2))
        return 0

    if args.live_prototype:
        summary = run_live_prototype(
            PrototypeConfig(
                profile_key=args.profile_key,
                parent_area_code=args.parent_area_code,
                parent_area_name=args.parent_area_name,
                child_area_type_id=args.child_area_type_id,
                parent_area_type_id=args.parent_area_type_id,
                england_area_type_id=args.england_area_type_id,
                output_dir=args.output_dir,
                max_indicators=args.max_indicators,
            )
        )
        print("Generated live prototype reports:")
        for report_type, path in summary["output_paths"].items():
            print(f"- {report_type}: {path}")
        print(f"Indicators selected: {summary['indicators_selected']}")
        print(f"Rows in reports: {summary['result_rows']}")
        print(
            "Benchmark sources: "
            + ", ".join(f"{k}={v}" for k, v in summary["benchmark_sources"].items())
        )
        print("District codes used: " + ", ".join(summary["district_codes_used"]))
        if summary["district_codes_missing"]:
            missing_codes = ", ".join(summary["district_codes_missing"])
            print("District codes missing from API: " + missing_codes)
        if summary["district_codes_extra_from_api"]:
            print(
                "District codes returned by API but not in canonical defaults: "
                + ", ".join(summary["district_codes_extra_from_api"])
            )
        return 0

    if args.input is None:
        raise ValueError("Provide --input for JSON mode or use --live-prototype")

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
