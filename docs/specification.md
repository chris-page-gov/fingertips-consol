# Fingertips Analytics and Monitoring Specification (Draft)

## Purpose

Monitor public health indicators for Warwickshire and each district/borough to identify:

- trends in undesired direction
- trends in desired direction
- indicators statistically worse than England
- indicators statistically better than England

## Scope

- all available Fingertips indicators at Warwickshire and district/borough levels
- all Fingertips categories/profiles

## User Experience

Produce two reports:

- Indicators requiring focus
- Indicators doing well

## Data Source

- Fingertips API

## Workflow

1. Ingest Fingertips data.
2. Classify trend direction and England benchmark.
3. Produce routine and on-demand auto-generated reports.
4. Allow analyst review before broader dissemination.
5. Highlight relevant sections for Public Health teams.

## Governance constraints

- UK GDPR
- Data Protection Act 2018
- ONS PCMD sharing rules
- Local Authority / ICS governance
- Dissemination to approved PH staff only
