# app.py
import streamlit as st

TIER_THRESHOLD = 50_000.0
BASE_RATE = 0.10
UPPER_RATE = 0.15


def calculate_commission(sales: float) -> dict:
    """Return a breakdown of commission for a given sales amount."""
    base_portion = min(sales, TIER_THRESHOLD)
    upper_portion = max(sales - TIER_THRESHOLD, 0.0)

    base_commission = base_portion * BASE_RATE
    upper_commission = upper_portion * UPPER_RATE
    total = base_commission + upper_commission

    return {
        "base_portion": base_portion,
        "upper_portion": upper_portion,
        "base_commission": base_commission,
        "upper_commission": upper_commission,
        "total": total,
        "effective_rate": (total / sales) if sales > 0 else 0.0,
    }


st.set_page_config(page_title="Sales Commission Calculator", page_icon="💰")
st.title("💰 Sales Commission Calculator")
st.caption(
    f"{BASE_RATE:.0%} on sales up to ${TIER_THRESHOLD:,.0f}, "
    f"{UPPER_RATE:.0%} on the amount above."
)

sales = st.number_input(
    "Total sales ($)",
    min_value=0.0,
    value=0.0,
    step=1_000.0,
    format="%.2f",
)

result = calculate_commission(sales)

col1, col2 = st.columns(2)
col1.metric("Total commission", f"${result['total']:,.2f}")
col2.metric("Effective rate", f"{result['effective_rate']:.2%}")

st.subheader("Breakdown")
st.table(
    {
        "Tier": [
            f"First ${TIER_THRESHOLD:,.0f} @ {BASE_RATE:.0%}",
            f"Above ${TIER_THRESHOLD:,.0f} @ {UPPER_RATE:.0%}",
            "Total",
        ],
        "Sales in tier": [
            f"${result['base_portion']:,.2f}",
            f"${result['upper_portion']:,.2f}",
            f"${sales:,.2f}",
        ],
        "Commission": [
            f"${result['base_commission']:,.2f}",
            f"${result['upper_commission']:,.2f}",
            f"${result['total']:,.2f}",
        ],
    }
)
