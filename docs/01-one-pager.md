# Cyber Risk Quantifier — One-Pager

**Author:** Mridhul Jose
**Date:** [today's date]
**Status:** Draft v1.0

## Problem
Most security teams report cyber risk using qualitative ratings (High / Medium / Low).
CFOs and boards cannot make budget decisions on color-coded heatmaps. As a result,
security spend is either over-funded based on fear or under-funded based on
under-communication, and the ROI of specific controls (MFA, EDR, phishing training)
is invisible.

## Opportunity
The FAIR (Factor Analysis of Information Risk) framework translates qualitative risk
into probability distributions of dollar losses using Monte Carlo simulation. A
lightweight, web-based implementation lets practitioners model their environment
in minutes instead of weeks of consultant engagement.

## Proposed Solution
A web application that accepts a handful of calibrated inputs (threat frequency,
control strength, loss magnitudes) and outputs:
- Annual Loss Expectancy distribution (P50 / P90 / P95 / P99)
- Side-by-side comparison of control scenarios (e.g., with vs. without MFA)
- Exportable executive summary for board and audit use

## Target Users
- GRC analysts preparing risk registers
- Security engineers justifying control investments
- CISOs presenting to boards
- Cyber insurance underwriters validating self-attested risk

## Success Metrics
- Users can produce a credible loss distribution in under 10 minutes
- Outputs align within ±15% of reference FAIR case studies
- Deployed publicly with zero ongoing cost

## Risks & Assumptions
- **Calibration risk**: outputs are only as good as input estimates
- **Methodology risk**: FAIR does not model novel risks (zero-days, nation-state)
- **Assumption**: users have basic knowledge of their environment; this is a
  quantification aid, not a threat intelligence tool

## Out of Scope (v1)
- Integration with SIEM/EDR for live telemetry
- Multi-user collaboration
- Historical trend tracking
- Custom framework support (NIST RMF, ISO 27005)