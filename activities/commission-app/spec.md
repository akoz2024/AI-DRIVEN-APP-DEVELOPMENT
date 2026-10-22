Build a single-file Streamlit app (app.py, Python 3, Streamlit only plus the standard library) that calculates a salesperson's commission for one pay period.

INPUT
- One field: "Total sales for the period ($)". Use st.number_input with value=None and a placeholder, so the box starts blank. Do NOT set min_value; the app must check negatives itself so it can show a clear message.
- Valid input: a number from $0.00 to $10,000,000.00 inclusive, in dollars and cents. Treat sales as net sales (after returns) for one person in one period.

COMMISSION RULE (tiered / marginal, like tax brackets)
- 10% on the portion of sales from $0.00 up to and including $50,000.00.
- 15% only on the portion above $50,000.00.
- Formula: commission = 0.10 * min(sales, 50000) + 0.15 * max(sales - 50000, 0).
- Do NOT use the flat model where crossing $50,000 earns 15% on everything.
- Do the math with decimal.Decimal and round the final commission to the cent with ROUND_HALF_UP.
- Put the math in a pure function calculate_commission(sales: Decimal) -> Decimal that raises ValueError for negative sales, separate from the UI code.

EDGE CASES
- Blank box: show st.info("Enter a sales amount to calculate commission.") and no commission number.
- $0: valid; commission $0.00. Do not show an effective rate for $0.
- Negative: show st.error("Sales can't be negative. Enter returns as a reduction to net sales, not as a negative period.") and no commission number.
- Above $10,000,000: show st.error saying the amount is over the $10,000,000 limit and to double-check it; no commission number.

OUTPUT
- st.metric "Commission" formatted like $9,500.00.
- Below it, a breakdown in plain text: amount at 10% and its commission, amount at 15% and its commission.
- Escape dollar signs in any Markdown text (st.caption, st.write, st.markdown) as \$ so Streamlit doesn't render them as LaTeX.

WORKED EXAMPLES THE APP MUST MATCH EXACTLY
| Sales | Commission |
| $40,000 | $4,000.00 |
| $50,000 | $5,000.00 |
| $50,001 | $5,000.15 |
| $80,000 | $9,500.00 |
| $0 | $0.00 |
| -$5,000 | error message, no commission |
| blank | info message, no commission |

Return the complete app.py in one code block.
