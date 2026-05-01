"""
presets.py — Industry presets for FAIR inputs
Sources: Verizon DBIR 2024, Ponemon Cost of a Data Breach 2024
"""

PRESETS = {
    "Custom (enter your own)": None,

    "Healthcare": {
        "tef": (800, 3000, 12000),
        "vuln": (0.002, 0.015, 0.06),
        "pl": (100000, 500000, 3000000),
        "slef": (0.10, 0.30, 0.60),
        "sl": (200000, 2000000, 25000000),
        "source": "Based on Verizon DBIR 2024 — Healthcare sector. High SLEF due to HIPAA.",
    },

    "Financial Services": {
        "tef": (1000, 5000, 20000),
        "vuln": (0.001, 0.008, 0.03),
        "pl": (80000, 400000, 2500000),
        "slef": (0.08, 0.25, 0.55),
        "sl": (150000, 1800000, 22000000),
        "source": "Based on Verizon DBIR 2024 — Finance sector. High TEF, lower Vuln due to mature controls.",
    },

    "Retail / E-commerce": {
        "tef": (500, 2000, 8000),
        "vuln": (0.003, 0.02, 0.07),
        "pl": (40000, 200000, 1500000),
        "slef": (0.05, 0.15, 0.40),
        "sl": (100000, 1000000, 15000000),
        "source": "Based on Verizon DBIR 2024 — Retail sector. PCI-DSS exposure in secondary loss.",
    },

    "Small Business (< 250 employees)": {
        "tef": (200, 800, 3000),
        "vuln": (0.005, 0.03, 0.10),
        "pl": (20000, 100000, 800000),
        "slef": (0.03, 0.10, 0.30),
        "sl": (50000, 500000, 5000000),
        "source": "Based on Ponemon 2024 — SMB segment. Higher vuln, lower absolute loss.",
    },
}