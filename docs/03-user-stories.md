# User Stories & Use Cases — Cyber Risk Quantifier

## Format
All stories use: "As a [persona], I want [capability] so that [benefit]."
Each has acceptance criteria in Given/When/Then format.

---

## US-001 — Run a Baseline Simulation
**As a** GRC analyst (Priya)
**I want to** enter my organization's threat and loss estimates
**So that** I can produce a defensible annual loss figure for my risk register.

### Acceptance Criteria
- **Given** I am on the main page
- **When** I enter valid values for all 5 FAIR inputs and click "Run Simulation"
- **Then** I see a summary table with Mean, P50, P90, P95, P99 within 3 seconds
- **And** I see a histogram of the loss distribution
- **And** the histogram displays P95 as a marked vertical line

---

## US-002 — Use an Industry Preset
**As a** security engineer (Marcus) new to FAIR
**I want to** start from pre-calibrated industry defaults
**So that** I don't have to guess at initial values.

### Acceptance Criteria
- Given the input panel is empty
- When I select "Financial Services" from the preset dropdown
- Then all 5 FAIR inputs populate with realistic ranges
- And a caption notes the data source (e.g., "Based on Verizon DBIR 2024, Finance sector")

---

## US-003 — Compare Control Scenarios
**As a** security engineer (Marcus)
**I want to** compare annual loss with and without a specific control
**So that** I can calculate ROI for a proposed investment.

### Acceptance Criteria
- Given I have run a baseline simulation
- When I click "Add scenario" and enter reduced vulnerability values
- And I click "Run comparison"
- Then I see both scenarios' P95 values side-by-side
- And I see the dollar-value difference labeled as "Risk Reduction"

---

## US-004 — Export an Executive Summary
**As a** CISO (Dana)
**I want to** download a one-page PDF summary
**So that** I can present it to the board without recreating the analysis.

### Acceptance Criteria
- Given I have completed at least one simulation
- When I click "Export PDF"
- Then a PDF downloads containing: title, input summary, results table, histogram,
  and a methodology footnote

---

## US-005 — Understand the Methodology
**As a** new user
**I want to** see explanations of each input field and the math behind it
**So that** I can trust the outputs and explain them to my leadership.

### Acceptance Criteria
- Every input field has a hover tooltip defining the term
- A "Methodology" link in the footer opens a plain-language explanation of FAIR and Monte Carlo
- Limitations of the model are explicitly listed

---

## Use Case Flows

### UC-A — First-Time User Produces Their First Risk Estimate
**Primary actor:** Priya (GRC Analyst, new to FAIR)
**Preconditions:** User has arrived at the app URL.
**Main flow:**
1. User lands on the main page and reads the 2-sentence intro
2. User clicks "Load Example: Financial Services" preset
3. App populates all 5 inputs with sample ranges
4. User clicks "Run Simulation"
5. App displays summary table and histogram within 3 seconds
6. User reads tooltips to understand the meaning of P95
7. User adjusts her threat frequency input to match her org's actuals
8. User re-runs simulation
9. User clicks "Export PDF"
10. User receives a PDF suitable for her risk register

**Alternative flows:**
- 4a. If any input is invalid (e.g., min > max), app displays inline validation error
- 5a. If simulation fails, app displays error with guidance, logs nothing PII

---

### UC-B — Engineer Builds ROI Case for EDR Investment
**Primary actor:** Marcus (Security Engineer)
**Preconditions:** Marcus has baseline numbers for his environment.
**Main flow:**
1. Marcus enters baseline scenario inputs and runs simulation → sees P95 = $4.2M
2. Marcus clicks "Add scenario: With EDR"
3. Marcus reduces vulnerability inputs (EDR is expected to cut success rate 60%)
4. Marcus clicks "Run comparison"
5. App shows baseline P95 = $4.2M vs. with-EDR P95 = $1.7M → $2.5M risk reduction
6. Marcus notes EDR annual cost is $200K → presents 12.5× ROI to CISO
7. Marcus exports the PDF for the budget meeting