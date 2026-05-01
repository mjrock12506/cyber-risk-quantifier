"""
simulation.py — FAIR Monte Carlo Engine
Core risk quantification logic. No UI code here.
"""

import numpy as np


def pert(low, mode, high, size, lam=4):
    """
    PERT distribution — expert-friendly: min, most likely, max.
    Used throughout FAIR for eliciting estimates from SMEs.
    """
    r = high - low
    alpha = 1 + lam * (mode - low) / r
    beta = 1 + lam * (high - mode) / r
    return low + np.random.beta(alpha, beta, size) * r