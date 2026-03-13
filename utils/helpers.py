"""
FutureFund – Helpers
Formatting and general utility functions.
"""


def fmt_inr(value: float, short: bool = False) -> str:
    """Format a number as Indian Rupees."""
    if value is None:
        return "₹0"
    v = abs(value)
    sign = "-" if value < 0 else ""
    if short:
        if v >= 1e7:
            return f"{sign}₹{v/1e7:.2f} Cr"
        elif v >= 1e5:
            return f"{sign}₹{v/1e5:.2f} L"
        elif v >= 1e3:
            return f"{sign}₹{v/1e3:.1f} K"
        return f"{sign}₹{v:,.0f}"
    if v >= 1e7:
        return f"{sign}₹{v/1e7:.2f} Cr"
    elif v >= 1e5:
        return f"{sign}₹{v/1e5:.2f} L"
    return f"{sign}₹{v:,.0f}"


def fmt_pct(value: float, decimals: int = 1) -> str:
    return f"{value:.{decimals}f}%"


def fmt_years(years: int) -> str:
    if years == 1:
        return "1 year"
    return f"{years} years"


def clamp(value, min_val, max_val):
    return max(min_val, min(max_val, value))


def health_color(score: float) -> str:
    """Return a color string based on a 0–100 score."""
    if score >= 75:
        return "#00c896"
    elif score >= 50:
        return "#ffa502"
    elif score >= 25:
        return "#ff6b6b"
    return "#b71c1c"


def probability_label(prob: float) -> tuple[str, str]:
    """Return (label, color) for a probability percentage."""
    if prob >= 80:
        return "High Confidence", "#00c896"
    elif prob >= 60:
        return "Moderate Confidence", "#ffa502"
    elif prob >= 40:
        return "Uncertain", "#ff9800"
    return "Needs Review", "#ff4757"
