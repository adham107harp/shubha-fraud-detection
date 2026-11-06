# Contributing to Shubha

Short rules so the four of us can work in parallel without breaking each other's work. Read once, then follow.

## 1. Setup (once)

```
git clone https://github.com/adham107harp/shubha-fraud-detection.git
cd shubha-fraud-detection
pip install -r requirements.txt
pytest
```

`pytest` must pass before you start. Download PaySim from Kaggle into `data/raw/` yourself (see `data/README.md`).

## 2. Never commit these

- The raw CSV or anything in `data/raw/` or `data/processed/` (too big, and git-ignored).
- `.db` files, `__pycache__`, virtual environments, passwords or API keys.

If `git status` shows one of them, stop and tell Adham.

## 3. Daily workflow

1. Pick your issue (#1 to #4). Your branch name is written inside it.
2. Update `main`, then create your branch:
   ```
   git checkout main
   git pull
   git checkout -b your-branch-name
   ```
3. Work in small steps. Commit often.
4. Run `pytest` before every push.
5. Push and open a pull request into `main`:
   ```
   git push -u origin your-branch-name
   ```
6. Never push directly to `main`.

## 4. Commits

- One idea per commit, message in the present tense: `Add schema for transactions table`, `Fix division by zero in balance_share`.
- Avoid messages like `update`, `fix`, `final`, `asdf`.
- Commit your own work under your own name and email. Every member must have commits in the repo (it is graded).

## 5. Pull requests

- Title says what changed. The description says what you did and how to check it.
- Last line of the description: `Closes #N` (your issue number), so the issue closes when it is merged.
- A teammate (not the author) must review and approve before merging. Adham reviews too.
- Reviewer: read the code, run `pytest`, leave at least one comment or question. Do not approve what you do not understand.
- Author: answer every comment, push fixes to the same branch.

## 6. Code style

- Python 3.10+, clear names, short functions, a one-line docstring on each function.
- Code lives in `src/shubha/`, tests in `tests/` (file names start with `test_`).
- Notebooks go in `notebooks/` and must run top to bottom.
- Every new function that has logic gets a test. The project needs at least 10 tests in total.
- You must be able to explain every line you wrote at the viva. Do not paste code you do not understand.

## 7. Using AI tools

Allowed: explaining a concept, finding a bug, polishing text you wrote yourself. Not allowed: submitting code or text you do not understand, inventing data, or using AI during the viva. Note any use in `docs/ai_use_statement.md`.

## 8. Weekly rhythm

- Fri check-in, each person answers: what did I finish, what is blocked, what do I need.
- Adham updates `docs/progress_log.md` before the TA meeting.
- Stuck for more than 30 minutes? Ask in the group. Do not wait for Friday.

## 9. Deadlines

| Date | Milestone |
| --- | --- |
| 15 Nov | M2: data and database |
| 29 Nov | M3: statistics and AI prototype |
| 13 Dec | M4: integrated system |
| 20 Dec | M5: final delivery |
| 23 Dec | Demo day |

Late work loses 10% per day, so aim to finish a day early.
