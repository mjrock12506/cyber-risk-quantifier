"""
app.py — Cyber Risk Quantifier UI
Streamlit frontend for the FAIR Monte Carlo engine.
"""

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from simulation import run_fair_simulation
from presets import PRESETS
from questionnaire import build_fair_inputs
from report import generate_report
from data_analyzer import analyze_data


# --- Page config ---
st.set_page_config(page_title="Cyber Risk Quantifier", layout="wide")
st.title("Cyber Risk Quantifier (FAIR)")
st.caption("Quantify annual cyber loss exposure using Monte Carlo simulation")


# --- Input method selector ---
st.sidebar.header("How do you want to start?")
input_method = st.sidebar.radio(
    "Choose input method:",
    ["Industry Preset", "Answer Questions", "Upload Your Data", "Manual Entry"],
    help="Preset = quick start. Questions = tailored to you. Upload = use your real data. Manual = full control."
)

# --- Method 1: Presets ---
if input_method == "Industry Preset":
    preset_name = st.sidebar.selectbox("Choose industry:", list(PRESETS.keys()))
    if PRESETS[preset_name] is not None:
        p = PRESETS[preset_name]
        st.sidebar.info(p["source"])
        d_tef = p["tef"]
        d_vuln = p["vuln"]
        d_pl = p["pl"]
        d_slef = p["slef"]
        d_sl = p["sl"]
    else:
        d_tef = (500, 2000, 10000)
        d_vuln = (0.001, 0.010, 0.050)
        d_pl = (50000, 250000, 2000000)
        d_slef = (0.05, 0.20, 0.50)
        d_sl = (100000, 1500000, 20000000)

# --- Method 2: Questionnaire ---
elif input_method == "Answer Questions":
    st.sidebar.subheader("Tell us about your organization")

    org_name = st.sidebar.text_input("Organization name:", value="My Organization")

    industry = st.sidebar.selectbox("What industry?",
        ["healthcare", "finance", "retail", "other"])

    employees = st.sidebar.number_input("How many employees?",
        min_value=1, max_value=100000, value=200)

    st.sidebar.subheader("What security controls do you have?")
    has_mfa = st.sidebar.checkbox("Multi-Factor Authentication (MFA)")
    has_edr = st.sidebar.checkbox("Endpoint Detection & Response (EDR)")
    has_training = st.sidebar.checkbox("Security Awareness Training")
    had_incident = st.sidebar.checkbox("Had a security incident in the past year")

    answers = {
        "industry": industry,
        "employees": employees,
        "has_mfa": has_mfa,
        "has_edr": has_edr,
        "has_training": has_training,
        "had_incident": had_incident,
    }
    q_result = build_fair_inputs(answers)
    st.sidebar.success(q_result["reasoning"])

    d_tef = q_result["tef"]
    d_vuln = q_result["vuln"]
    d_pl = q_result["pl"]
    d_slef = q_result["slef"]
    d_sl = q_result["sl"]

# --- Method 3: Upload Data ---
elif input_method == "Upload Your Data":
    st.sidebar.subheader("Upload incident or security data")
    st.sidebar.caption(
        "Upload a CSV or Excel file with your incident data. "
        "The tool will detect columns like date, cost, severity, "
        "status and calculate your FAIR inputs automatically."
    )

    uploaded_file = st.sidebar.file_uploader(
        "Choose a file:", type=["csv", "xlsx", "xls"]
    )

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.sidebar.success(f"Loaded {len(df)} rows, {len(df.columns)} columns")

            analysis = analyze_data(df)

            st.sidebar.subheader("What we found:")
            for finding in analysis["findings"]:
                st.sidebar.write(f"- {finding}")

            detected = analysis["columns_detected"]
            missed = analysis["columns_missed"]
            if detected:
                st.sidebar.info(f"Columns matched: {', '.join(detected.values())}")
            if missed:
                st.sidebar.warning(f"Could not detect: {', '.join(missed)}")

            fi = analysis["fair_inputs"]
            d_tef = fi["tef"]
            d_vuln = fi["vuln"]
            d_pl = fi["pl"]
            d_slef = fi["slef"]
            d_sl = fi["sl"]

            st.subheader("Uploaded Data Preview")
            st.dataframe(df.head(20))

        except Exception as e:
            st.sidebar.error(f"Error reading file: {str(e)}")
            d_tef = (500, 2000, 10000)
            d_vuln = (0.001, 0.010, 0.050)
            d_pl = (50000, 250000, 2000000)
            d_slef = (0.05, 0.20, 0.50)
            d_sl = (100000, 1500000, 20000000)
    else:
        d_tef = (500, 2000, 10000)
        d_vuln = (0.001, 0.010, 0.050)
        d_pl = (50000, 250000, 2000000)
        d_slef = (0.05, 0.20, 0.50)
        d_sl = (100000, 1500000, 20000000)

# --- Method 4: Manual ---
else:
    d_tef = (500, 2000, 10000)
    d_vuln = (0.001, 0.010, 0.050)
    d_pl = (50000, 250000, 2000000)
    d_slef = (0.05, 0.20, 0.50)
    d_sl = (100000, 1500000, 20000000)


# --- Detailed inputs (always shown, pre-filled by chosen method) ---
st.sidebar.markdown("---")
st.sidebar.header("FAIR Inputs (adjust if needed)")

st.sidebar.subheader("Threat Event Frequency")
st.sidebar.caption("Attack attempts per year")
tef_low = st.sidebar.number_input("TEF Min", value=float(d_tef[0]))
tef_mode = st.sidebar.number_input("TEF Most Likely", value=float(d_tef[1]))
tef_high = st.sidebar.number_input("TEF Max", value=float(d_tef[2]))

st.sidebar.subheader("Vulnerability")
st.sidebar.caption("Probability each attempt succeeds (0 to 1)")
vuln_low = st.sidebar.number_input("Vuln Min", value=float(d_vuln[0]), format="%.4f")
vuln_mode = st.sidebar.number_input("Vuln Most Likely", value=float(d_vuln[1]), format="%.4f")
vuln_high = st.sidebar.number_input("Vuln Max", value=float(d_vuln[2]), format="%.4f")

st.sidebar.subheader("Primary Loss (USD)")
st.sidebar.caption("Direct cost per breach")
pl_low = st.sidebar.number_input("PL Min", value=float(d_pl[0]))
pl_mode = st.sidebar.number_input("PL Most Likely", value=float(d_pl[1]))
pl_high = st.sidebar.number_input("PL Max", value=float(d_pl[2]))

st.sidebar.subheader("Secondary Loss Event Frequency")
st.sidebar.caption("Probability breach triggers fines/lawsuits (0 to 1)")
slef_low = st.sidebar.number_input("SLEF Min", value=float(d_slef[0]), format="%.2f")
slef_mode = st.sidebar.number_input("SLEF Most Likely", value=float(d_slef[1]), format="%.2f")
slef_high = st.sidebar.number_input("SLEF Max", value=float(d_slef[2]), format="%.2f")

st.sidebar.subheader("Secondary Loss Magnitude (USD)")
st.sidebar.caption("Cost of fines, settlements, churn")
sl_low = st.sidebar.number_input("SL Min", value=float(d_sl[0]))
sl_mode = st.sidebar.number_input("SL Most Likely", value=float(d_sl[1]))
sl_high = st.sidebar.number_input("SL Max", value=float(d_sl[2]))


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

    # --- Percentiles table ---
    st.subheader("Detailed Percentiles")
    percentiles = [10, 25, 50, 75, 90, 95, 99]
    data = {f"P{p}": [f"${np.percentile(losses, p):,.0f}"] for p in percentiles}
    st.dataframe(data)

    # --- Executive report ---
    org = org_name if input_method == "Answer Questions" else "Your Organization"
    report_text, risk_level, risk_color = generate_report(result, org)
    st.markdown("---")
    st.markdown(report_text)