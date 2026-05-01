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


from dataclasses import dataclass


@dataclass
class SimulationResult:
    """Container for simulation outputs."""
    raw_losses: np.ndarray
    mean: float
    p50: float
    p90: float
    p95: float
    p99: float
    max_loss: float
    breach_rate: float  # average breaches per year


def run_fair_simulation(
    tef_low, tef_mode, tef_high,
    vuln_low, vuln_mode, vuln_high,
    pl_low, pl_mode, pl_high,
    slef_low, slef_mode, slef_high,
    sl_low, sl_mode, sl_high,
    n_sims=50_000
):
    """
    Run a full FAIR Monte Carlo simulation.

    Parameters:
        tef  = Threat Event Frequency (attempts per year)
        vuln = Vulnerability (probability each attempt succeeds)
        pl   = Primary Loss magnitude (USD)
        slef = Secondary Loss Event Frequency (probability per breach)
        sl   = Secondary Loss magnitude (USD)
        n_sims = number of Monte Carlo iterations

    Returns:
        SimulationResult with loss distribution and summary stats
    """
    # Sample each FAIR input from PERT distributions
    tef = pert(tef_low, tef_mode, tef_high, n_sims)
    vuln = pert(vuln_low, vuln_mode, vuln_high, n_sims)
    primary_loss = pert(pl_low, pl_mode, pl_high, n_sims)
    sec_freq = pert(slef_low, slef_mode, slef_high, n_sims)
    sec_loss = pert(sl_low, sl_mode, sl_high, n_sims)

    # Loss Event Frequency = how many breaches actually happen
    lef = tef * vuln
    n_breaches = np.random.poisson(lef)

    # Primary loss: direct cost per breach × number of breaches
    total_primary = n_breaches * primary_loss

    # Secondary loss: each breach independently rolls for downstream consequences
    n_secondary = np.random.binomial(n_breaches, sec_freq)
    total_secondary = n_secondary * sec_loss

    # Total annual loss
    annual_loss = total_primary + total_secondary

    return SimulationResult(
        raw_losses=annual_loss,
        mean=float(annual_loss.mean()),
        p50=float(np.percentile(annual_loss, 50)),
        p90=float(np.percentile(annual_loss, 90)),
        p95=float(np.percentile(annual_loss, 95)),
        p99=float(np.percentile(annual_loss, 99)),
        max_loss=float(annual_loss.max()),
        breach_rate=float(lef.mean()),
    )