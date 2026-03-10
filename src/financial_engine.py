
import numpy as np

def future_income(current_income, growth_rate, years):
    return current_income * (1 + growth_rate) ** years


def savings_projection(income, savings_rate, years):
    return income * savings_rate * years