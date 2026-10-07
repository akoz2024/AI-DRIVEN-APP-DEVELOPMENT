# AI-Driven App Development — Classwork Repository

**Alexander Kozin** · Babson College · OIM 3641, Fall 2026

This repository holds my coursework, in-class activities, and project milestones for
**AI-Driven App Development**. Each assignment lives in its own folder with the notebook
or application code, plus any data needed to reproduce the results.

---

## About Me

I'm a Babson College student finishing my degree in December 2026. I work in private
equity at Dover Capital, across a portfolio of distressed B2B SaaS companies — turnaround
situations where the operating data is scattered across Salesforce, QuickBooks, and a
dozen other systems, and nobody fully trusts any of it. My job is to fix that: I build the
data pipelines and internal tools that reconcile those systems and turn them into
something an operator can actually act on — revenue and churn reconciliation, customer
health scoring, and AI-driven workflows that replace manual reporting.

I'm taking this course to go from *scripts that answer a question* to *applications other
people can use* — LLM-backed apps, clean interfaces, and deployment that doesn't require me
to be in the room.

---

## Skills & Tools

**Languages**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=flat&logo=postgresql&logoColor=white)
![Markdown](https://img.shields.io/badge/Markdown-000000?style=flat&logo=markdown&logoColor=white)

**Libraries & Frameworks**

![pandas](https://img.shields.io/badge/pandas-150458?style=flat&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat&logo=scikitlearn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)

**Tools & Platforms**

![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat&logo=jupyter&logoColor=white)
![VS Code](https://img.shields.io/badge/VS%20Code-007ACC?style=flat&logo=visualstudiocode&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)

| Area | What I use |
| --- | --- |
| Data wrangling | pandas, NumPy, SQL |
| Modeling | scikit-learn |
| Apps & APIs | Streamlit, FastAPI, REST APIs |
| Version control | Git, GitHub |
| Environments | Jupyter, VS Code, virtualenv |

---

## Directory Structure

```
AI-DRIVEN-APP-DEVELOPMENT/
├── README.md                 # This file
├── .gitignore                # Excludes secrets, venvs, and build output
├── notebooks/                # In-class activities and prework notebooks
│   ├── 02-python_concepts.ipynb
│   └── user.py
├── activities/               # In-class activity apps
│   └── rag-chatbot/          # Activities 10–11: RAG chatbot over the student handbook
│       ├── app.py            #   uv run streamlit run app.py
│       └── data/             #   Babson undergraduate student handbook (PDF)
├── assignments/              # Graded individual assignments
│   └── assignment-1/         # Stock Analysis Streamlit app (OOP + Streamlit)
│       ├── assignment_1.py   #   streamlit run assignment_1.py
│       ├── stock.py
│       ├── demo_modified.py
│       └── analysis.docx
├── projects/                 # Team project milestones (one folder per milestone)
├── data/                     # Small sample datasets used by the notebooks
└── requirements.txt          # Python dependencies for the repo
```

Folders are added as the course progresses. Anything sensitive — API keys, credentials,
`.env` files — is excluded by `.gitignore` and never committed.

---

## Install & Run

### 1. Clone the repository

```bash
git clone https://github.com/akoz2024/AI-DRIVEN-APP-DEVELOPMENT.git
cd AI-DRIVEN-APP-DEVELOPMENT
```

### 2. Create and activate a virtual environment

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` isn't present yet, the notebooks only need the core stack:

```bash
pip install jupyter pandas numpy scikit-learn streamlit
```

### 4. Open the notebooks

```bash
jupyter lab          # or: jupyter notebook
```

### 5. Run a Streamlit app (for later projects)

```bash
streamlit run projects/<milestone>/app.py
```

---

## Contact & Connect

- **LinkedIn** — [linkedin.com/in/alex-kozin04](https://www.linkedin.com/in/alex-kozin04/)
- **GitHub** — [@akoz2024](https://github.com/akoz2024)
- **Email** — [akozin@intelliboard.net](mailto:akozin@intelliboard.net)

---

<sub>Babson College · OIM 3641 — AI-Driven App Development · Fall 2026</sub>
