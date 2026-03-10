from src.financial_engine import required_sip

def simulate_delay(goal_value, return_rate, years, delay):

    sip_now = required_sip(goal_value, return_rate, years)

    sip_delayed = required_sip(goal_value, return_rate, years - delay)

    return sip_now, sip_delayed 
