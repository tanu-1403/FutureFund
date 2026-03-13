"""
FutureFund – Monte Carlo Simulation
Runs N simulations of investment growth with randomised annual returns
to estimate the probability of reaching a financial goal.
"""

import numpy as np
import pandas as pd


def run_monte_carlo(
    monthly_sip: float,
    mean_return: float,       # annual % e.g. 12
    years: int,
    goal_target: float,
    n_simulations: int = 1000,
    volatility: float = 8.0,  # annual std dev %
    seed: int = 42,
) -> dict:
    """
    Run Monte Carlo simulations.

    Returns a dict with:
      - final_values: np.array of terminal portfolio values
      - probability: float  (% chance of meeting goal)
      - percentiles: dict   (p10, p25, p50, p75, p90)
      - paths_sample: pd.DataFrame of 200 sampled paths for plotting
    """
    rng = np.random.default_rng(seed)
    n_months = years * 12
    monthly_mean = mean_return / 100 / 12
    monthly_vol  = volatility / 100 / np.sqrt(12)

    # Shape: (n_simulations, n_months)
    monthly_returns = rng.normal(
        loc=monthly_mean,
        scale=monthly_vol,
        size=(n_simulations, n_months),
    )

    # Build portfolio paths
    portfolio = np.zeros((n_simulations, n_months))
    for month in range(n_months):
        if month == 0:
            portfolio[:, month] = monthly_sip * (1 + monthly_returns[:, month])
        else:
            portfolio[:, month] = (
                portfolio[:, month - 1] * (1 + monthly_returns[:, month])
                + monthly_sip
            )

    final_values = portfolio[:, -1]
    probability  = float(np.mean(final_values >= goal_target) * 100)

    percentiles = {
        "p10": float(np.percentile(final_values, 10)),
        "p25": float(np.percentile(final_values, 25)),
        "p50": float(np.percentile(final_values, 50)),
        "p75": float(np.percentile(final_values, 75)),
        "p90": float(np.percentile(final_values, 90)),
    }

    # Sample 200 paths for the fan chart
    sample_idx = rng.choice(n_simulations, size=min(200, n_simulations), replace=False)
    sample_paths = portfolio[sample_idx, :]           # (200, n_months)
    months_axis  = np.arange(1, n_months + 1)

    paths_df = pd.DataFrame(
        sample_paths.T,
        index=months_axis,
    )
    paths_df.index.name = "month"

    return {
        "final_values":   final_values,
        "probability":    probability,
        "percentiles":    percentiles,
        "paths_sample":   paths_df,
        "goal_target":    goal_target,
        "n_simulations":  n_simulations,
    }


def monte_carlo_distribution_data(mc_result: dict) -> pd.DataFrame:
    """
    Return a tidy DataFrame of final values for histogram plotting.
    """
    fv = mc_result["final_values"]
    goal = mc_result["goal_target"]
    return pd.DataFrame({
        "final_value": fv,
        "meets_goal":  fv >= goal,
    })
