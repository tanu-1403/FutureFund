from datetime import datetime, timedelta

def investment_projection(sip, annual_return, years, inflation=0.06, start_date=None):
    """
    Projects investment growth over time with compounding and optional inflation adjustment.

    Parameters:
        sip : float : Monthly investment
        annual_return : float : Expected annual return (decimal, e.g., 0.08 for 8%)
        years : int : Investment horizon in years
        inflation : float : Expected annual inflation rate (default 6%)
        start_date : datetime : Optional start date for projection

    Returns:
        list of dicts : Each dict has month, nominal portfolio, inflation-adjusted portfolio
    """
    r = annual_return / 12
    months = years * 12
    portfolio_value = 0
    projections = []

    # Set start date
    if not start_date:
        start_date = datetime.today()

    for i in range(1, months + 1):
        portfolio_value = portfolio_value * (1 + r) + sip
        # Calculate inflation-adjusted value
        inflation_adjusted_value = portfolio_value / ((1 + inflation) ** (i / 12))
        month_date = start_date + timedelta(days=30 * i)
        projections.append({
            "month": month_date,
            "nominal": portfolio_value,
            "real_value": inflation_adjusted_value
        })

    return projections