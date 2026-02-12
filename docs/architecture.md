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

## Planned extensions

- live API ingestion from Fingertips endpoints
- statistical significance handling using confidence intervals/period metadata
- analyst review state tracking and sign-off workflow
- controlled dissemination output channels
