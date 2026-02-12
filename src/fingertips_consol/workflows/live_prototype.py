"""Live-data prototype workflow using the Fingertips API."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from fingertips_consol.decision_defaults import DEFAULT_DECISIONS
from fingertips_consol.ingest.fingertips_client import FingertipsClient
from fingertips_consol.models import BenchmarkClass, IndicatorResult, TrendClass
from fingertips_consol.workflows.generate_reports import generate_reports

ENGLAND_AREA_CODE = "E92000001"
ENGLAND_COMPARATOR_ID = "4"


@dataclass(frozen=True)
class PrototypeConfig:
    profile_key: str = "public-health-outcomes-framework"
    parent_area_code: str = DEFAULT_DECISIONS.warwickshire.county_area_code
    parent_area_name: str = DEFAULT_DECISIONS.warwickshire.county_area_name
    child_area_type_id: int = DEFAULT_DECISIONS.warwickshire.child_area_type_id
    parent_area_type_id: int = DEFAULT_DECISIONS.warwickshire.county_area_type_id
    england_area_type_id: int = DEFAULT_DECISIONS.warwickshire.england_area_type_id
    district_area_codes: tuple[str, ...] = DEFAULT_DECISIONS.warwickshire.district_area_codes
    validate_district_area_codes: bool = True
    output_dir: Path = Path("assets/output/live-prototype")
    max_indicators: int = 120


def _chunked(values: list[int], size: int) -> Iterable[list[int]]:
    for index in range(0, len(values), size):
        yield values[index : index + size]


def _grouping(root: dict[str, Any]) -> dict[str, Any]:
    grouping = root.get("Grouping")
    if isinstance(grouping, list) and grouping:
        return grouping[0]
    return {}


def _root_key(root: dict[str, Any]) -> tuple[int, int, int, int, int, int]:
    group = _grouping(root)
    return (
        int(root.get("IID", -1)),
        int(group.get("SexId", -1)),
        int(group.get("AgeId", -1)),
        int(group.get("YearRange", -1)),
        int(group.get("CategoryTypeId", -1)),
        int(group.get("CategoryId", -1)),
    )


def _resolve_trend_marker(trend_payload: dict[str, Any] | None) -> int | None:
    if not isinstance(trend_payload, dict):
        return None

    marker = int(trend_payload.get("Marker", 0))
    if marker != 0:
        return marker

    latest_comparison = trend_payload.get("MarkerForMostRecentValueComparedWithPreviousValue")
    if latest_comparison is None:
        return None
    return int(latest_comparison)


def _trend_from_marker(marker: int | None, polarity_id: int) -> TrendClass:
    if marker in {None, 0, 3}:
        return TrendClass.STABLE

    if polarity_id == 1:
        if marker == 1:
            return TrendClass.IMPROVING
        if marker == 2:
            return TrendClass.WORSENING

    if polarity_id == 0:
        if marker == 1:
            return TrendClass.WORSENING
        if marker == 2:
            return TrendClass.IMPROVING

    return TrendClass.STABLE


def _benchmark_from_sig_code(sig_code: int | None, sig_labels: dict[int, str]) -> BenchmarkClass:
    if sig_code is None:
        return BenchmarkClass.SIMILAR_TO_ENGLAND

    label = sig_labels.get(sig_code, "").lower()
    if "better" in label:
        return BenchmarkClass.BETTER_THAN_ENGLAND
    if "worse" in label:
        return BenchmarkClass.WORSE_THAN_ENGLAND
    return BenchmarkClass.SIMILAR_TO_ENGLAND


def _ci_bounds(row: dict[str, Any]) -> tuple[float, float] | None:
    low = row.get("LoCI")
    high = row.get("UpCI")
    if low is None or high is None:
        return None

    try:
        return float(low), float(high)
    except (TypeError, ValueError):
        return None


def _benchmark_from_ci(
    local_row: dict[str, Any],
    england_row: dict[str, Any],
    polarity_id: int,
) -> BenchmarkClass | None:
    local_ci = _ci_bounds(local_row)
    england_ci = _ci_bounds(england_row)
    if local_ci is None or england_ci is None:
        return None

    local_low, local_high = local_ci
    england_low, england_high = england_ci

    if local_high < england_low:
        if polarity_id == 0:
            return BenchmarkClass.BETTER_THAN_ENGLAND
        if polarity_id == 1:
            return BenchmarkClass.WORSE_THAN_ENGLAND
        return BenchmarkClass.SIMILAR_TO_ENGLAND

    if local_low > england_high:
        if polarity_id == 0:
            return BenchmarkClass.WORSE_THAN_ENGLAND
        if polarity_id == 1:
            return BenchmarkClass.BETTER_THAN_ENGLAND
        return BenchmarkClass.SIMILAR_TO_ENGLAND

    return BenchmarkClass.SIMILAR_TO_ENGLAND


def _sig_code_for_england(row: dict[str, Any]) -> int | None:
    sig = row.get("Sig")
    if not isinstance(sig, dict):
        return None

    code = sig.get(ENGLAND_COMPARATOR_ID)
    if code is None:
        code = sig.get(int(ENGLAND_COMPARATOR_ID))
    if code is None:
        return None
    return int(code)


def _valid_value(row: dict[str, Any]) -> float | None:
    value = row.get("Val")
    formatted = str(row.get("ValF", "")).strip()

    if value is None or formatted in {"", "-", "x"}:
        return None
    return float(value)


def _benchmark_with_fallback(
    *,
    local_row: dict[str, Any],
    england_row: dict[str, Any] | None,
    polarity_id: int,
    sig_labels: dict[int, str],
) -> tuple[BenchmarkClass, str]:
    sig_code = _sig_code_for_england(local_row)
    if sig_code is not None:
        return _benchmark_from_sig_code(sig_code, sig_labels), "sig"

    if england_row is not None:
        ci_benchmark = _benchmark_from_ci(local_row, england_row, polarity_id)
        if ci_benchmark is not None:
            return ci_benchmark, "ci"

    return BenchmarkClass.SIMILAR_TO_ENGLAND, "default"


def _indicator_name(root: dict[str, Any], metadata: dict[str, Any]) -> str:
    indicator_id = str(root.get("IID"))
    meta_entry = metadata.get(indicator_id, {}) if isinstance(metadata, dict) else {}
    descriptive = meta_entry.get("Descriptive", {}) if isinstance(meta_entry, dict) else {}

    base_name = descriptive.get("Name")
    if not isinstance(base_name, str) or not base_name.strip():
        base_name = f"Indicator {indicator_id}"

    qualifiers: list[str] = []
    if bool(root.get("StateSex")):
        sex_name = (root.get("Sex") or {}).get("Name")
        if isinstance(sex_name, str) and sex_name:
            qualifiers.append(sex_name)
    if bool(root.get("StateAge")):
        age_name = (root.get("Age") or {}).get("Name")
        if isinstance(age_name, str) and age_name:
            qualifiers.append(age_name)
    period = _grouping(root).get("Period")
    if isinstance(period, str) and period:
        qualifiers.append(period)

    if qualifiers:
        return f"{base_name} ({', '.join(qualifiers)})"
    return base_name


def _significance_labels_by_polarity(client: FingertipsClient) -> dict[int, dict[int, str]]:
    labels: dict[int, dict[int, str]] = {}
    for polarity_id in (-1, 0, 1, 99):
        entries = client.get_comparator_significances(polarity_id)
        labels[polarity_id] = {
            int(entry.get("Id", -1)): str(entry.get("Name", ""))
            for entry in entries
            if isinstance(entry, dict)
        }
    return labels


def _area_lookup(
    client: FingertipsClient,
    config: PrototypeConfig,
    profile_id: int,
) -> dict[str, str]:
    areas = client.get_areas_by_parent_area_code(
        area_type_id=config.child_area_type_id,
        parent_area_code=config.parent_area_code,
        profile_id=profile_id,
    )
    lookup = {
        str(area.get("Code")): str(area.get("Name")) for area in areas if isinstance(area, dict)
    }
    lookup[config.parent_area_code] = config.parent_area_name
    lookup[ENGLAND_AREA_CODE] = "England"
    return lookup


def _district_codes_for_run(
    area_names: dict[str, str],
    config: PrototypeConfig,
) -> tuple[set[str], list[str], list[str]]:
    api_district_codes = {
        code
        for code, name in area_names.items()
        if code not in {config.parent_area_code, ENGLAND_AREA_CODE} and name
    }
    configured_codes = set(config.district_area_codes)

    if not config.validate_district_area_codes:
        return api_district_codes, [], []

    missing = sorted(configured_codes - api_district_codes)
    extra = sorted(api_district_codes - configured_codes)
    # Prefer canonical list while still allowing execution when any configured code is available.
    selected = configured_codes & api_district_codes
    if selected:
        return selected, missing, extra
    return api_district_codes, missing, extra


def run_live_prototype(
    config: PrototypeConfig,
    client: FingertipsClient | None = None,
) -> dict[str, Any]:
    if config.max_indicators < 0:
        raise ValueError("max_indicators must be zero or greater")

    fingertips = client or FingertipsClient()

    profile = fingertips.get_profile_by_key(config.profile_key)
    profile_id = int(profile.get("Id", 0))
    if profile_id <= 0:
        raise ValueError(f"Unable to resolve profile for key '{config.profile_key}'")

    group_ids = [int(group_id) for group_id in profile.get("GroupIds", [])]
    if not group_ids:
        raise ValueError(f"No groups available for profile key '{config.profile_key}'")

    group_metadata = fingertips.get_group_metadata(group_ids)
    group_names = {
        int(item.get("Id")): str(item.get("Name", f"Group {item.get('Id')}"))
        for item in group_metadata
        if isinstance(item, dict)
    }

    area_names = _area_lookup(fingertips, config, profile_id)
    district_codes, district_missing, district_extra = _district_codes_for_run(area_names, config)
    if not district_codes:
        raise ValueError("No district area codes available for live prototype run")

    sig_labels_by_polarity = _significance_labels_by_polarity(fingertips)

    results: list[IndicatorResult] = []
    selected_indicator_count = 0
    benchmark_source_counts: dict[str, int] = {"sig": 0, "ci": 0, "default": 0}

    for group_id in group_ids:
        remaining = config.max_indicators - selected_indicator_count
        if config.max_indicators > 0 and remaining <= 0:
            break

        indicator_metadata = fingertips.get_indicator_metadata_by_group_ids([group_id])
        indicator_ids = sorted(int(value) for value in indicator_metadata.keys())
        if config.max_indicators > 0:
            indicator_ids = indicator_ids[:remaining]
        if not indicator_ids:
            continue

        selected_indicator_count += len(indicator_ids)
        group_name = group_names.get(group_id, f"Group {group_id}")

        for chunk in _chunked(indicator_ids, size=100):
            district_roots = fingertips.get_latest_data_for_child_areas(
                area_type_id=config.child_area_type_id,
                parent_area_code=config.parent_area_code,
                indicator_ids=chunk,
                profile_id=profile_id,
            )
            warwickshire_roots = fingertips.get_latest_data_for_single_area(
                area_type_id=config.parent_area_type_id,
                area_code=config.parent_area_code,
                indicator_ids=chunk,
                restrict_to_profile_ids=[profile_id],
            )
            england_roots = fingertips.get_latest_data_for_single_area(
                area_type_id=config.england_area_type_id,
                area_code=ENGLAND_AREA_CODE,
                indicator_ids=chunk,
                restrict_to_profile_ids=[profile_id],
            )

            england_row_by_key: dict[tuple[int, int, int, int, int, int], dict[str, Any]] = {}
            for root in england_roots:
                key = _root_key(root)
                data = root.get("Data")
                if isinstance(data, list) and data:
                    row = data[0]
                    value = _valid_value(row)
                    if value is not None:
                        england_row_by_key[key] = row

            warwickshire_trend_by_key: dict[tuple[int, int, int, int, int, int], TrendClass] = {}
            for root in district_roots:
                key = _root_key(root)
                polarity_id = int(root.get("PolarityId", -1))
                trend_payload = (root.get("RecentTrends") or {}).get(config.parent_area_code)
                marker = _resolve_trend_marker(trend_payload)
                warwickshire_trend_by_key[key] = _trend_from_marker(marker, polarity_id)

            for root in district_roots:
                key = _root_key(root)
                england_row = england_row_by_key.get(key)
                if england_row is None:
                    continue
                england_value = _valid_value(england_row)
                if england_value is None:
                    continue

                polarity_id = int(root.get("PolarityId", -1))
                sig_labels = sig_labels_by_polarity.get(polarity_id, {})
                indicator_name = _indicator_name(root, indicator_metadata)
                trend_map = root.get("RecentTrends") or {}

                data_rows = root.get("Data")
                if not isinstance(data_rows, list):
                    continue

                for row in data_rows:
                    area_code = str(row.get("AreaCode", ""))
                    if area_code not in district_codes:
                        continue

                    latest_value = _valid_value(row)
                    if latest_value is None:
                        continue

                    marker = _resolve_trend_marker(trend_map.get(area_code))
                    trend = _trend_from_marker(marker, polarity_id)
                    benchmark, benchmark_source = _benchmark_with_fallback(
                        local_row=row,
                        england_row=england_row,
                        polarity_id=polarity_id,
                        sig_labels=sig_labels,
                    )
                    benchmark_source_counts[benchmark_source] += 1

                    results.append(
                        IndicatorResult(
                            indicator_id=int(root.get("IID", -1)),
                            indicator_name=indicator_name,
                            profile_name=group_name,
                            area_code=area_code,
                            area_name=area_names.get(area_code, area_code),
                            latest_value=latest_value,
                            england_value=england_value,
                            trend=trend,
                            benchmark=benchmark,
                            notes=[f"benchmark_source:{benchmark_source}"],
                        )
                    )

            for root in warwickshire_roots:
                key = _root_key(root)
                england_row = england_row_by_key.get(key)
                if england_row is None:
                    continue
                england_value = _valid_value(england_row)
                if england_value is None:
                    continue

                data_rows = root.get("Data")
                if not isinstance(data_rows, list) or not data_rows:
                    continue

                row = data_rows[0]
                latest_value = _valid_value(row)
                if latest_value is None:
                    continue

                polarity_id = int(root.get("PolarityId", -1))
                sig_labels = sig_labels_by_polarity.get(polarity_id, {})
                indicator_name = _indicator_name(root, indicator_metadata)
                benchmark, benchmark_source = _benchmark_with_fallback(
                    local_row=row,
                    england_row=england_row,
                    polarity_id=polarity_id,
                    sig_labels=sig_labels,
                )
                benchmark_source_counts[benchmark_source] += 1
                trend = warwickshire_trend_by_key.get(key, TrendClass.STABLE)

                results.append(
                    IndicatorResult(
                        indicator_id=int(root.get("IID", -1)),
                        indicator_name=indicator_name,
                        profile_name=group_name,
                        area_code=config.parent_area_code,
                        area_name=config.parent_area_name,
                        latest_value=latest_value,
                        england_value=england_value,
                        trend=trend,
                        benchmark=benchmark,
                        notes=[f"benchmark_source:{benchmark_source}"],
                    )
                )

    outputs = generate_reports(results, output_dir=config.output_dir)
    return {
        "profile_id": profile_id,
        "group_ids": group_ids,
        "indicators_selected": selected_indicator_count,
        "result_rows": len(results),
        "benchmark_sources": benchmark_source_counts,
        "district_codes_used": sorted(district_codes),
        "district_codes_missing": district_missing,
        "district_codes_extra_from_api": district_extra,
        "output_paths": outputs,
    }
