"""
FutureFund – Goal Manager
Handles CRUD operations for financial goals stored in st.session_state.
"""

import uuid
from datetime import datetime
from typing import Optional


GOAL_ICONS = {
    "car":       "🚗",
    "house":     "🏠",
    "education": "🎓",
    "retirement":"🌴",
    "travel":    "✈️",
    "wedding":   "💍",
    "business":  "💼",
    "emergency": "🛡️",
    "other":     "⭐",
}


def make_goal(
    name: str,
    cost: float,
    years: int,
    category: str = "other",
    notes: str = "",
    priority: str = "Medium",
) -> dict:
    """Create a new goal dict."""
    return {
        "id":        str(uuid.uuid4())[:8],
        "name":      name.strip(),
        "cost":      float(cost),
        "years":     int(years),
        "category":  category.lower(),
        "notes":     notes.strip(),
        "priority":  priority,
        "created_at": datetime.now().strftime("%b %d, %Y"),
        "icon":      GOAL_ICONS.get(category.lower(), "⭐"),
    }


def add_goal(goals: list, goal: dict) -> list:
    return goals + [goal]


def remove_goal(goals: list, goal_id: str) -> list:
    return [g for g in goals if g["id"] != goal_id]


def get_goal_by_id(goals: list, goal_id: str) -> Optional[dict]:
    for g in goals:
        if g["id"] == goal_id:
            return g
    return None


def total_sip_required(goals: list, annual_return: float, inflation_rate: float) -> float:
    """Sum of required SIPs for all goals."""
    from src.financial_engine import future_value, required_sip
    total = 0.0
    for g in goals:
        fv = future_value(g["cost"], inflation_rate, g["years"])
        total += required_sip(fv, annual_return, g["years"])
    return total


def sort_goals(goals: list, by: str = "years") -> list:
    """Sort goals by 'years', 'cost', or 'name'."""
    return sorted(goals, key=lambda g: g.get(by, 0))


PRIORITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}
PRIORITY_COLORS = {
    "High":   "#ff4757",
    "Medium": "#ffa502",
    "Low":    "#2ed573",
}
