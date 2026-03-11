def generate_advice(goal_name, income, savings, sip, probability, min_savings_rate=0.2):
    """
    Generates personalized financial advice for a specific goal.

    Parameters:
        goal_name : str : Name of the goal
        income : float : Monthly income
        savings : float : Monthly savings available
        sip : float : Monthly investment required for the goal
        probability : float : Probability of achieving the goal (0-1)
        min_savings_rate : float : Minimum recommended savings rate (default 20%)

    Returns:
        list of str : Advice messages
    """
    advice = []

    if income <= 0:
        return [f"Income data missing for goal '{goal_name}'."]
    
    savings_rate = savings / income

    # Savings rate advice
    if savings_rate < min_savings_rate:
        advice.append(f"Try saving at least {int(min_savings_rate*100)}% of your monthly income for '{goal_name}'.")

    # SIP feasibility
    if sip > savings:
        advice.append(f"Your goal '{goal_name}' requires a higher investment than your current monthly savings. Consider adjusting your plan or extending the timeline.")

    # Goal probability advice
    if probability < 0.6:
        advice.append(f"The probability of achieving '{goal_name}' is low. Consider increasing your timeline or monthly investment.")
    elif probability > 0.8:
        advice.append(f"Excellent! Your investment plan for '{goal_name}' is strong.")
    else:
        advice.append(f"Your plan for '{goal_name}' is reasonable but monitor regularly and adjust as needed.")

    # Default advice if nothing triggered
    if not advice:
        advice.append(f"Your financial plan for '{goal_name}' looks balanced and achievable.")

    return advice