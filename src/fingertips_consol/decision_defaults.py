"""Default product decisions derived from docs/open-questions.md."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class WarwickshireDefaults:
    county_area_code: str = "E10000031"
    county_area_name: str = "Warwickshire"
    district_area_codes: tuple[str, ...] = (
        "E07000218",  # North Warwickshire
        "E07000219",  # Nuneaton and Bedworth
        "E07000220",  # Rugby
        "E07000221",  # Stratford-on-Avon
        "E07000222",  # Warwick
    )
    england_area_code: str = "E92000001"
    child_area_type_id: int = 501
    county_area_type_id: int = 502
    england_area_type_id: int = 15


@dataclass(frozen=True)
class DeliveryDefaults:
    primary_format: str = "html"
    canonical_source_format: str = "markdown"
    optional_formats: tuple[str, ...] = ("pdf", "email_summary")


@dataclass(frozen=True)
class ReviewDefaults:
    workflow: str = "two_stage_signoff"
    steps: tuple[str, ...] = (
        "automated_qa_gate",
        "analyst_review",
        "named_approver_signoff",
    )


@dataclass(frozen=True)
class ScheduleDefaults:
    routine_cadence: str = "weekly"
    on_demand_triggers: tuple[str, ...] = ("analyst_request", "data_change_detected")
    digest_cadence: str = "monthly"


@dataclass(frozen=True)
class BenchmarkDefaults:
    strategy: str = "sig_then_ci_then_threshold"
    england_comparator_id: str = "4"
    bob_polarity_handling: str = "neutral_lower_higher"


@dataclass(frozen=True)
class EndpointDefaults:
    strategy: str = "granular_v1"
    api_docs_version: str = "v1"
    required_paths: tuple[str, ...] = (
        "/api/profile/by_key",
        "/api/group_metadata",
        "/api/indicator_metadata/by_group_id",
        "/api/latest_data/specific_indicators_for_child_areas",
        "/api/latest_data/specific_indicators_for_single_area",
        "/api/comparator_significances",
    )
    optimization_paths: tuple[str, ...] = (
        "/api/latest_data/all_indicators_in_profile_group_for_child_areas",
        "/api/latest_data/all_indicators_in_profile_group_for_single_area",
    )


@dataclass(frozen=True)
class StakeholderDefaults:
    profile_map: dict[str, tuple[str, ...]] = field(
        default_factory=lambda: {
            "public_health_intelligence": (
                "public-health-outcomes-framework",
                "health-profiles",
                "mortality-profile",
                "populations",
            ),
            "health_improvement": (
                "tobacco-control",
                "obesity-physical-activity-nutrition",
                "local-alcohol-profiles",
                "sexualhealth",
                "nhs-health-check-detailed",
            ),
            "health_protection": (
                "health-protection",
                "tb-monitoring",
                "amr-local-indicators",
            ),
            "children_and_young_people": (
                "child-health-profiles",
                "perinatal-cyp-mental-health",
            ),
            "mental_health_and_wellbeing": (
                "adult-mental-health-wellbeing",
                "suicide-prevention",
                "dementia",
            ),
            "wider_determinants_and_inequalities": (
                "wider-determinants",
                "inequality-tools",
                "local-health",
            ),
            "long_term_conditions_and_prevention": (
                "cardiovascular",
                "diabetes-ft",
                "cardiovascular-disease-diabetes-kidney-disease",
                "respiratory-disease",
                "msk",
                "liver-disease",
            ),
        }
    )


@dataclass(frozen=True)
class DecisionDefaults:
    endpoints: EndpointDefaults = EndpointDefaults()
    warwickshire: WarwickshireDefaults = WarwickshireDefaults()
    benchmark: BenchmarkDefaults = BenchmarkDefaults()
    delivery: DeliveryDefaults = DeliveryDefaults()
    review: ReviewDefaults = ReviewDefaults()
    schedule: ScheduleDefaults = ScheduleDefaults()
    stakeholders: StakeholderDefaults = StakeholderDefaults()


DEFAULT_DECISIONS = DecisionDefaults()


def decision_defaults_as_dict() -> dict[str, Any]:
    """Return serializable decision defaults."""
    return asdict(DEFAULT_DECISIONS)
