# Product Requirements Document — Cyber Risk Quantifier

**Author:** Mridhul Jose
**Version:** 1.0
**Status:** Approved for Development

## 1. Background
[Paste the Problem and Opportunity sections from the one-pager]

## 2. Goals
### Primary Goals
- G1: Enable a user to produce a FAIR-compliant annual loss distribution in one session
- G2: Enable side-by-side comparison of up to 3 control scenarios
- G3: Ship a live, publicly accessible version with no backend infrastructure cost

### Non-Goals
- Not building a replacement for RiskLens or Archer
- Not offering customer-specific consulting
- Not storing user data (stateless by design)

## 3. Personas

### Persona 1 — Priya, GRC Analyst
- 2 years in compliance, CISA certification in progress
- Builds quarterly risk reports for leadership
- Frustrated with qualitative risk language; wants defensible dollar figures
- Needs: fast input, credible methodology, exportable output

### Persona 2 — Marcus, Security Engineer
- 5 years hands-on, evaluating whether to push for EDR budget
- Needs to make a dollar-denominated case to his CISO
- Needs: control scenario comparison, clean executive chart

### Persona 3 — Dana, CISO
- Reports to the board quarterly
- Needs: one-slide summary with P95 loss figures and recommended controls

## 4. Functional Requirements

### FR-1 — Input Collection
The system shall collect the following FAIR inputs as PERT triplets (min, most likely, max):
- Threat Event Frequency (events per year)
- Vulnerability (probability 0–1)
- Primary Loss Magnitude (USD)
- Secondary Loss Event Frequency (probability 0–1)
- Secondary Loss Magnitude (USD)

### FR-2 — Simulation
The system shall run 50,000 Monte Carlo iterations per scenario, completing in
under 3 seconds on standard consumer hardware.

### FR-3 — Output Display
The system shall display:
- Summary table with Mean, P50, P90, P95, P99
- Histogram of annual loss distribution
- Loss Exceedance Curve (probability of exceeding various loss thresholds)

### FR-4 — Control Scenario Comparison
The user shall be able to define up to 3 named scenarios, each with independent inputs,
and compare results side-by-side.

### FR-5 — Presets
The system shall offer industry presets (Financial Services, Healthcare, Retail, SMB)
that prefill realistic input ranges sourced from Verizon DBIR and Ponemon reports.

### FR-6 — Export
The user shall be able to export results as PDF containing summary metrics, charts,
methodology notes, and scenario inputs.

## 5. Non-Functional Requirements

### NFR-1 — Performance
- Simulation completes in < 3s for 50k iterations
- Page initial load < 2s on 3G

### NFR-2 — Reliability
- 99.5% uptime (acceptable for Streamlit Cloud free tier)

### NFR-3 — Security
- No PII collected, no backend database
- HTTPS enforced
- No third-party analytics that could leak user inputs

### NFR-4 — Usability
- First-time user reaches a complete simulation result within 10 minutes
- Tooltips explain every FAIR term

### NFR-5 — Accessibility
- WCAG 2.1 AA color contrast on all charts

## 6. Acceptance Criteria
Each functional requirement maps to user-story-level acceptance criteria in
`03-user-stories.md`.

## 7. Release Plan
- **v0.1 (MVP)**: FR-1, FR-2, FR-3 — working single-scenario simulation
- **v0.2**: FR-4 — scenario comparison
- **v0.3**: FR-5, FR-6 — presets and export
- **v1.0**: All NFRs validated, public launch