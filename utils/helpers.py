
def format_currency(x, currency="₹"):
    """
    Formats a number as currency with commas.
    Example: 1250000 -> ₹1,250,000
    """
    if x is None:
        return f"{currency}0"

    return f"{currency}{x:,.0f}"


def generate_insight(sip_now, sip_later, goal_name=None):
    """
    Generates a textual insight comparing two SIP scenarios.
    """

    if sip_now <= 0:
        return "Unable to generate insight due to invalid SIP value."

    diff_percent = ((sip_later - sip_now) / sip_now) * 100

    goal_text = f" for your goal '{goal_name}'" if goal_name else ""

    if diff_percent > 0:
        return (
            f"⚠ Delaying investment{goal_text} increases the required SIP "
            f"by {diff_percent:.1f}%."
        )
    elif diff_percent < 0:
        return (
            f"✅ Investing earlier{goal_text} reduces the required SIP "
            f"by {abs(diff_percent):.1f}%."
        )
    else:
        return "No difference between the two investment scenarios."


def calculate_monthly_sip(future_value, years, annual_return=0.08):
    """
    Calculate required monthly SIP to reach a future goal.

    Formula:
        FV = P * [((1+r)^n - 1) / r]

    Where:
        FV = future value
        P  = SIP amount
        r  = monthly interest rate
        n  = number of months
    """

    if future_value <= 0:
        raise ValueError("Future value must be positive")

    if years <= 0:
        raise ValueError("Years must be positive")

    months = years * 12
    monthly_rate = annual_return / 12

    # Edge case: zero return
    if monthly_rate == 0:
        sip = future_value / months
        return round(sip, 2)

    sip = future_value * monthly_rate / (((1 + monthly_rate) ** months) - 1)

    return round(sip, 2)

