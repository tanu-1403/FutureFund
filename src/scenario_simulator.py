import sys
import os

# Add parent directory to path so Python can find utils/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.helpers import calculate_monthly_sip, generate_insight, format_currency
from utils.goal_manager import calculate_future_cost

def simulate_delay(goal_name, current_cost, years, delay, annual_return=0.08, inflation=0.06):
    """
    Simulates the effect of delaying investment for a specific goal.
    """
    future_goal_value = calculate_future_cost(current_cost, years, inflation)
    future_goal_value_delayed = calculate_future_cost(current_cost, years - delay, inflation)

    sip_now = calculate_monthly_sip(future_goal_value, years, annual_return)
    sip_delayed = calculate_monthly_sip(future_goal_value_delayed, years - delay, annual_return)

    diff = sip_delayed - sip_now
    percent_increase = (diff / sip_now) * 100
    insight_text = generate_insight(sip_now, sip_delayed, goal_name)

    return {
        "goal_name": goal_name,
        "sip_now": sip_now,
        "sip_delayed": sip_delayed,
        "diff": diff,
        "percent_increase": percent_increase,
        "insight": insight_text,
        "future_goal_value": future_goal_value,
        "future_goal_value_delayed": future_goal_value_delayed
    }