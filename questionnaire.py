"""
questionnaire.py — Smart Questionnaire
Asks simple questions about the organization, maps answers to FAIR ranges.
No AI needed — just expert logic.
"""


def build_fair_inputs(answers):
    """
    Takes a dictionary of simple answers and returns calibrated FAIR ranges.
    Think of this as a security consultant in a box.
    """

    industry = answers.get("industry", "other")

    baselines = {
        "healthcare": {
            "tef": [800, 3000, 12000],
            "vuln": [0.002, 0.015, 0.060],
            "pl": [100000, 500000, 3000000],
            "slef": [0.10, 0.30, 0.60],
            "sl": [200000, 2000000, 25000000],
        },
        "finance": {
            "tef": [1000, 5000, 20000],
            "vuln": [0.001, 0.008, 0.030],
            "pl": [80000, 400000, 2500000],
            "slef": [0.08, 0.25, 0.55],
            "sl": [150000, 1800000, 22000000],
        },
        "retail": {
            "tef": [500, 2000, 8000],
            "vuln": [0.003, 0.020, 0.070],
            "pl": [40000, 200000, 1500000],
            "slef": [0.05, 0.15, 0.40],
            "sl": [100000, 1000000, 15000000],
        },
        "other": {
            "tef": [300, 1500, 6000],
            "vuln": [0.003, 0.020, 0.070],
            "pl": [30000, 150000, 1000000],
            "slef": [0.05, 0.15, 0.35],
            "sl": [80000, 800000, 10000000],
        },
    }

    inputs = baselines.get(industry, baselines["other"])

    # Adjust based on company size
    size = answers.get("employees", 100)
    if size > 1000:
        inputs["tef"] = [x * 1.5 for x in inputs["tef"]]
        inputs["pl"] = [x * 1.3 for x in inputs["pl"]]
        inputs["sl"] = [x * 1.5 for x in inputs["sl"]]
    elif size < 50:
        inputs["tef"] = [x * 0.5 for x in inputs["tef"]]
        inputs["pl"] = [x * 0.6 for x in inputs["pl"]]
        inputs["sl"] = [x * 0.5 for x in inputs["sl"]]

    # Adjust vulnerability based on security controls
    has_mfa = answers.get("has_mfa", False)
    has_edr = answers.get("has_edr", False)
    has_training = answers.get("has_training", False)
    had_incident = answers.get("had_incident", False)

    vuln_multiplier = 1.0

    if has_mfa:
        vuln_multiplier *= 0.3
    if has_edr:
        vuln_multiplier *= 0.5
    if has_training:
        vuln_multiplier *= 0.7
    if had_incident:
        vuln_multiplier *= 1.3

    inputs["vuln"] = [v * vuln_multiplier for v in inputs["vuln"]]
    inputs["vuln"] = [min(v, 0.99) for v in inputs["vuln"]]

    # Build reasoning
    controls = []
    if has_mfa:
        controls.append("MFA (reduces vulnerability ~70%)")
    if has_edr:
        controls.append("EDR (reduces vulnerability ~50%)")
    if has_training:
        controls.append("Security training (reduces vulnerability ~30%)")
    if not controls:
        controls.append("No major controls reported — vulnerability remains at baseline")

    reasoning = (
        f"Industry: {industry.title()}. "
        f"Size: {size} employees. "
        f"Controls: {', '.join(controls)}. "
    )
    if had_incident:
        reasoning += "Past incident reported — vulnerability adjusted upward. "

    return {
        "tef": tuple(inputs["tef"]),
        "vuln": tuple(inputs["vuln"]),
        "pl": tuple(inputs["pl"]),
        "slef": tuple(inputs["slef"]),
        "sl": tuple(inputs["sl"]),
        "reasoning": reasoning,
    }