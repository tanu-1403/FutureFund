import numpy as np

def monte_carlo_simulation(sip, years, goal_value=None, mean_return=0.10, volatility=0.15, simulations=500):
    """
    Monte Carlo simulation for investment growth.

    Parameters:
        sip : float : Monthly investment
        years : int : Investment horizon
        goal_value : float : Target goal to calculate success probability
        mean_return : float : Expected annual return (decimal)
        volatility : float : Annual volatility (decimal)
        simulations : int : Number of simulations to run

    Returns:
        dict : {
            'final_values': list of portfolio values,
            'mean': float,
            'median': float,
            'success_prob': float (if goal_value provided),
            'percentiles': dict
        }
    """
    months = years * 12
    final_values = []

    for _ in range(simulations):
        portfolio = 0
        for m in range(months):
            monthly_return = np.random.normal(mean_return / 12, volatility / np.sqrt(12))
            portfolio = portfolio * (1 + monthly_return) + sip
        final_values.append(portfolio)

    final_values = np.array(final_values)
    results = {
        "final_values": final_values,
        "mean": np.mean(final_values),
        "median": np.median(final_values),
        "percentiles": {
            "10th": np.percentile(final_values, 10),
            "25th": np.percentile(final_values, 25),
            "75th": np.percentile(final_values, 75),
            "90th": np.percentile(final_values, 90),
        }
    }

    if goal_value is not None:
        success_prob = np.mean(final_values >= goal_value) * 100
        results["success_prob"] = success_prob

    return results