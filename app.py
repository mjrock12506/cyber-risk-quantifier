import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from simulation import run_fair_simulation
from presets import PRESETS
from questionnaire import build_fair_inputs
from report import generate_report
from data_analyzer import analyze_data

st.set_page_config(page_title="Cyber Risk Quantifier", layout="wide")
st.title("Cyber Risk Quantifier (FAIR)")
st.caption("Quantify annual cyber loss exposure using Monte Carlo simulation")

st.sidebar.header("How do you want to start?")
input_method = st.sidebar.radio(
    "Choose input method:",
    ["Industry Preset", "Answer Questions", "Upload Your Data", "Manual Entry"],
)

org_name = "Your Organization"

if input_method == "Industry Preset":
    preset_name = st.sidebar.selectbox("Choose industry:", list(PRESETS.keys()))
    if PRESETS[preset_name] is not None:
        p = PRESETS[preset_name]
        st.sidebar.info(p["source"])
        d_tef, d_vuln, d_pl = p["tef"], p["vuln"], p["pl"]
        d_slef, d_sl = p["slef"], p["sl"]
    else:
        d_tef, d_vuln = (500, 2000, 10000), (0.001, 0.010, 0.050)
        d_pl, d_slef = (50000, 250000, 2000000), (0.05, 0.20, 0.50)
        d_sl = (100000, 1500000, 20000000)
elif input_method == "Answer Questions":
    st.sidebar.subheader("Tell us about your organization")
    org_name = st.sidebar.text_input("Organization name:", value="My Organization")
    industry = st.sidebar.selectbox("What industry?", ["healthcare", "finance", "retail", "other"])
    employees = st.sidebar.number_input("How many employees?", min_value=1, max_value=100000, value=200)
    st.sidebar.subheader("What security controls do you have?")
    has_mfa = st.sidebar.checkbox("Multi-Factor Authentication (MFA)")
    has_edr = st.sidebar.checkbox("Endpoint Detection & Response (EDR)")
    has_training = st.sidebar.checkbox("Security Awareness Training")
    had_incident = st.sidebar.checkbox("Had a security incident in the past year")
    answers = {"industry": industry, "employees": employees, "has_mfa": has_mfa, "has_edr": has_edr, "has_training": has_training, "had_incident": had_incident}
    q_result = build_fair_inputs(answers)
    st.sidebar.success(q_result["reasoning"])
    d_tef, d_vuln, d_pl = q_result["tef"], q_result["vuln"], q_result["pl"]
    d_slef, d_sl = q_result["slef"], q_result["sl"]
elif input_method == "Upload Your Data":
    st.sidebar.subheader("Upload incident or security data")
    uploaded_file = st.sidebar.file_uploader("Choose a file:", type=["csv", "xlsx", "xls"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.sidebar.success(f"Loaded {len(df)} rows, {len(df.columns)} columns")
            analysis = analyze_data(df)
            for finding in analysis["findings"]:
                st.sidebar.write(f"- {finding}")
            fi = analysis["fair_inputs"]
            d_tef, d_vuln, d_pl = fi["tef"], fi["vuln"], fi["pl"]
            d_slef, d_sl = fi["slef"], fi["sl"]
            st.subheader("Uploaded Data Preview")
            st.dataframe(df.head(20))
        except Exception as e:
            st.sidebar.error(f"Error: {str(e)}")
            d_tef, d_vuln = (500, 2000, 10000), (0.001, 0.010, 0.050)
            d_pl, d_slef = (50000, 250000, 2000000), (0.05, 0.20, 0.50)
            d_sl = (100000, 1500000, 20000000)
    else:
        d_tef, d_vuln = (500, 2000, 10000), (0.001, 0.010, 0.050)
        d_pl, d_slef = (50000, 250000, 2000000), (0.05, 0.20, 0.50)
        d_sl = (100000, 1500000, 20000000)
else:
    d_tef, d_vuln = (500, 2000, 10000), (0.001, 0.010, 0.050)
    d_pl, d_slef = (50000, 250000, 2000000), (0.05, 0.20, 0.50)
    d_sl = (100000, 1500000, 20000000)

st.sidebar.markdown("---")
st.sidebar.header("FAIR Inputs (adjust if needed)")
tef_low = st.sidebar.number_input("TEF Min", value=float(d_tef[0]))
tef_mode = st.sidebar.number_input("TEF Most Likely", value=float(d_tef[1]))
tef_high = st.sidebar.number_input("TEF Max", value=float(d_tef[2]))
vuln_low = st.sidebar.number_input("Vuln Min", value=float(d_vuln[0]), format="%.4f")
vuln_mode = st.sidebar.number_input("Vuln Most Likely", value=float(d_vuln[1]), format="%.4f")
vuln_high = st.sidebar.number_input("Vuln Max", value=float(d_vuln[2]), format="%.4f")
pl_low = st.sidebar.number_input("PL Min", value=float(d_pl[0]))
pl_mode = st.sidebar.number_input("PL Most Likely", value=float(d_pl[1]))
pl_high = st.sidebar.number_input("PL Max", value=float(d_pl[2]))
slef_low = st.sidebar.number_input("SLEF Min", value=float(d_slef[0]), format="%.2f")
slef_mode = st.sidebar.number_input("SLEF Most Likely", value=float(d_slef[1]), format="%.2f")
slef_high = st.sidebar.number_input("SLEF Max", value=float(d_slef[2]), format="%.2f")
sl_low = st.sidebar.number_input("SL Min", value=float(d_sl[0]))
sl_mode = st.sidebar.number_input("SL Most Likely", value=float(d_sl[1]))
sl_high = st.sidebar.number_input("SL Max", value=float(d_sl[2]))

st.markdown("---")
run_comparison = False
vuln_reduction = 0
scenario_name = "With MFA"
annual_cost = 200000

col_run1, col_run2 = st.columns([1, 1])
with col_run1:
    run_baseline = st.button("Run Baseline (50,000 sims)", type="primary")
with col_run2:
    want_compare = st.checkbox("I want to compare a control scenario")
    if want_compare:
        scenario_name = st.text_input("Scenario name:", value="With MFA")
        vuln_reduction = st.slider("Vulnerability reduction %", min_value=0, max_value=95, value=70, step=5)
        annual_cost = st.number_input("Annual cost of control (USD):", min_value=0, value=200000, step=10000)
        new_vuln_mode = vuln_mode * (1 - vuln_reduction / 100)
        st.caption(f"Current vulnerability: {vuln_mode:.4f} ({vuln_mode*100:.2f}%)")
        st.caption(f"After {scenario_name}: {new_vuln_mode:.4f} ({new_vuln_mode*100:.2f}%)")
        run_comparison = True

if run_baseline or run_comparison:
    baseline = run_fair_simulation(tef_low, tef_mode, tef_high, vuln_low, vuln_mode, vuln_high, pl_low, pl_mode, pl_high, slef_low, slef_mode, slef_high, sl_low, sl_mode, sl_high)
    st.markdown("---")
    st.subheader("Baseline - Current State")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Median (P50)", f"${baseline.p50:,.0f}")
    c2.metric("Bad Year (P90)", f"${baseline.p90:,.0f}")
    c3.metric("Severe (P95)", f"${baseline.p95:,.0f}")
    c4.metric("Disaster (P99)", f"${baseline.p99:,.0f}")
    st.metric("Avg Breaches/Year", f"{baseline.breach_rate:.1f}")
    if run_comparison and vuln_reduction > 0:
        rd = vuln_reduction / 100
        scenario = run_fair_simulation(tef_low, tef_mode, tef_high, vuln_low*(1-rd), vuln_mode*(1-rd), vuln_high*(1-rd), pl_low, pl_mode, pl_high, slef_low, slef_mode, slef_high, sl_low, sl_mode, sl_high)
        st.markdown("---")
        st.subheader(f"Scenario - {scenario_name}")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Median (P50)", f"${scenario.p50:,.0f}", delta=f"-${baseline.p50-scenario.p50:,.0f}", delta_color="inverse")
        c2.metric("Bad Year (P90)", f"${scenario.p90:,.0f}", delta=f"-${baseline.p90-scenario.p90:,.0f}", delta_color="inverse")
        c3.metric("Severe (P95)", f"${scenario.p95:,.0f}", delta=f"-${baseline.p95-scenario.p95:,.0f}", delta_color="inverse")
        c4.metric("Disaster (P99)", f"${scenario.p99:,.0f}", delta=f"-${baseline.p99-scenario.p99:,.0f}", delta_color="inverse")
        st.markdown("---")
        st.subheader("Return on Investment")
        risk_red = baseline.p95 - scenario.p95
        roi = risk_red / annual_cost if annual_cost > 0 else 0
        r1, r2, r3 = st.columns(3)
        r1.metric("P95 Risk Reduction", f"${risk_red:,.0f}")
        r2.metric(f"Cost of {scenario_name}", f"${annual_cost:,.0f}")
        r3.metric("ROI", f"{roi:.1f}x")
        if roi > 10:
            st.success(f"Strong investment. {roi:.0f}x return.")
        elif roi > 3:
            st.info(f"Solid investment. {roi:.0f}x return.")
        elif roi > 1:
            st.warning(f"Marginal. Barely breaks even.")
        else:
            st.error(f"Weak investment. Consider alternatives.")
        st.markdown("---")
        st.subheader("Side-by-Side Comparison")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), sharey=True)
        bn = baseline.raw_losses[baseline.raw_losses > 0]
        sn = scenario.raw_losses[scenario.raw_losses > 0]
        if len(bn) > 0:
            ax1.hist(bn, bins=60, color="#E74C3C", edgecolor="white", alpha=0.85)
            ax1.axvline(baseline.p95, color="darkred", linestyle="--", linewidth=2, label=f"P95: ${baseline.p95:,.0f}")
            ax1.set_xlabel("Annual Loss (USD)")
            ax1.set_ylabel("Frequency")
            ax1.set_title("Baseline")
            ax1.legend()
        if len(sn) > 0:
            ax2.hist(sn, bins=60, color="#27AE60", edgecolor="white", alpha=0.85)
            ax2.axvline(scenario.p95, color="darkgreen", linestyle="--", linewidth=2, label=f"P95: ${scenario.p95:,.0f}")
            ax2.set_xlabel("Annual Loss (USD)")
            ax2.set_title(scenario_name)
            ax2.legend()
        plt.tight_layout()
        st.pyplot(fig)
    else:
        nz = baseline.raw_losses[baseline.raw_losses > 0]
        if len(nz) > 0:
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.hist(nz, bins=80, color="#4A90D9", edgecolor="white", alpha=0.85)
            ax.axvline(baseline.p95, color="red", linestyle="--", linewidth=2, label=f"P95: ${baseline.p95:,.0f}")
            ax.axvline(baseline.p50, color="green", linestyle="--", linewidth=2, label=f"P50: ${baseline.p50:,.0f}")
            ax.set_xlabel("Annual Loss (USD)")
            ax.set_ylabel("Frequency")
            ax.legend()
            ax.set_title("Annual Cyber Loss Distribution")
            st.pyplot(fig)
    report_text, risk_level, risk_color = generate_report(baseline, org_name)
    st.markdown("---")
    st.markdown(report_text)