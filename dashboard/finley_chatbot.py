"""
FutureFund – Finley AI Assistant
Rule-based + pattern-matched chatbot that provides contextual
financial guidance based on the user's profile and goals.
"""
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import re
from utils.helpers import fmt_inr, fmt_pct


class FinleyBot:
    """
    Finley: FutureFund's friendly AI financial assistant.
    Provides illustrative, educational guidance — not professional advice.
    """

    GREETING_PATTERNS = [
        r"\b(hi|hello|hey|howdy|sup|yo)\b",
    ]
    CAR_PATTERNS      = [r"\bcar\b", r"\bvehicle\b", r"\bauto\b"]
    HOUSE_PATTERNS    = [r"\bhouse\b", r"\bhome\b", r"\bproperty\b", r"\bflat\b"]
    EDU_PATTERNS      = [r"\beducation\b", r"\bcollege\b", r"\bmba\b", r"\bstudy\b", r"\bdegree\b"]
    SAVE_PATTERNS     = [r"\bsave\b", r"\bsaving\b", r"\bsavings\b"]
    INVEST_PATTERNS   = [r"\binvest\b", r"\binvestment\b", r"\bsip\b", r"\bmutual fund\b"]
    RETIRE_PATTERNS   = [r"\bretire\b", r"\bretirement\b", r"\bpension\b"]
    AFFORD_PATTERNS   = [r"\bafford\b", r"\bcan i\b", r"\bbudget\b"]
    INFLATION_PATTERNS= [r"\binflation\b"]
    HELP_PATTERNS     = [r"\bhelp\b", r"\bwhat can you do\b", r"\bcommands\b"]
    THANKS_PATTERNS   = [r"\bthank\b", r"\bthanks\b", r"\bthx\b", r"\bgreat\b"]

    def __init__(self):
        self.profile = {}
        self.goals   = []

    def update_context(self, profile: dict, goals: list):
        self.profile = profile
        self.goals   = goals

    def _match(self, text: str, patterns: list) -> bool:
        text = text.lower()
        return any(re.search(p, text) for p in patterns)

    def respond(self, user_input: str) -> str:
        txt = user_input.strip().lower()

        # ── Greetings ──────────────────────────────────────────────────
        if self._match(txt, self.GREETING_PATTERNS):
            name_hint = ""
            return (
                f"Hey there! 👋 I'm Finley, your personal finance buddy! "
                f"I can help you understand your savings, goals, SIP requirements, "
                f"and more. What's on your mind today?"
            )

        # ── Help ───────────────────────────────────────────────────────
        if self._match(txt, self.HELP_PATTERNS):
            return (
                "I can help with:\n"
                "• **How much should I save?**\n"
                "• **Can I afford a car / house?**\n"
                "• **What is SIP?**\n"
                "• **What is inflation doing to my goals?**\n"
                "• **When can I retire?**\n"
                "• **How are my investments growing?**\n\n"
                "Just ask naturally — I'll do my best! 🤖"
            )

        # ── Thanks ─────────────────────────────────────────────────────
        if self._match(txt, self.THANKS_PATTERNS):
            return "Happy to help! 😊 Ask me anything else about your financial journey."

        # ── Savings ────────────────────────────────────────────────────
        if self._match(txt, self.SAVE_PATTERNS):
            income  = self.profile.get("monthly_income", 0)
            savings = self.profile.get("monthly_savings", 0)
            if income > 0:
                rate = (savings / income) * 100
                ideal = income * 0.20
                msg = (
                    f"You're currently saving **{fmt_inr(savings)}/month** "
                    f"({rate:.1f}% of income). "
                )
                if rate < 10:
                    msg += (
                        f"That's a bit low. Financial planners often suggest the **50/30/20 rule** — "
                        f"aim for at least 20% ({fmt_inr(ideal)}/month). "
                        f"Even small increases compound significantly over time! 📈"
                    )
                elif rate < 20:
                    msg += (
                        f"Good start! Pushing to **20%** ({fmt_inr(ideal)}/month) "
                        f"would put you on a stronger footing. 💪"
                    )
                else:
                    msg += "Excellent savings discipline! You're ahead of most people. 🎉"
                return msg
            return (
                "Fill in your **Monthly Income** in the Profile panel on the right, "
                "and I'll give you personalised savings advice! 👉"
            )

        # ── Car ────────────────────────────────────────────────────────
        if self._match(txt, self.CAR_PATTERNS):
            car_goals = [g for g in self.goals if "car" in g.get("category", "").lower()
                         or "car" in g.get("name", "").lower()]
            if car_goals:
                g = car_goals[0]
                return (
                    f"Your **{g['name']}** goal is set for "
                    f"{fmt_inr(g['cost'])} in **{g['years']} years**. "
                    f"Check your dashboard for the inflation-adjusted cost and required SIP. "
                    f"Pro tip: Consider a **recurring deposit or liquid fund** for short-term car goals! 🚗"
                )
            return (
                "A car is typically a **short-to-medium term goal** (1–5 years). "
                "Add it in the Goal Notebook on the left, and I'll show you exactly how much to save monthly! 🚗"
            )

        # ── House ──────────────────────────────────────────────────────
        if self._match(txt, self.HOUSE_PATTERNS):
            return (
                "Buying a home is one of the biggest financial decisions! 🏠\n\n"
                "**Key rules of thumb:**\n"
                "• Down payment = 20% of property value\n"
                "• EMI should be ≤ 40% of take-home pay\n"
                "• Build a 6-month emergency fund first\n\n"
                "Add your home goal in the Goal Notebook and I'll calculate your SIP target! "
                f"Your current monthly savings: **{fmt_inr(self.profile.get('monthly_savings', 0))}**"
            )

        # ── Education ─────────────────────────────────────────────────
        if self._match(txt, self.EDU_PATTERNS):
            inflation = self.profile.get("inflation_rate", 6)
            return (
                f"Education costs in India are rising at ~**10–12% per year** — "
                f"much faster than general inflation ({inflation}%). "
                f"Set your inflation assumption to **10–12%** for education goals. 🎓\n\n"
                f"Consider **Sukanya Samriddhi (for girls), PPF, or equity mutual funds** "
                f"depending on the time horizon!"
            )

        # ── Retirement ────────────────────────────────────────────────
        if self._match(txt, self.RETIRE_PATTERNS):
            income  = self.profile.get("monthly_income", 0)
            returns = self.profile.get("annual_return", 12)
            return (
                f"Retirement planning is all about **starting early**! ⏰\n\n"
                f"The **25x Rule**: You need ~25× your annual expenses as a retirement corpus.\n"
                f"With an assumed return of **{returns}%**, money doubles every "
                f"**{round(72/returns, 1)} years** (Rule of 72).\n\n"
                f"Add a retirement goal in the Notebook and run the **Lifetime Wealth** simulation!"
            )

        # ── Invest / SIP ──────────────────────────────────────────────
        if self._match(txt, self.INVEST_PATTERNS):
            returns = self.profile.get("annual_return", 12)
            savings = self.profile.get("monthly_savings", 0)
            return (
                f"**SIP (Systematic Investment Plan)** is a disciplined way to invest monthly "
                f"in mutual funds. 📊\n\n"
                f"At your assumed return of **{returns}% p.a.**, investing "
                f"**{fmt_inr(savings)}/month** for:\n"
                f"• 10 years → "
                f"**{fmt_inr(_sip_fv(savings, returns, 10), short=True)}**\n"
                f"• 20 years → "
                f"**{fmt_inr(_sip_fv(savings, returns, 20), short=True)}**\n"
                f"• 30 years → "
                f"**{fmt_inr(_sip_fv(savings, returns, 30), short=True)}**\n\n"
                f"That's the magic of compounding! ✨"
            )

        # ── Inflation ─────────────────────────────────────────────────
        if self._match(txt, self.INFLATION_PATTERNS):
            inf = self.profile.get("inflation_rate", 6)
            return (
                f"At **{inf}% inflation**, money's purchasing power halves every "
                f"**{round(70/inf, 1)} years** (Rule of 70). 📉\n\n"
                f"This is why we **inflate your goal costs** before calculating SIP — "
                f"₹10 lakh today costs more in the future!\n\n"
                f"FutureFund automatically adjusts all your goals for inflation."
            )

        # ── Affordability ────────────────────────────────────────────
        if self._match(txt, self.AFFORD_PATTERNS):
            savings = self.profile.get("monthly_savings", 0)
            if not self.goals:
                return (
                    "Add some goals in the **Goal Notebook** first, and I'll tell you "
                    "exactly which ones fit your budget! 📝"
                )
            from src.financial_engine import future_value, required_sip
            inf = self.profile.get("inflation_rate", 6)
            ret = self.profile.get("annual_return", 12)
            lines = []
            for g in self.goals[:3]:
                fv  = future_value(g["cost"], inf, g["years"])
                sip = required_sip(fv, ret, g["years"])
                pct = (sip / savings * 100) if savings > 0 else 999
                status = "✅" if pct <= 50 else ("⚠️" if pct <= 100 else "🔴")
                lines.append(f"{status} **{g['name']}**: {fmt_inr(sip)}/mo ({pct:.0f}% of savings)")
            return (
                f"Here's your affordability check:\n\n"
                + "\n".join(lines)
                + f"\n\n*(Based on monthly savings of {fmt_inr(savings)})*"
            )

        # ── Default ───────────────────────────────────────────────────
        return (
            "Hmm, I'm still learning! 🤔 Try asking me:\n"
            "• *How much should I save?*\n"
            "• *Can I afford a house?*\n"
            "• *What is SIP?*\n"
            "• *Tell me about inflation*"
        )


def _sip_fv(monthly_sip, annual_return, years):
    import math
    r = (annual_return / 100) / 12
    n = years * 12
    if r == 0 or monthly_sip == 0:
        return monthly_sip * n
    return monthly_sip * ((math.pow(1 + r, n) - 1) / r) * (1 + r)


def fmt_inr(value: float, short: bool = False) -> str:
    v = abs(value)
    sign = "-" if value < 0 else ""
    if short:
        if v >= 1e7: return f"{sign}₹{v/1e7:.2f} Cr"
        if v >= 1e5: return f"{sign}₹{v/1e5:.2f} L"
        if v >= 1e3: return f"{sign}₹{v/1e3:.1f} K"
    if v >= 1e7: return f"{sign}₹{v/1e7:.2f} Cr"
    if v >= 1e5: return f"{sign}₹{v/1e5:.2f} L"
    return f"{sign}₹{v:,.0f}"
