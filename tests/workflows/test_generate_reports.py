from datetime import datetime, timezone

from fingertips_consol.workflows.generate_reports import (
    build_results_from_payload,
    generate_reports,
)


def test_generate_reports_writes_expected_files(tmp_path) -> None:
    payload = [
        {
            "indicator_id": 1,
            "indicator_name": "Smoking prevalence",
            "profile_name": "Wider determinants",
            "area_code": "E10000031",
            "area_name": "Warwickshire",
            "latest_value": 16.2,
            "england_value": 13.8,
            "trend": "worsening",
            "benchmark": "worse_than_england",
        }
    ]

    results = build_results_from_payload(payload)
    outputs = generate_reports(results, tmp_path, generated_at=datetime.now(timezone.utc))

    assert outputs["focus"].exists()
    assert outputs["doing_well"].exists()
