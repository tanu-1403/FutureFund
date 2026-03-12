
from datetime import datetime
from dateutil.relativedelta import relativedelta


def simulate_life(
    income,
    savings_rate,
    growth=0.08,
    years=30,
    inflation=0.06,
    monthly=False,
    salary_growth=0.05,
    start_date=None
):
    """
    Simulate lifetime wealth accumulation.

    Parameters
    ----------
    income : float
        Monthly income
    savings_rate : float
        Fraction of income saved (0-1)
    growth : float
        Annual investment return
    years : int
        Simulation horizon
    inflation : float
        Annual inflation
    monthly : bool
        Monthly or yearly simulation
    salary_growth : float
        Annual salary increase
    start_date : datetime
        Optional start date

    Returns
    -------
    list[dict]
        Wealth history
    """

    if income <= 0:
        raise ValueError("Income must be positive")

    if not (0 <= savings_rate <= 1):
        raise ValueError("Savings rate must be between 0 and 1")

    if not start_date:
        start_date = datetime.today()

    history = []
    wealth = 0

    # ---------------------------------------
    # MONTHLY SIMULATION
    # ---------------------------------------

    if monthly:

        months = years * 12

        monthly_growth = (1 + growth) ** (1/12) - 1
        monthly_inflation = (1 + inflation) ** (1/12) - 1

        current_income = income

        for m in range(1, months + 1):

            monthly_savings = current_income * savings_rate

            wealth = wealth * (1 + monthly_growth) + monthly_savings

            real_wealth = wealth / ((1 + monthly_inflation) ** m)

            history.append({
                "date": start_date + relativedelta(months=m),
                "nominal": round(wealth, 2),
                "real_value": round(real_wealth, 2)
            })

            # increase salary yearly
            if m % 12 == 0:
                current_income *= (1 + salary_growth)

    # ---------------------------------------
    # YEARLY SIMULATION
    # ---------------------------------------

    else:

        current_income = income

        for y in range(1, years + 1):

            yearly_savings = current_income * savings_rate * 12

            wealth = wealth * (1 + growth) + yearly_savings

            real_wealth = wealth / ((1 + inflation) ** y)

            history.append({
                "year": y,
                "nominal": round(wealth, 2),
                "real_value": round(real_wealth, 2)
            })

            current_income *= (1 + salary_growth)

    return history

