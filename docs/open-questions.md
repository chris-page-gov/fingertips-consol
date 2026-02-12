# Open Questions: Options and Recommendations

Research date: 2026-02-12

Decision interface: `docs/open-questions-decision-ui.html`

## 1) Which exact Fingertips endpoints/versions should be used for profile, indicator metadata, and time-series values?

| Option | What this means | Pros | Risks |
|---|---|---|---|
| A | Use Swagger `v1` granular endpoints (`/api/profile/by_key`, `/api/group_metadata`, `/api/indicator_metadata/by_group_id`, `/api/latest_data/specific_indicators_for_child_areas`, `/api/latest_data/specific_indicators_for_single_area`, `/api/comparator_significances`) | Clear contracts, easy to test, already implemented in prototype | More API calls |
| B | Use Swagger `v1` bulk latest-data endpoints (`/api/latest_data/all_indicators_in_profile_group_for_child_areas`, `/api/latest_data/all_indicators_in_profile_group_for_single_area`) | Fewer requests | Larger payloads, harder error isolation |
| C | Mix legacy-style area endpoints for data extraction | Flexible fallback | Inconsistent behavior across endpoints |

Warwickshire considerations:
- Current prototype flow already works with option A and Warwickshire area types (`501`, `502`, `15`).
- Swagger discovery shows the active documented API version is `v1`.

Recommendation:
- Adopt option A as production baseline.
- Keep option B as an optimization path behind a feature flag for large profile runs.

## 2) What is the canonical list of Warwickshire district/borough area codes to include by default?

| Option | What this means | Pros | Risks |
|---|---|---|---|
| A | Hard-code the five districts/boroughs and county code | Simple, deterministic | Needs manual update if geographies change |
| B | Resolve all child areas dynamically from API each run | Always current | Can drift from expected governance scope |
| C | Hybrid: fixed default list + runtime API validation | Stable and auditable, still catches changes | Slightly more logic |

Warwickshire default list (validated from Fingertips API `areas/by_parent_area_code` for `parent_area_code=E10000031`, `area_type_id=501`):
- `E07000218` North Warwickshire
- `E07000219` Nuneaton and Bedworth
- `E07000220` Rugby
- `E07000221` Stratford-on-Avon
- `E07000222` Warwick
- County: `E10000031` Warwickshire (area type `502`)
- Comparator: `E92000001` England (area type `15`)

Recommendation:
- Adopt option C with the list above as canonical defaults.

## 3) How should "statistically better/worse" be computed in production?

| Option | What this means | Pros | Risks |
|---|---|---|---|
| A | Use source significance (`Data[].Sig[4]` + `comparator_significances`) | Aligns with Fingertips methodology | Missing values for some rows |
| B | Compute using confidence intervals (`LoCI`, `UpCI`) | Transparent fallback when `Sig` missing | CI overlap is an approximation of significance |
| C | Custom value thresholds (for example ±5%) | Works when no significance metadata | Highest risk of false signals |
| D | Hybrid precedence rule | Robust and practical | Requires explicit governance rule |

Warwickshire considerations:
- Current prototype already reads `Sig[4]` (England comparator).
- Fingertips returns polarity-specific labels; for polarity `99`, labels are `Lower/Similar/Higher` rather than `Better/Worse`.

Recommendation:
- Adopt option D with this order:
1. Use `Sig[4]` + `comparator_significances(polarity_id)` when present.
2. If missing, use CI rule versus England (`non-overlap => different`, `overlap => similar`).
3. If CI missing, use a conservative threshold rule and mark result as `derived`.
- For polarity `99`, treat `Lower/Higher` as neutral labels unless an explicit indicator-level direction mapping exists.

## 4) What is the preferred report format for delivery (markdown, HTML, PDF, email body)?

| Option | What this means | Pros | Risks |
|---|---|---|---|
| A | Markdown only | Easy generation and versioning | Not ideal for non-technical readers |
| B | HTML primary | Best accessibility and web readability | Needs template styling |
| C | PDF primary | Familiar for board packs | Accessibility burden and maintenance overhead |
| D | Email-body primary | Fast circulation | Poor structure for long report content |

Warwickshire considerations:
- Public-sector guidance recommends HTML wherever possible for accessibility, with PDF as a last resort.

Recommendation:
- Use HTML as primary delivery.
- Keep Markdown as canonical source artifact.
- Generate PDF only when specifically required for formal packs.
- Send short email summaries linking to the HTML report.

## 5) What review/approval step is required before report sections are shared with Public Health teams?

| Option | What this means | Pros | Risks |
|---|---|---|---|
| A | Fully automated publish | Fastest | Highest governance and trust risk |
| B | One analyst review | Better quality control | Single-point dependency |
| C | Two-stage review and sign-off | Strong governance and auditability | More process overhead |

Warwickshire considerations:
- Local governance constraints in this repo already require dissemination only to approved PH staff.
- UK government analysis quality guidance favors proportionate QA before release.

Recommendation:
- Adopt option C:
1. Automated QA gate (schema checks, missingness thresholds, benchmark/trend sanity checks).
2. Analyst review and annotations.
3. Named approver sign-off (PH Intelligence lead or delegated consultant in Public Health).
4. Dissemination only after approved status is recorded.

## 6) What cadence should routine reporting run on, and what triggers on-demand runs?

| Option | What this means | Pros | Risks |
|---|---|---|---|
| A | Daily | Responsive | Usually unnecessary for many indicators |
| B | Weekly | Balanced timeliness and effort | Can miss same-day urgent requests |
| C | Monthly | Low overhead | Slower issue detection |
| D | Event-driven only | Efficient compute use | Requires robust trigger logic |

Warwickshire considerations:
- Fingertips exposes `data_changes/all_indicators` and `data_changes_and_updates/by_indicator_ids` so jobs can detect updates.
- Recent PHOF sample data shows batched publication updates rather than continuous daily updates.

Recommendation:
- Primary cadence: weekly scheduled run.
- Triggered runs: on-demand by analyst request and optional auto-run when `data_changes` detects relevant updates.
- Add a monthly consolidated digest for senior stakeholders.

## 7) Which stakeholder groups map to which Fingertips profiles for highlighted sections?

| Option | What this means | Pros | Risks |
|---|---|---|---|
| A | One shared profile set for all groups | Simple governance | Lower relevance per team |
| B | Theme-based routing by stakeholder group | Most actionable, matches Warwickshire themes | Needs maintained mapping table |
| C | Manual mapping each run | Flexible | High analyst burden |

Warwickshire considerations:
- Warwickshire public health pages and JSNA topics are strongly theme-based (for example mental health, wider determinants, children and young people, alcohol, healthy ageing).

Recommendation:
- Adopt option B with this initial routing map.
- Public Health Intelligence core: `public-health-outcomes-framework`, `health-profiles`, `mortality-profile`, `populations`.
- Health Improvement: `tobacco-control`, `obesity-physical-activity-nutrition`, `local-alcohol-profiles`, `sexualhealth`, `nhs-health-check-detailed`.
- Health Protection: `health-protection`, `tb-monitoring`, `amr-local-indicators`.
- Children and Young People: `child-health-profiles`, `perinatal-cyp-mental-health`.
- Mental Health and Wellbeing: `adult-mental-health-wellbeing`, `suicide-prevention`, `dementia`.
- Wider Determinants and Inequalities: `wider-determinants`, `inequality-tools`, `local-health`.
- Long-term Conditions and Prevention: `cardiovascular`, `diabetes-ft`, `cardiovascular-disease-diabetes-kidney-disease`, `respiratory-disease`, `msk`, `liver-disease`.

## Suggested default decisions for implementation

1. Endpoint set: Q1 option A.
2. Warwickshire areas: Q2 option C with fixed baseline codes listed above.
3. Better/worse logic: Q3 option D hybrid precedence.
4. Report delivery: Q4 option B with Markdown source and optional PDF.
5. Approval flow: Q5 option C two-stage review.
6. Cadence/triggers: Q6 option B weekly + trigger-based on-demand.
7. Stakeholder routing: Q7 option B theme-based mapping.

## Sources

- Fingertips API Swagger `v1`: https://fingertips.phe.org.uk/swagger/docs/v1
- Fingertips API explorer: https://fingertips.phe.org.uk/api
- Fingertips profile by key example: https://fingertips.phe.org.uk/api/profile/by_key?profile_key=public-health-outcomes-framework
- Fingertips Warwickshire child areas example: https://fingertips.phe.org.uk/api/areas/by_parent_area_code?area_type_id=501&parent_area_code=E10000031&profile_id=19
- Fingertips comparator significance example: https://fingertips.phe.org.uk/api/comparator_significances?polarity_id=99
- Fingertips data updates endpoint: https://fingertips.phe.org.uk/api/data_changes_and_updates/by_indicator_ids
- Warwickshire health and wellbeing: https://www.warwickshire.gov.uk/health-wellbeing
- Warwickshire strategy and governance (health and wellbeing): https://www.warwickshire.gov.uk/healthgovernance
- Warwickshire JSNA hub: https://www.warwickshire.gov.uk/jsna
- GOV.UK publishing accessible documents: https://www.gov.uk/guidance/publishing-accessible-documents
- GSS quality assurance of administrative data: https://www.gov.uk/government/publications/quality-assurance-of-administrative-data-qaad
