import numpy as np

def future_goal_value(cost, years, inflation=0.06):
    """
    Calculates the inflation-adjusted future cost of a goal.

    Parameters:
        cost : float : Current cost
        years : int : Years until goal
        inflation : float : Expected annual inflation rate (default 6%)

    Returns:
        float : Future cost
    """
    if years <= 0:
        raise ValueError("Years must be greater than 0")
    if cost < 0:
        raise ValueError("Cost must be positive")

    return round(cost * (1 + inflation) ** years, 2)


def required_sip(future_value, annual_return=0.08, years=10):
    """
    Calculates required monthly SIP to achieve a future value.

    Parameters:
        future_value : float : Future target amount
        annual_return : float : Expected annual return (decimal)
        years : int : Investment horizon in years

    Returns:
        float : Monthly SIP
    """
    if years <= 0:
        raise ValueError("Years must be greater than 0")
    if future_value <= 0:
        raise ValueError("Future value must be positive")

    r = annual_return / 12
    n = years * 12

    sip = (future_value * r) / (((1 + r) ** n - 1) * (1 + r))

    return round(sip, 2)