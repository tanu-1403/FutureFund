
from datetime import datetime
from dateutil.relativedelta import relativedelta


def investment_projection(
    sip,
    annual_return,
    years,
    inflation=0.06,
    sip_growth=0.0,
    start_date=None
):
    """
    Project investment growth over time with compounding and inflation adjustment.

    Parameters
    ----------
    sip : float
        Monthly investment
    annual_return : float
        Expected annual return (decimal)
    years : int
        Investment horizon
    inflation : float
        Annual inflation rate
    sip_growth : float
        Optional annual increase in SIP
    start_date : datetime
        Optional start date

    Returns
    -------
    list[dict]
        Monthly portfolio projections
    """

    # -----------------------------
    # Input validation
    # -----------------------------
    sip = float(sip)
    annual_return = float(annual_return)
    years = int(years)

    if sip < 0:
        raise ValueError("SIP must be non-negative")

    if years <= 0:
        raise ValueError("Years must be positive")

    if not start_date:
        start_date = datetime.today()

    months = years * 12
    monthly_return = annual_return / 12
    monthly_inflation = (1 + inflation) ** (1/12) - 1

    portfolio = 0
    projections = []

    current_sip = sip

    # -----------------------------
    # Projection loop
    # -----------------------------
    for m in range(1, months + 1):

        portfolio = portfolio * (1 + monthly_return) + current_sip

        # inflation-adjusted value
        real_value = portfolio / ((1 + monthly_inflation) ** m)

        projections.append({

            "date": start_date + relativedelta(months=m),

            "nominal": round(portfolio, 2),

            "real_value": round(real_value, 2),

            "sip": round(current_sip, 2)

        })

        # yearly SIP increase
        if sip_growth > 0 and m % 12 == 0:
            current_sip *= (1 + sip_growth)

    return projections

