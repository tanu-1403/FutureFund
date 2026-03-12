
def generate_advice(goal_name, income, savings, sip, probability, min_savings_rate=0.2):
    """
    Generates personalized financial advice for a specific goal.

    Parameters
    ----------
    goal_name : str
        Name of the goal
    income : float
        Monthly income
    savings : float
        Monthly savings available
    sip : float
        Monthly investment required
    probability : float
        Probability of achieving goal (0-1)
    min_savings_rate : float
        Recommended minimum savings rate (default 20%)

    Returns
    -------
    list[str]
        List of financial advice messages
    """

    advice = []

    # ----------------------------
    # Input Safety
    # ----------------------------
    try:
        income = float(income)
        savings = float(savings)
        sip = float(sip)
        probability = float(probability)
    except:
        return [f"Financial inputs for '{goal_name}' are invalid."]

    if income <= 0:
        return [f"Income data missing or invalid for goal '{goal_name}'."]

    if probability < 0 or probability > 1:
        probability = 0

    # ----------------------------
    # Savings Rate Check
    # ----------------------------
    savings_rate = savings / income

    if savings_rate < min_savings_rate:

        needed = income * min_savings_rate - savings

        advice.append(
            f"Your savings rate is **{savings_rate*100:.1f}%**. "
            f"Try increasing savings by about **₹{needed:,.0f}/month** "
            f"to reach the recommended **{int(min_savings_rate*100)}% rate**."
        )

    # ----------------------------
    # SIP Feasibility
    # ----------------------------
    if sip > savings:

        gap = sip - savings

        advice.append(
            f"The goal **'{goal_name}'** requires **₹{sip:,.0f}/month**, "
            f"but your current savings allow only **₹{savings:,.0f}**. "
            f"You're short by **₹{gap:,.0f}**."
        )

        advice.append(
            "Consider:\n"
            "• Increasing monthly savings\n"
            "• Extending the goal timeline\n"
            "• Reducing goal cost if possible"
        )

    # ----------------------------
    # Probability Advice
    # ----------------------------
    if probability < 0.5:

        advice.append(
            f"⚠️ The probability of achieving **'{goal_name}'** is only "
            f"**{probability*100:.1f}%**. "
            "Your plan may need adjustments."
        )

    elif probability < 0.8:

        advice.append(
            f"Your probability of achieving **'{goal_name}'** is "
            f"**{probability*100:.1f}%**. "
            "This is moderate — periodic review is recommended."
        )

    else:

        advice.append(
            f"✅ Great! The probability of achieving **'{goal_name}'** "
            f"is **{probability*100:.1f}%**, which is strong."
        )

    # ----------------------------
    # Balanced Plan Message
    # ----------------------------
    if len(advice) == 1 and probability >= 0.8 and sip <= savings:

        advice.append(
            f"Your financial strategy for **'{goal_name}'** looks well balanced."
        )

    return advice

