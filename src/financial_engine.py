
import numpy as np


# --------------------------------------------------
# FUTURE GOAL VALUE (Inflation Adjustment)
# --------------------------------------------------

def future_goal_value(cost, years, inflation=0.06):
    """
    Calculate inflation-adjusted future cost of a goal.

    Parameters
    ----------
    cost : float
        Current cost of the goal
    years : int
        Years until the goal
    inflation : float
        Annual inflation rate (default 6%)

    Returns
    -------
    float
        Future cost of the goal
    """

    try:
        cost = float(cost)
        years = int(years)
        inflation = float(inflation)
    except:
        raise ValueError("Invalid input values")

    if years <= 0:
        raise ValueError("Years must be greater than 0")

    if cost < 0:
        raise ValueError("Cost must be non-negative")

    future_cost = cost * (1 + inflation) ** years

    return round(future_cost, 2)


# --------------------------------------------------
# REQUIRED SIP CALCULATOR
# --------------------------------------------------

def required_sip(future_value, annual_return=0.08, years=10):
    """
    Calculate the monthly SIP required to achieve a target future value.

    Uses the future value of SIP formula.

    Parameters
    ----------
    future_value : float
        Target future amount
    annual_return : float
        Expected annual return (default 8%)
    years : int
        Investment horizon in years

    Returns
    -------
    float
        Monthly SIP required
    """

    try:
        future_value = float(future_value)
        annual_return = float(annual_return)
        years = int(years)
    except:
        raise ValueError("Invalid numeric input")

    if future_value <= 0:
        raise ValueError("Future value must be positive")

    if years <= 0:
        raise ValueError("Years must be greater than 0")

    if annual_return <= 0:
        raise ValueError("Annual return must be positive")

    # Monthly return
    r = annual_return / 12

    # Number of months
    n = years * 12

    # SIP formula
    denominator = ((1 + r) ** n - 1) * (1 + r)

    if denominator == 0:
        raise ValueError("Invalid parameters for SIP calculation")

    sip = (future_value * r) / denominator

    return round(sip, 2)


# --------------------------------------------------
# FUTURE VALUE OF EXISTING SIP
# (useful for projections)
# --------------------------------------------------

def sip_future_value(monthly_investment, annual_return=0.08, years=10):
    """
    Calculates future value of a monthly SIP.

    Parameters
    ----------
    monthly_investment : float
        Monthly investment amount
    annual_return : float
        Expected annual return
    years : int
        Investment horizon

    Returns
    -------
    float
        Future portfolio value
    """

    if monthly_investment <= 0:
        return 0

    r = annual_return / 12
    n = years * 12

    fv = monthly_investment * (((1 + r) ** n - 1) / r) * (1 + r)

    return round(fv, 2)

