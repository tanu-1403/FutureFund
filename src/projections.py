def investment_projection(sip, annual_return, years):

    r = annual_return / 12
    months = years * 12

    value = 0
    portfolio = []

    for i in range(months):

        value = value * (1 + r) + sip
        portfolio.append(value)

    return portfolio