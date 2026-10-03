# Assignment 1: Stock Analysis Streamlit App

OIM 3641 AI-Driven App Development, Fall 2026 · Alexander Kozin

A two-tab Streamlit app built on the `Stock` class from class. `stock.py` owns the data
(download, daily change, log returns, moving averages, plots). `assignment_1.py` owns the interface.

| File | What it is |
| --- | --- |
| `assignment_1.py` | The app: Single Stock Analysis and Portfolio Comparison tabs |
| `stock.py` | The `Stock` class, extended with an optional `long_window` second moving average |
| `06-streamlit-demo.py` | The in-class demo before any changes (for comparison; the plotting half was rebuilt from the assignment description) |
| `demo_modified.py` | The demo with a second moving average added |
| `analysis.docx` | Reflection answers and the MSFT vs JPM portfolio write-up |
| `screenshots/` | App screenshots used in the analysis |

## Run

```bash
cd assignments/assignment-1
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run assignment_1.py
```
