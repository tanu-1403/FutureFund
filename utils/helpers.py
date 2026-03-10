def format_currency(x):

    return f"₹{x:,.0f}"


def generate_insight(sip_now, sip_later):

    diff = ((sip_later - sip_now) / sip_now) * 100

    return f"Delaying investment increases required SIP by {diff:.1f}%"