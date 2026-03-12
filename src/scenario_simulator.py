
import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.helpers import calculate_monthly_sip, generate_insight
from utils.goal_manager import calculate_future_cost


def simulate_delay(
    goal_name,
    current_cost,
    years,
    delay,
    annual_return=0.08,
    inflation=0.06
):
    """
    Simulate the financial impact of delaying investment.

    Parameters
    ----------
    goal_name : str
    current_cost : float
    years : int
    delay : int
    annual_return : float
    inflation : float

    Returns
    -------
    dict
    """

    # -----------------------------
    # Input validation
    # -----------------------------
    if years <= 0:
        raise ValueError("Years must be positive")

    if delay < 0:
        raise ValueError("Delay cannot be negative")

    if delay >= years:
        raise ValueError("Delay cannot exceed goal timeline")

    if current_cost <= 0:
        raise ValueError("Goal cost must be positive")

    # -----------------------------
    # Future cost (goal still inflates)
    # -----------------------------
    future_goal_value = calculate_future_cost(
        current_cost,
        years,
        inflation
    )

    # -----------------------------
    # SIP if investing today
    # -----------------------------
    sip_now = calculate_monthly_sip(
        future_goal_value,
        years,
        annual_return
    )

    # -----------------------------
    # SIP if investing later
    # -----------------------------
    remaining_years = years - delay

    sip_delayed = calculate_monthly_sip(
        future_goal_value,
        remaining_years,
        annual_return
    )

    # -----------------------------
    # Financial impact
    # -----------------------------
    diff = sip_delayed - sip_now

    percent_increase = 0
    if sip_now > 0:
        percent_increase = (diff / sip_now) * 100

    # -----------------------------
    # Insight text
    # -----------------------------
    insight_text = generate_insight(
        sip_now,
        sip_delayed,
        goal_name
    )

    return {

        "goal_name": goal_name,

        "future_goal_value": future_goal_value,

        "sip_now": sip_now,

        "sip_delayed": sip_delayed,

        "difference": diff,

        "percent_increase": percent_increase,

        "delay_years": delay,

        "insight": insight_text
    }

