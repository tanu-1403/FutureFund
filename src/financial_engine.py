"""
FutureFund – Financial Engine
Core financial formula implementations.
All calculations are illustrative and educational.
"""
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import math


def future_value(present_value: float, inflation_rate: float, years: int) -> float:
    """
    Calculate the future cost of a goal after inflation.
    FV = PV × (1 + i)^n
    """
    if years <= 0:
        return present_value
    return present_value * math.pow(1 + inflation_rate / 100, years)


def required_sip(future_goal: float, annual_return: float, years: int) -> float:
    """
    Calculate required monthly SIP to reach a future goal.
    SIP = FV × r / [((1 + r)^n − 1) × (1 + r)]
    where r = monthly rate, n = total months
    """
    if years <= 0 or future_goal <= 0:
        return 0.0
    r = (annual_return / 100) / 12
    n = years * 12
    if r == 0:
        return future_goal / n
    sip = (future_goal * r) / ((math.pow(1 + r, n) - 1) * (1 + r))
    return max(sip, 0.0)


def sip_future_value(monthly_sip: float, annual_return: float, years: int) -> float:
    """
    Calculate future value of a fixed monthly SIP.
    FV = P × [((1 + r)^n − 1) / r] × (1 + r)
    """
    if years <= 0 or monthly_sip <= 0:
        return 0.0
    r = (annual_return / 100) / 12
    n = years * 12
    if r == 0:
        return monthly_sip * n
    return monthly_sip * ((math.pow(1 + r, n) - 1) / r) * (1 + r)


def savings_rate(monthly_savings: float, monthly_income: float) -> float:
    """Return savings rate as a percentage."""
    if monthly_income <= 0:
        return 0.0
    return (monthly_savings / monthly_income) * 100


def affordability_score(
    monthly_sip: float,
    monthly_savings: float,
    monthly_income: float
) -> dict:
    """
    Returns an affordability assessment dict with score, label and colour.
    """
    if monthly_savings <= 0 or monthly_income <= 0:
        return {"score": 0, "label": "Unknown", "color": "#888888"}

    ratio = monthly_sip / monthly_savings if monthly_savings > 0 else float("inf")

    if ratio <= 0.3:
        return {"score": 95, "label": "Very Affordable", "color": "#00c896"}
    elif ratio <= 0.5:
        return {"score": 75, "label": "Affordable", "color": "#4caf50"}
    elif ratio <= 0.75:
        return {"score": 50, "label": "Moderate Stretch", "color": "#ff9800"}
    elif ratio <= 1.0:
        return {"score": 25, "label": "Tight Budget", "color": "#f44336"}
    else:
        return {"score": 5, "label": "Needs Adjustment", "color": "#b71c1c"}
