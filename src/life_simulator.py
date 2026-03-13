"""
FutureFund – Life Simulator
Projects lifetime wealth accumulation across user-defined life phases.
"""

import pandas as pd
import numpy as np


# Default life phases (user can override)
DEFAULT_PHASES = [
    {"name": "Early Career",   "age_start": 22, "age_end": 35, "income_growth": 8,  "savings_rate": 20},
    {"name": "Growth Phase",   "age_start": 35, "age_end": 50, "income_growth": 5,  "savings_rate": 30},
    {"name": "Peak Earnings",  "age_start": 50, "age_end": 60, "income_growth": 3,  "savings_rate": 40},
    {"name": "Pre-Retirement", "age_start": 60, "age_end": 65, "income_growth": 2,  "savings_rate": 50},
    {"name": "Retirement",     "age_start": 65, "age_end": 85, "income_growth": 0,  "savings_rate": -5},
]


def simulate_lifetime_wealth(
    current_age: int,
    current_savings: float,       # total existing savings/investments
    monthly_income: float,
    annual_return: float,
    inflation_rate: float,
    goal_withdrawals: list = None,  # list of {year_from_now, amount}
) -> pd.DataFrame:
    """
    Simulate year-by-year net worth from current_age to age 85.

    Returns DataFrame with: age, year, net_worth, annual_savings, cumulative_invested
    """
    goal_withdrawals = goal_withdrawals or []
    withdrawal_map = {w["year_from_now"]: w["amount"] for w in goal_withdrawals}

    r_monthly = (annual_return / 100) / 12
    r_annual  = (1 + r_monthly) ** 12 - 1

    records = []
    net_worth = current_savings
    income = monthly_income * 12
    year = 0

    for age in range(current_age, 86):
        # Determine phase
        phase = _get_phase(age)
        savings_rate_pct = phase["savings_rate"] if phase else 20
        income_growth    = phase["income_growth"] if phase else 3

        # Annual savings contribution
        annual_savings = income * (savings_rate_pct / 100)
        if annual_savings < 0:
            annual_savings = abs(annual_savings) * -1   # drawdown in retirement

        # Grow net worth
        net_worth = net_worth * (1 + r_annual) + annual_savings

        # Subtract goal withdrawals
        if year in withdrawal_map:
            net_worth = max(0, net_worth - withdrawal_map[year])

        records.append({
            "age": age,
            "year": year,
            "net_worth": round(max(net_worth, 0), 2),
            "annual_savings": round(annual_savings, 2),
            "income": round(income, 2),
            "phase": phase["name"] if phase else "Retirement",
        })

        # Grow income for next year
        income *= (1 + income_growth / 100)
        year += 1

    return pd.DataFrame(records)


def _get_phase(age: int) -> dict:
    for phase in DEFAULT_PHASES:
        if phase["age_start"] <= age < phase["age_end"]:
            return phase
    return DEFAULT_PHASES[-1]
