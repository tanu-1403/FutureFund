def simulate_life(income, savings, growth=0.08, years=30):

    wealth = 0

    history = []

    for y in range(years):

        income *= 1.05

        invest = savings * 12

        wealth = wealth * (1 + growth) + invest

        history.append(wealth)

    return history