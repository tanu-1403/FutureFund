
import numpy as np


def monte_carlo_simulation(
    sip,
    years,
    goal_value=None,
    mean_return=0.10,
    volatility=0.15,
    simulations=500,
    seed=None
):
    """
    Monte Carlo simulation for SIP investment growth.

    Parameters
    ----------
    sip : float
        Monthly investment
    years : int
        Investment horizon
    goal_value : float
        Optional target goal value
    mean_return : float
        Expected annual return
    volatility : float
        Annual return volatility
    simulations : int
        Number of simulations
    seed : int
        Optional random seed for reproducibility

    Returns
    -------
    dict
        Simulation statistics and portfolio outcomes
    """

    # -----------------------------
    # Input validation
    # -----------------------------
    sip = float(sip)
    years = int(years)

    if sip < 0:
        raise ValueError("SIP must be non-negative")

    if years <= 0:
        raise ValueError("Years must be positive")

    if simulations <= 0:
        raise ValueError("Simulations must be positive")

    if seed is not None:
        np.random.seed(seed)

    months = years * 12

    # convert annual parameters
    monthly_mean = mean_return / 12
    monthly_vol = volatility / np.sqrt(12)

    final_values = []

    # -----------------------------
    # Simulation
    # -----------------------------
    for _ in range(simulations):

        portfolio = 0

        for _ in range(months):

            monthly_return = np.random.normal(monthly_mean, monthly_vol)

            # prevent impossible loss
            monthly_return = max(monthly_return, -0.95)

            portfolio = portfolio * (1 + monthly_return) + sip

        final_values.append(portfolio)

    final_values = np.array(final_values)

    # -----------------------------
    # Statistics
    # -----------------------------
    results = {

        "final_values": final_values.tolist(),

        "mean": float(np.mean(final_values)),

        "median": float(np.median(final_values)),

        "std_dev": float(np.std(final_values)),

        "percentiles": {

            "10th": float(np.percentile(final_values, 10)),
            "25th": float(np.percentile(final_values, 25)),
            "50th": float(np.percentile(final_values, 50)),
            "75th": float(np.percentile(final_values, 75)),
            "90th": float(np.percentile(final_values, 90))

        }
    }

    # -----------------------------
    # Goal success probability
    # -----------------------------
    if goal_value is not None:

        success_prob = np.mean(final_values >= goal_value)

        results["success_prob"] = float(success_prob)

    return results

