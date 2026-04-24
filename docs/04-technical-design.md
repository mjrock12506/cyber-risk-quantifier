# Technical Design Document — Cyber Risk Quantifier

**Author:** Mridhul Jose
**Status:** Approved for Implementation
**Reviewers:** (self-review)

## 1. Summary
A single-page Streamlit web application that runs Monte Carlo simulations of the
FAIR risk model in the browser-facing server process. Stateless; no database.

## 2. Context & Motivation
[Pulls from the PRD Goals section]

## 3. Non-Goals
- Multi-tenant data persistence
- Real-time collaboration
- Integration with external risk feeds

## 4. Proposed Design

### 4.1 High-Level Architecture
User browser  →  Streamlit Cloud  →  Python process (NumPy + Streamlit)
No external services. No database. Stateless.

### 4.2 Components

**`app.py`** — Streamlit UI entry point. Renders sidebar inputs, invokes simulation,
displays results. No business logic beyond UI orchestration.

**`simulation.py`** — Pure Python module. Contains:
- `pert(low, mode, high, size)` — generates PERT samples
- `run_fair_simulation(inputs, n_sims)` — runs 50k-iteration Monte Carlo
- Returns a `SimulationResult` dataclass with raw samples, percentiles, and metadata

**`presets.py`** — Industry preset dictionaries (Finance, Healthcare, Retail, SMB)

**`export.py`** — PDF generation using `reportlab` or `matplotlib` PDF backend

**`data/dbir_references.md`** — Citations backing each preset's input ranges

### 4.3 Data Flow

1. User adjusts inputs in `st.sidebar`
2. User clicks "Run Simulation" button
3. `app.py` collects inputs, calls `run_fair_simulation(inputs, n_sims=50_000)`
4. `simulation.py` generates sample arrays, computes loss distribution
5. Returns `SimulationResult` to `app.py`
6. `app.py` renders: metric cards (`st.metric`), histogram (`matplotlib`), table (`st.dataframe`)

### 4.4 Key Algorithms

**PERT Sampling** (beta-distribution-based, λ=4 standard):