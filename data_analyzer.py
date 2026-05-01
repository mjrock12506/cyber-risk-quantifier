"""
data_analyzer.py — Upload-based FAIR Input Estimator
Reads CSV/Excel files with incident or security data,
extracts statistics, and maps them to FAIR input ranges.
"""

import pandas as pd
import numpy as np


def detect_columns(df):
    """
    Tries to figure out which columns contain what.
    Looks for common column names from SIEM/ticketing exports.
    Returns a dictionary mapping our needs to actual column names.
    """
    col_lower = {c: c.lower().strip() for c in df.columns}

    mapping = {
        "date": None,
        "cost": None,
        "severity": None,
        "type": None,
        "status": None,
        "detect_time": None,
    }

    date_keywords = ["date", "time", "timestamp", "created", "opened", "reported"]
    cost_keywords = ["cost", "loss", "amount", "damage", "financial", "impact_cost", "dollar"]
    severity_keywords = ["severity", "priority", "level", "risk", "rating", "criticality"]
    type_keywords = ["type", "category", "class", "incident_type", "attack", "threat"]
    status_keywords = ["status", "state", "outcome", "result", "resolved"]
    detect_keywords = ["detect", "dwell", "mttr", "mttd", "response_time", "time_to"]

    for actual_col, lower_col in col_lower.items():
        for kw in date_keywords:
            if kw in lower_col and mapping["date"] is None:
                mapping["date"] = actual_col
        for kw in cost_keywords:
            if kw in lower_col and mapping["cost"] is None:
                mapping["cost"] = actual_col
        for kw in severity_keywords:
            if kw in lower_col and mapping["severity"] is None:
                mapping["severity"] = actual_col
        for kw in type_keywords:
            if kw in lower_col and mapping["type"] is None:
                mapping["type"] = actual_col
        for kw in status_keywords:
            if kw in lower_col and mapping["status"] is None:
                mapping["status"] = actual_col
        for kw in detect_keywords:
            if kw in lower_col and mapping["detect_time"] is None:
                mapping["detect_time"] = actual_col

    return mapping


def analyze_data(df):
    """
    Analyzes uploaded data and returns:
    - FAIR input estimates
    - Summary statistics
    - Plain-English explanation of findings
    """
    mapping = detect_columns(df)
    total_rows = len(df)
    findings = []
    fair_inputs = {}

    # --- Estimate TEF (Threat Event Frequency) ---
    # Total rows = total events/attempts logged
    if mapping["date"] is not None:
        try:
            dates = pd.to_datetime(df[mapping["date"]], errors="coerce")
            dates_clean = dates.dropna()
            if len(dates_clean) > 1:
                date_range_days = (dates_clean.max() - dates_clean.min()).days
                if date_range_days > 0:
                    events_per_year = total_rows * (365 / date_range_days)
                else:
                    events_per_year = total_rows
            else:
                events_per_year = total_rows
        except Exception:
            events_per_year = total_rows

        tef_mode = round(events_per_year)
        tef_low = round(tef_mode * 0.5)
        tef_high = round(tef_mode * 2.0)
        fair_inputs["tef"] = (tef_low, tef_mode, tef_high)
        findings.append(
            f"Found {total_rows} events across your data. "
            f"Estimated annual threat frequency: ~{tef_mode} events/year."
        )
    else:
        # No date column — use row count as rough estimate
        fair_inputs["tef"] = (
            round(total_rows * 0.5),
            total_rows,
            round(total_rows * 2.0),
        )
        findings.append(
            f"Found {total_rows} rows. No date column detected — "
            f"using row count as event frequency estimate."
        )

    # --- Estimate Vulnerability ---
    # If we can identify "successful" vs "total" events
    if mapping["status"] is not None:
        status_col = df[mapping["status"]].astype(str).str.lower()
        success_keywords = ["success", "breach", "compromised", "confirmed",
                          "true positive", "critical", "high", "exploited"]
        successful = status_col.apply(
            lambda x: any(kw in x for kw in success_keywords)
        ).sum()

        if total_rows > 0:
            vuln_rate = successful / total_rows
        else:
            vuln_rate = 0.01

        vuln_mode = max(vuln_rate, 0.001)  # Floor at 0.1%
        vuln_low = vuln_mode * 0.3
        vuln_high = min(vuln_mode * 3.0, 0.99)
        fair_inputs["vuln"] = (round(vuln_low, 4), round(vuln_mode, 4), round(vuln_high, 4))
        findings.append(
            f"Detected {successful} successful/confirmed incidents out of "
            f"{total_rows} total events = {vuln_rate:.2%} success rate."
        )
    elif mapping["severity"] is not None:
        # Use severity as a proxy — high/critical = likely successful
        sev_col = df[mapping["severity"]].astype(str).str.lower()
        high_sev = sev_col.apply(
            lambda x: any(kw in x for kw in ["high", "critical", "severe", "4", "5"])
        ).sum()

        if total_rows > 0:
            vuln_rate = high_sev / total_rows
        else:
            vuln_rate = 0.01

        vuln_mode = max(vuln_rate, 0.001)
        vuln_low = vuln_mode * 0.3
        vuln_high = min(vuln_mode * 3.0, 0.99)
        fair_inputs["vuln"] = (round(vuln_low, 4), round(vuln_mode, 4), round(vuln_high, 4))
        findings.append(
            f"No status column found. Using severity as proxy: "
            f"{high_sev} high/critical events out of {total_rows} = {vuln_rate:.2%}."
        )
    else:
        fair_inputs["vuln"] = (0.001, 0.010, 0.050)
        findings.append(
            "No status or severity column found. Using default vulnerability range."
        )

    # --- Estimate Primary Loss ---
    if mapping["cost"] is not None:
        costs = pd.to_numeric(df[mapping["cost"]], errors="coerce").dropna()
        if len(costs) > 0:
            pl_low = round(float(costs.quantile(0.10)))
            pl_mode = round(float(costs.median()))
            pl_high = round(float(costs.quantile(0.95)))
            # Ensure min < mode < max
            if pl_low >= pl_mode:
                pl_low = round(pl_mode * 0.3)
            if pl_high <= pl_mode:
                pl_high = round(pl_mode * 3.0)
            fair_inputs["pl"] = (max(pl_low, 1000), pl_mode, pl_high)
            findings.append(
                f"Cost data found. Median cost: ${pl_mode:,.0f}. "
                f"Range: ${pl_low:,.0f} to ${pl_high:,.0f}."
            )
        else:
            fair_inputs["pl"] = (50000, 250000, 2000000)
            findings.append("Cost column found but no valid numbers. Using defaults.")
    else:
        fair_inputs["pl"] = (50000, 250000, 2000000)
        findings.append("No cost column found. Using industry-average primary loss range.")

    # --- Secondary loss (defaults — hard to detect from raw data) ---
    fair_inputs["slef"] = (0.05, 0.20, 0.50)
    fair_inputs["sl"] = (100000, 1500000, 20000000)
    findings.append(
        "Secondary loss (fines/lawsuits) uses default ranges — "
        "adjust based on your regulatory environment."
    )

    # --- Build summary ---
    summary = {
        "total_events": total_rows,
        "columns_detected": {k: v for k, v in mapping.items() if v is not None},
        "columns_missed": [k for k, v in mapping.items() if v is None],
        "findings": findings,
        "fair_inputs": fair_inputs,
    }

    return summary