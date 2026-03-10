def generate_advice(income, savings, sip, probability):

    advice = []

    if income == 0:
        return ["Income data missing."]

    savings_rate = savings / income

    # Savings advice
    if savings_rate < 0.2:
        advice.append("Try saving at least 20% of your monthly income.")

    # SIP feasibility
    if sip > savings:
        advice.append("Your goal requires higher investment than your current savings.")

    # Goal probability
    if probability < 0.6:
        advice.append("Goal probability is low. Consider increasing your timeline or investments.")

    if probability > 0.8:
        advice.append("Excellent! Your investment plan is strong.")

    if not advice:
        advice.append("Your financial plan looks balanced and achievable.")

    return advice