# Shubha roadmap

Shubha is a fraud-triage tool for mobile-wallet companies. A fraud analyst cannot review millions of transactions, so Shubha ranks them by risk, explains each alert, and learns from the analyst's decisions.

## Now (course project, Fall 2026)

- Scoring service: `POST /score` takes a transaction and returns the fraud probability, a verdict and the reasons.
- Analyst console, 3 features only:
  1. Alert queue, ranked by risk, with the reason for each alert.
  2. Threshold slider that shows precision, recall, F1 and the number of daily alerts live.
  3. Analyst decision (fraud / legitimate) saved in the database.
- Naive Bayes written from scratch plus explicit rules, compared against two baselines.
- Every prediction is logged with `model_version`.

## Next

- Retrain the model from the analysts' saved decisions (the feedback loop).
- Stronger models behind the same interface (`fit`, `predict_proba`, `save`, `load`).
- Different thresholds per client company.
- Alert reasons in Arabic.
- Replay mode: play the data in `step` order as if it were live.

## Later

- Real-time streaming instead of batch scoring.
- A mobile app for analysts.
- Integration with real wallet APIs.
- Privacy and licensing review before using real customer data.

## Honest limits

- PaySim is synthetic and not Egyptian. Results on it do not prove the system works on real data.
- The system flags transactions for human review. It never blocks a payment by itself.
