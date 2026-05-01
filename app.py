"""
app.py — Cyber Risk Quantifier UI
Streamlit frontend for the FAIR Monte Carlo engine.
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from simulation import run_fair_simulation


# --- Page config ---
st.set_page_config(page_title="Cyber Risk Quantifier", layout="wide")
st.title("Cyber Risk Quantifier (FAIR)")
st.caption("Quantify annual cyber loss exposure using Monte Carlo simulation")


# --- Sidebar inputs ---
st.sidebar.header("FAIR Inputs")
st.sidebar.markdown("Enter min, most likely, and max for each variable.")

st.sidebar.subheader("Threat Event Frequency")
st.sidebar.caption("How many threat attempts per year?")
tef_low = st.sidebar.number_input("TEF Min", value=500)
tef_mode = st.sidebar.number_input("TEF Most Likely", value=2000)
tef_high = st.sidebar.number_input("TEF Max", value=10000)

st.sidebar.subheader("Vulnerability")
st.sidebar.caption("Probability each attempt succeeds (0 to 1)")
vuln_low = st.sidebar.number_input("Vuln Min", value=0.001, format="%.4f")
vuln_mode = st.sidebar.number_input("Vuln Most Likely", value=0.010, format="%.4f")
vuln_high = st.sidebar.number_input("Vuln Max", value=0.050, format="%.4f")

st.sidebar.subheader("Primary Loss (USD)")
st.sidebar.caption("Direct cost per breach: IR, downtime, forensics")
pl_low = st.sidebar.number_input("PL Min", value=50000)
pl_mode = st.sidebar.number_input("PL Most Likely", value=250000)
pl_high = st.sidebar.number_input("PL Max", value=2000000)

st.sidebar.subheader("Secondary Loss Event Frequency")
st.sidebar.caption("Probability a breach triggers fines/lawsuits (0 to 1)")
slef_low = st.sidebar.number_input("SLEF Min", value=0.05, format="%.2f")
slef_mode = st.sidebar.number_input("SLEF Most Likely", value=0.20, format="%.2f")
slef_high = st.sidebar.number_input("SLEF Max", value=0.50, format="%.2f")

st.sidebar.subheader("Secondary Loss Magnitude (USD)")
st.sidebar.caption("Cost of fines, settlements, customer churn")
sl_low = st.sidebar.number_input("SL Min", value=100000)
sl_mode = st.sidebar.number_input("SL Most Likely", value=1500000)
sl_high = st.sidebar.number_input("SL Max", value=20000000)


# --- Run simulation ---
if st.button("Run 50,000 Simulations", type="primary"):
    result = run_fair_simulation(
        tef_low, tef_mode, tef_high,
        vuln_low, vuln_mode, vuln_high,
        pl_low, pl_mode, pl_high,
        slef_low, slef_mode, slef_high,
        sl_low, sl_mode, sl_high,
    )

    # --- Summary metrics ---
    st.subheader("Annual Loss Exposure")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Median (P50)", f"${result.p50:,.0f}")
    col2.metric("Bad Year (P90)", f"${result.p90:,.0f}")
    col3.metric("Severe (P95)", f"${result.p95:,.0f}")
    col4.metric("Disaster (P99)", f"${result.p99:,.0f}")

    st.metric("Average Breaches per Year", f"{result.breach_rate:.1f}")

    # --- Histogram ---
    st.subheader("Loss Distribution")
    losses = result.raw_losses
    nonzero = losses[losses > 0]

    if len(nonzero) > 0:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.hist(nonzero, bins=80, color="#4A90D9", edgecolor="white", alpha=0.85)
        ax.axvline(result.p95, color="red", linestyle="--", linewidth=2, label=f"P95: ${result.p95:,.0f}")
        ax.axvline(result.p50, color="green", linestyle="--", linewidth=2, label=f"P50: ${result.p50:,.0f}")
        ax.set_xlabel("Annual Loss (USD)")
        ax.set_ylabel("Frequency")
        ax.legend()
        ax.set_title("Monte Carlo Simulation — Annual Cyber Loss Distribution")
        st.pyplot(fig)
    else:
        st.info("No breaches occurred in any simulation. Your controls are very strong!")

    # --- Raw percentiles table ---
    st.subheader("Detailed Percentiles")
    percentiles = [10, 25, 50, 75, 90, 95, 99]
    data = {f"P{p}": [f"${np.percentile(losses, p):,.0f}"] for p in percentiles}
    st.dataframe(data)