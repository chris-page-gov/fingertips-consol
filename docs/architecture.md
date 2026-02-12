# Architecture Skeleton

## Layers

- `ingest/`: Fingertips API access and raw payload retrieval
- `analysis/`: trend and benchmark classification logic
- `reporting/`: report generation and split into focus vs doing-well outputs
- `notifications/`: group and prepare highlighted sections by profile/team
- `workflows/`: routine and on-demand orchestration

## Current data flow

1. Input payload is parsed into `IndicatorResult` records.
2. Records are split into focus and doing-well categories.
3. Two markdown reports are generated.

## Live prototype flow

1. Resolve profile and groups from Fingertips (`profile/by_key`, `group_metadata`).
2. Pull indicator metadata and latest values for:
   - Warwickshire districts (`child_area_type_id=501`)
   - Warwickshire county (`parent_area_type_id=502`)
   - England (`area_type_id=15`)
3. Classify benchmark using England comparator significance (`Sig[4]`).
4. Classify trend using `RecentTrends` markers with polarity-aware mapping.
5. Generate focus/doing-well markdown outputs.

## Planned extensions

- live API ingestion from Fingertips endpoints
- statistical significance handling using confidence intervals/period metadata
- analyst review state tracking and sign-off workflow
- controlled dissemination output channels
