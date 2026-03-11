from datetime import datetime, timedelta

def simulate_life(income, savings, growth=0.08, years=30, inflation=0.06, monthly=False, start_date=None):
    """
    Simulates lifetime wealth accumulation.

    Parameters:
        income : float : Annual income
        savings : float : Fraction of income saved (0-1)
        growth : float : Annual investment growth rate
        years : int : Number of years to simulate
        inflation : float : Annual inflation rate
        monthly : bool : Whether to simulate monthly instead of yearly
        start_date : datetime : Optional start date

    Returns:
        list of dict : Each dict has date, nominal wealth, real wealth
    """
    history = []
    wealth = 0

    if not start_date:
        start_date = datetime.today()

    if monthly:
        months = years * 12
        monthly_income = income / 12
        monthly_savings = monthly_income * savings
        monthly_growth = (1 + growth) ** (1/12) - 1
        monthly_inflation = (1 + inflation) ** (1/12) - 1

        for m in range(1, months + 1):
            wealth = wealth * (1 + monthly_growth) + monthly_savings
            real_wealth = wealth / ((1 + monthly_inflation) ** m)
            history.append({
                "date": start_date + timedelta(days=30 * m),
                "nominal": wealth,
                "real_value": real_wealth
            })
            # Optionally increase income yearly
            if m % 12 == 0:
                monthly_income *= 1.05
                monthly_savings = monthly_income * savings
    else:
        for y in range(1, years + 1):
            wealth = wealth * (1 + growth) + savings * 12
            real_wealth = wealth / ((1 + inflation) ** y)
            history.append({
                "year": y,
                "nominal": wealth,
                "real_value": real_wealth
            })
            income *= 1.05
            savings = income * savings

    return history