import numpy as np

def monte_carlo_simulation(sip, years, mean_return=0.10, volatility=0.15, simulations=500):

    months = years * 12
    final_values = []

    for _ in range(simulations):

        portfolio = 0

        for m in range(months):

            monthly_return = np.random.normal(mean_return/12, volatility/np.sqrt(12))

            portfolio = portfolio * (1 + monthly_return) + sip

        final_values.append(portfolio)

    return final_values