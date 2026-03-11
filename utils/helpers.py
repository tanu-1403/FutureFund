def format_currency(x, currency="₹"):
    """Formats a number as currency with commas."""
    return f"{currency}{x:,.0f}"

def generate_insight(sip_now, sip_later, goal_name=None):
    """Generates a textual insight comparing two SIP scenarios"""
    diff = ((sip_later - sip_now) / sip_now) * 100
    goal_text = f" for your goal '{goal_name}'" if goal_name else ""
    return f"Delaying investment{goal_text} increases required SIP by {diff:.1f}%"

def calculate_monthly_sip(future_value, years, annual_return=0.08):
    """
    Calculate the required monthly SIP to achieve a future goal using compound interest.
    
    Parameters:
        future_value : float : Future goal amount
        years : int : Number of years to achieve the goal
        annual_return : float : Expected annual return (default 8%)
    Returns:
        float : Required monthly SIP
    """
    months = years * 12
    monthly_rate = annual_return / 12
    # SIP formula: FV = P * [((1+r)^n -1)/r]
    sip = future_value * monthly_rate / (((1 + monthly_rate) ** months) - 1)
    return round(sip, 2)