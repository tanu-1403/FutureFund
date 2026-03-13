"""
FutureFund – Projections
Month-by-month investment growth timeseries for charting.
"""

import pandas as pd
from src.financial_engine import future_value


def build_growth_projection(
    monthly_sip: float,
    annual_return: float,
    years: int,
    goal_target: float,
) -> pd.DataFrame:
    """
    Build a month-by-month investment growth DataFrame.

    Returns columns: month, invested, portfolio_value, goal_line
    """
    r = (annual_return / 100) / 12
    records = []
    portfolio = 0.0
    total_invested = 0.0

    for month in range(1, years * 12 + 1):
        portfolio = portfolio * (1 + r) + monthly_sip
        total_invested += monthly_sip
        records.append({
            "month": month,
            "year": month / 12,
            "invested": round(total_invested, 2),
            "portfolio_value": round(portfolio, 2),
            "goal_line": round(goal_target, 2),
            "gains": round(portfolio - total_invested, 2),
        })

    return pd.DataFrame(records)


def build_goal_timeline(goals: list, annual_return: float, inflation_rate: float) -> pd.DataFrame:
    """
    Build a summary DataFrame of all goals with FV and SIP.
    goals: list of dicts with keys: name, cost, years
    """
    from src.financial_engine import future_value, required_sip
    rows = []
    for g in goals:
        fv = future_value(g["cost"], inflation_rate, g["years"])
        sip = required_sip(fv, annual_return, g["years"])
        rows.append({
            "Goal": g["name"],
            "Current Cost": g["cost"],
            "Years Away": g["years"],
            "Inflation-Adjusted Cost": round(fv, 2),
            "Required Monthly SIP": round(sip, 2),
        })
    return pd.DataFrame(rows) if rows else pd.DataFrame()
