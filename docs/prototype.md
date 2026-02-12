# Live Prototype: Fingertips API

## Objective
Build an initial live-data prototype that classifies indicators into:
- requiring focus
- doing well

for Warwickshire and Warwickshire lower-tier districts/boroughs.

## API endpoints used
- `GET /api/profile/by_key`
- `GET /api/group_metadata`
- `GET /api/indicator_metadata/by_group_id`
- `GET /api/areas/by_parent_area_code`
- `GET /api/comparator_significances`
- `GET /api/latest_data/specific_indicators_for_child_areas`
- `GET /api/latest_data/specific_indicators_for_single_area`

## Default prototype configuration
- Profile key: `public-health-outcomes-framework`
- Warwickshire code: `E10000031`
- Child area type: `501` (lower tier local authorities, post 4/23)
- Warwickshire area type: `502` (upper tier local authorities, post 4/23)
- England area code/type: `E92000001` / `15`

## Classification logic
- Benchmark vs England:
  - Uses `Sig[4]` (comparator `4 = England`) from latest data rows.
  - Maps comparator significance labels from `comparator_significances`.
  - Fallback: if `Sig[4]` is unavailable, compares local and England confidence intervals (`LoCI`/`UpCI`) with polarity-aware interpretation.
- Trend direction:
  - Uses `RecentTrends[area_code].Marker`.
  - Falls back to `MarkerForMostRecentValueComparedWithPreviousValue`.
  - Applies polarity-aware mapping:
    - polarity `1`: marker `1` improving, `2` worsening
    - polarity `0`: marker `1` worsening, `2` improving

## Run
```bash
scripts/run_live_prototype.sh assets/output/live-prototype 120
```

## Current prototype limitations
- `--max-indicators 0` means full profile coverage; positive values cap runtime.
- Indicators that lack England value for a given demographic split are skipped.
- `BOB` polarity labels (`Lower`/`Higher`) are currently treated as similar to England in benchmark classification.
- API calls now include retry/backoff for timeout, HTTP 429, and HTTP 5xx responses.
