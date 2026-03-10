import numpy as np

def future_goal_value(cost, inflation, years):

    return cost * (1 + inflation) ** years


def required_sip(future_value, annual_return, years):

    r = annual_return / 12
    n = years * 12

    sip = (future_value * r) / (((1 + r) ** n - 1) * (1 + r))

    return sip
    
    