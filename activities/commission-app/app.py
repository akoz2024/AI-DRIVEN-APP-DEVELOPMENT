"""Sales commission calculator (single pay period).

Run with:  streamlit run app.py
"""

from decimal import Decimal, ROUND_HALF_UP

import streamlit as st

# ---------------------------------------------------------------------------
# Business rules
# ---------------------------------------------------------------------------

TIER_THRESHOLD = Decimal("50000.00")
TIER_1_RATE = Decimal("0.10")
TIER_2_RATE = Decimal("0.15")
MAX_SALES = Decimal("10000000.00")
CENT = Decimal("0.01")


def to_cents(amount: Decimal) -> Decimal:
    """Round a Decimal to the cent using ROUND_HALF_UP."""
    return amount.quantize(CENT, rounding=ROUND_HALF_UP)


def split_tiers(sales: Decimal) -> tuple[Decimal, Decimal]:
    """Return (amount taxed at tier 1, amount taxed at tier 2)."""
    if sales < 0:
        raise ValueError("Sales cannot be negative.")
    tier_1_amount = min(sales, TIER_THRESHOLD)
    tier_2_amount = max(sales - TIER_THRESHOLD, Decimal("0"))
    return tier_1_amount, tier_2_amount


def calculate_commission(sales: Decimal) -> Decimal:
    """Tiered (marginal) commission for one pay period.

    10% on the portion of sales up to and including $50,000.00,
    15% only on the portion above $50,000.00.
    Result is rounded to the cent with ROUND_HALF_UP.

    Raises ValueError for negative sales.
    """
    if sales < 0:
        raise ValueError("Sales cannot be negative.")
    tier_1_amount, tier_2_amount = split_tiers(sales)
    commission = TIER_1_RATE * tier_1_amount + TIER_2_RATE * tier_2_amount
    return to_cents(commission)


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def money(amount: Decimal) -> str:
    """Plain dollar formatting, e.g. $9,500.00 (for non-Markdown widgets)."""
    return f"${amount:,.2f}"


def md_money(amount: Decimal) -> str:
    """Dollar formatting with the $ escaped for Markdown-rendered text."""
    return f"\\${amount:,.2f}"


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

def main() -> None:
    st.set_page_config(page_title="Commission Calculator", page_icon="💵")
    st.title("Sales Commission Calculator")
    st.caption(
        "10% on net sales up to \\$50,000.00, plus 15% on the portion above "
        "\\$50,000.00. Enter net sales (after returns) for one person in one "
        "pay period."
    )

    raw_sales = st.number_input(
        "Total sales for the period ($)",
        value=None,
        step=0.01,
        format="%.2f",
        placeholder="e.g. 80000.00",
    )

    # Blank box
    if raw_sales is None:
        st.info("Enter a sales amount to calculate commission.")
        return

    # Convert via str() to avoid binary float artifacts, then round to cents.
    sales = to_cents(Decimal(str(raw_sales)))

    # Negative
    if sales < 0:
        st.error(
            "Sales can't be negative. Enter returns as a reduction to net "
            "sales, not as a negative period."
        )
        return

    # Above limit
    if sales > MAX_SALES:
        st.error(
            f"{md_money(sales)} is over the \\$10,000,000 limit. "
            "Please double-check the amount."
        )
        return

    commission = calculate_commission(sales)
    tier_1_amount, tier_2_amount = split_tiers(sales)
    tier_1_commission = to_cents(TIER_1_RATE * tier_1_amount)
    tier_2_commission = to_cents(TIER_2_RATE * tier_2_amount)

    st.metric("Commission", money(commission))

    st.markdown(
        f"**Breakdown**  \n"
        f"{md_money(tier_1_amount)} at 10% = {md_money(tier_1_commission)}  \n"
        f"{md_money(tier_2_amount)} at 15% = {md_money(tier_2_commission)}"
    )

    # Effective rate only makes sense for positive sales.
    if sales > 0:
        effective_rate = (commission / sales * 100).quantize(
            CENT, rounding=ROUND_HALF_UP
        )
        st.caption(f"Effective commission rate: {effective_rate}%")


if __name__ == "__main__":
    main()
