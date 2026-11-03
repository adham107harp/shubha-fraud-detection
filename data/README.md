# Data

Source: PaySim synthetic mobile-money dataset, Kaggle `ealaxi/paysim1`.
Download the CSV into `data/raw/` (it is git-ignored). Cleaned data goes in `data/processed/`.

## Data dictionary (to be completed at M2)

| Variable | Description |
| --- | --- |
| step | Hour of simulation |
| type | Transaction type |
| amount | Transaction amount |
| nameOrig | Sender ID |
| oldbalanceOrg | Sender balance before |
| newbalanceOrig | Sender balance after |
| nameDest | Receiver ID |
| oldbalanceDest | Receiver balance before |
| newbalanceDest | Receiver balance after |
| isFraud | 1 if fraud |
| isFlaggedFraud | 1 if flagged by the simulator's rule |
