# Fingertips API Intro Tutorial for Fingertips Consol

This tutorial is for new users of this repository.
It explains:

- what the Fingertips API is
- how the API is structured
- how this repo uses it for Warwickshire monitoring
- where the platform has come from, and where it is going

It is based on:

- `docs/ideas.md` (product intent)
- `docs/specification.md` (monitoring objectives)
- `PROGRESS.md` and `CONTEXT.md` (current implementation status)
- official Fingertips API/guidance sources listed at the end

## 1. What We Are Building in This Repo

The target workflow in this project is:

1. Pull indicator data for Warwickshire and Warwickshire districts/boroughs.
2. Classify each indicator by:
   - trend (`improving`, `worsening`, `stable`)
   - benchmark vs England (`better`, `worse`, `similar`)
3. Produce two reports:
   - indicators requiring focus
   - indicators doing well

This maps directly to your ideas/specification files.

## 2. Fingertips API: Design and Function

### 2.1 Entry points

- Human API explorer: `https://fingertips.phe.org.uk/api`
- Swagger JSON (machine-readable): `https://fingertips.phe.org.uk/swagger/docs/v1`

The Swagger currently advertises 113 paths, grouped into:

- Areas
- Data
- Entities
- IndicatorMetadata
- Profiles

### 2.2 Core identifier model

Most requests are built around these IDs/codes:

- `profile_id` / `profile_key`: profile selection
- `group_id`: domain/topic inside a profile
- `indicator_id`: metric
- `area_type_id` + `area_code`: geography
- `parent_area_code`: roll-up context (for child area calls)

The official API guide and annex describe this ID-first model in detail.

### 2.3 Data retrieval patterns that matter for this repo

For this repo's prototype, the key live endpoints are:

- `GET /api/profile/by_key`
- `GET /api/group_metadata`
- `GET /api/indicator_metadata/by_group_id`
- `GET /api/areas/by_parent_area_code`
- `GET /api/comparator_significances`
- `GET /api/latest_data/specific_indicators_for_child_areas`
- `GET /api/latest_data/specific_indicators_for_single_area`

Important behavior:

- Some API endpoints return JSON.
- Some endpoints return CSV (for example under `/api/all_data/csv/...`).
- Trend and benchmark semantics are encoded values; they are not plain-language fields.

### 2.4 Trend and benchmark semantics

For benchmark classification:

- England comparator is `4`.
- In many data payloads, benchmark status appears under `Sig["4"]`.
- You map those significance codes using `GET /api/comparator_significances?polarity_id=...`.

For trend classification:

- `GET /api/recent_trends/for_child_areas` returns trend markers by area code.
- Marker meaning depends on indicator polarity.
- Polarity is discoverable from data payloads and from `GET /api/polarities`.

## 3. Warwickshire Onboarding Walkthrough

### 3.1 Find your profile

```bash
curl -sS 'https://fingertips.phe.org.uk/api/profile/by_key?profile_key=public-health-outcomes-framework' | jq
```

### 3.2 Resolve Warwickshire areas dynamically

```bash
curl -sS 'https://fingertips.phe.org.uk/api/areas/by_parent_area_code?area_type_id=501&parent_area_code=E10000031' | jq
```

This returns the 5 district/borough codes under Warwickshire:

- `E07000218` North Warwickshire
- `E07000219` Nuneaton and Bedworth
- `E07000220` Rugby
- `E07000221` Stratford-on-Avon
- `E07000222` Warwick

### 3.3 Pull latest data for one indicator

Example for one indicator (`92443`) and Warwickshire county code (`E10000031`):

```bash
curl -sS 'https://fingertips.phe.org.uk/api/latest_data/specific_indicators_for_single_area?area_type_id=502&area_code=E10000031&indicator_ids=92443&restrict_to_profile_ids=19' | jq
```

For district/borough child areas:

```bash
curl -sS 'https://fingertips.phe.org.uk/api/latest_data/specific_indicators_for_child_areas?area_type_id=501&parent_area_code=E10000031&indicator_ids=92443&profile_id=19' | jq
```

### 3.4 Pull trend markers for the same split

```bash
curl -sS 'https://fingertips.phe.org.uk/api/recent_trends/for_child_areas?parent_area_code=E10000031&group_id=1000042&area_type_id=501&indicator_id=92443&sex_id=4&age_id=168&year_range=1' | jq
```

## 4. Using the Tools in This Repo

### 4.1 Mode A: local JSON input (stable scaffold mode)

```bash
.venv/bin/python -m fingertips_consol.cli \
  --input assets/sample-indicators.json \
  --output-dir assets/output
```

### 4.2 Mode B: live prototype against Fingertips API

```bash
.venv/bin/python -m fingertips_consol.cli \
  --live-prototype \
  --output-dir assets/output/live-prototype \
  --max-indicators 120
```

Equivalent helper:

```bash
scripts/run_live_prototype.sh assets/output/live-prototype 120
```

Live prototype defaults:

- profile key: `public-health-outcomes-framework`
- parent area code: `E10000031` (Warwickshire)
- child area type: `501` (Districts & UAs from April 2023)
- parent area type: `502` (Counties & UAs from April 2023)
- England area code: `E92000001`

Outputs:

- `focus-report.md`
- `doing-well-report.md`

## 5. History and Direction of the API

### 5.1 History (confirmed from official materials)

- The official "An introduction to using Fingertips API" guide lists:
  - version `1.0` in June 2021
  - version `1.1` in June 2023 (minor changes)
- The Fingertips ecosystem has established client libraries:
  - `fingertipsR` repository created in 2017 and actively maintained
  - `fingertips_py` repository created in 2019 and currently active

### 5.2 Current platform state (December 2025 update)

The Fingertips "New service updates" page reports:

- stability/resilience work on servers
- changed API validation behavior
- API and website rate limiting to protect service performance
- continued publication on current Fingertips until replacement launch

### 5.3 Future direction

The same update states the planned direction is:

- a new public health data service on GOV.UK
- migration guidance and regular updates during transition
- ongoing user research feedback feeding service design

For this repo, that means abstraction around endpoint contracts is essential.

## 6. Practical Guidance for New Users of This Repo

1. Do not hardcode profile/group/indicator lookup tables unless absolutely necessary.
2. Resolve profile/group/indicator metadata from live endpoints each run (or cache with expiry).
3. Treat area types as versioned entities (`301/302` vs `501/502` generations).
4. Expect intermittent rate limiting and build retry/backoff in production ingestion.
5. Keep trend and benchmark mapping logic explicit and testable.
6. Track open decisions in `docs/open-questions.md` before production rollout.

## 7. Source Links

- Fingertips API page: [https://fingertips.phe.org.uk/api](https://fingertips.phe.org.uk/api)
- Swagger/OpenAPI JSON: [https://fingertips.phe.org.uk/swagger/docs/v1](https://fingertips.phe.org.uk/swagger/docs/v1)
- Fingertips API guidance page: [https://fingertips.phe.org.uk/profile/guidance/supporting-information/api](https://fingertips.phe.org.uk/profile/guidance/supporting-information/api)
- API guide PDF: [https://fingertips.phe.org.uk/documents/fingertips_api_guide.pdf](https://fingertips.phe.org.uk/documents/fingertips_api_guide.pdf)
- API annex (ODS): [https://fingertips.phe.org.uk/documents/api_annex.ods](https://fingertips.phe.org.uk/documents/api_annex.ods)
- New service updates: [https://fingertips.phe.org.uk/profile/guidance/supporting-information/new-service](https://fingertips.phe.org.uk/profile/guidance/supporting-information/new-service)
- Geography guidance/changelog: [https://fingertips.phe.org.uk/profile/guidance/supporting-information/geochangelog](https://fingertips.phe.org.uk/profile/guidance/supporting-information/geochangelog)
- Public health methods guidance: [https://fingertips.phe.org.uk/profile/guidance/supporting-information/ph-methods](https://fingertips.phe.org.uk/profile/guidance/supporting-information/ph-methods)
- `fingertipsR` repository: [https://github.com/ropensci/fingertipsR](https://github.com/ropensci/fingertipsR)
- `fingertips_py` docs: [https://fingertips-py.readthedocs.io/en/latest/](https://fingertips-py.readthedocs.io/en/latest/)
- `fingertips_py` repository: [https://github.com/dhsc-govuk/fingertips_py](https://github.com/dhsc-govuk/fingertips_py)
