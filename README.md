# Shubha — Mobile-Wallet Fraud Detection

Integrated Mega Project, Fall 2026 — School of Computing and Data Science, Badya University.
Courses: CS 312 Programming with Python, AI 306 Probability and Statistics for Data Science, CO 208 Introduction to AI.

Shubha screens mobile-money transactions and flags suspicious ones, with the reasons behind each flag. It combines a Naive Bayes classifier (implemented from scratch) with logic-based rules, and is evaluated against a "never fraud" baseline using precision, recall and F1.

## Team

| Member | ID | Lead role |
| --- | --- | --- |
| Adham Mohamed | 2400517 | Project manager + Quality and documentation lead |
| Fathy Ahmed | 2400740 | Data and statistics lead |
| Nasr Yousef | 2400825 | AI lead |
| Abdelrahman Ahmed | 2400736 | Database and web lead |

Supervisors: Dr. Ghada Khoriba, Dr. Amal Foad, Dr. Abdulla Mamdouh.

## Data

PaySim synthetic mobile-money dataset (Kaggle: `ealaxi/paysim1`). Place the downloaded CSV in `data/raw/` (not committed). See `data/README.md` for the data dictionary once it is written.

## Requirements

Python 3.10 or later.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Running

Instructions for the pipeline, the web app and the tests will be added as each milestone is delivered.

```bash
pytest                          # run the automated tests
```

## Repository layout

```
README.md          Installation and execution instructions
requirements.txt   Python dependencies
data/              Raw and cleaned data + data dictionary
notebooks/         EDA and statistical analysis
src/shubha/        Python package: pipeline, AI component, web app
tests/             Automated tests (pytest)
docs/              Proposal, diagrams, report, AI-use statement, progress log
```

## Architecture

Three layers, kept separate on purpose so each can be replaced later.

```
Analyst console (Flask pages)  -->  Scoring API (POST /score)  -->  Model (NaiveBayes + rules)
                                              |
                                              v
                                   SQLite: transactions, alerts, analyst decisions
```

- **Model** (`src/shubha/ai/`): a class with `fit`, `predict_proba`, `predict`, `save`, `load`. Swapping in another model must not change the other layers.
- **API** (`src/shubha/web/`): `POST /score` receives a transaction and returns `{probability, verdict, reasons, model_version}`.
- **Console** (`src/shubha/web/`): pages call the API like any other client.
- **Database** (`src/shubha/db/schema.sql`): every prediction is logged with `model_version`, and the analyst's decision is stored next to it. These decisions are the training data for future models.

## Workflow

- One-week sprints on GitHub Projects.
- Work on a branch, open a pull request, get a review from a teammate, then merge.
- Every member commits their own work.
