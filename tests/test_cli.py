from __future__ import annotations

import runpy
import sys
from pathlib import Path

import pytest

from fingertips_consol.cli import main, parse_args


def _write_payload(path: Path, payload: str) -> None:
    path.write_text(payload, encoding="utf-8")


def test_parse_args_uses_default_output_dir(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    input_path = tmp_path / "input.json"
    _write_payload(input_path, "[]")
    monkeypatch.setattr(sys, "argv", ["fingertips-consol", "--input", str(input_path)])

    args = parse_args()

    assert args.input == input_path
    assert args.output_dir == Path("assets/output")


def test_main_raises_when_input_payload_is_not_a_list(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    input_path = tmp_path / "input.json"
    _write_payload(input_path, '{"indicator_id": 1}')
    monkeypatch.setattr(sys, "argv", ["fingertips-consol", "--input", str(input_path)])

    with pytest.raises(ValueError, match="Input JSON must be a list"):
        main()


def test_main_generates_reports_and_prints_output(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    input_path = tmp_path / "input.json"
    output_dir = tmp_path / "reports"
    _write_payload(
        input_path,
        """
[
  {
    "indicator_id": 1,
    "indicator_name": "Smoking prevalence",
    "profile_name": "Wider determinants",
    "area_code": "E10000031",
    "area_name": "Warwickshire",
    "latest_value": 16.2,
    "england_value": 13.8,
    "trend": "worsening",
    "benchmark": "worse_than_england"
  }
]
""",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["fingertips-consol", "--input", str(input_path), "--output-dir", str(output_dir)],
    )

    exit_code = main()

    assert exit_code == 0
    assert (output_dir / "focus-report.md").exists()
    assert (output_dir / "doing-well-report.md").exists()
    stdout = capsys.readouterr().out
    assert "Generated reports:" in stdout
    assert "focus:" in stdout
    assert "doing_well:" in stdout


def test_module_main_guard_exits_with_status_code_zero(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    input_path = tmp_path / "input.json"
    _write_payload(input_path, "[]")
    monkeypatch.setattr(sys, "argv", ["fingertips-consol", "--input", str(input_path)])
    sys.modules.pop("fingertips_consol.cli", None)

    with pytest.raises(SystemExit) as raised:
        runpy.run_module("fingertips_consol.cli", run_name="__main__")

    assert raised.value.code == 0
