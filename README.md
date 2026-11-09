# Next Day SKU Sales Forecasting
ANLY 530 · KA1 Milestone 1. This repository contains a development-only feasibility audit for the same daily SKU sales series used in the course project. The full model comparison is planned for Milestone 2.

## Reproduce the audit
1. Use Python 3.12 and install dependencies: `python -m pip install -r requirements.txt`.
2. Save an authorized export locally as `data/sales.csv`, with one SKU/scope only and columns `date` (YYYY-MM-DD) and `units_sold` (nonnegative number or blank if unknown). Preserve genuine zero-sales days and the original final date.
3. Run `python audit_sales.py data/sales.csv`. If an original holdout boundary has already been fixed, pass `--holdout-start YYYY-MM-DD` to confirm it matches the final 60 calendar days.
4. Record the original source, SKU, scope, date range, extraction rules, and exclusions in a private data log. The script reports development quality checks and eligibility for five 28-day forward validation blocks; it does not train models or report reserved targets.

## Data policy
Do not commit sales data, company details, or credentials. The Git ignore file excludes local CSVs and data directories. Obtain permission before using the original data. M5 is a contingency benchmark only: https://www.kaggle.com/competitions/m5-forecasting-accuracy/data. If used, document the new series and boundary; do not present it as the original series.

## Contribution
Individual project. ChatGPT assisted with drafting and preparation of the audit script.
