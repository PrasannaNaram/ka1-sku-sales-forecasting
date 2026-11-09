"""Audit an authorized daily SKU series; never summarize reserved outcomes."""
import argparse
import numpy as np
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv")
    parser.add_argument("--holdout-start")
    args = parser.parse_args()
    source = pd.read_csv(args.csv, usecols=["date", "units_sold"], dtype={"date": str})
    dates = pd.to_datetime(source["date"], format="%Y-%m-%d", errors="raise")
    if dates.empty or dates.isna().any():
        parser.error("Input must contain valid calendar dates.")
    stop = dates.max() - pd.Timedelta(days=59)
    if args.holdout_start and stop != pd.Timestamp(args.holdout_start):
        parser.error("Reserved boundary does not match; verify the original file and dates.")
    dev = source.loc[dates < stop].copy()
    dev["date"] = dates.loc[dev.index]
    if dev.empty or dev["date"].duplicated().any():
        parser.error("Development data are empty or contain duplicate dates.")
    y = pd.to_numeric(dev.set_index("date")["units_sold"], errors="coerce")
    bad = y.notna() & (~np.isfinite(y) | (y < 0))
    if bad.any():
        parser.error("Resolve negative or infinite development values before analysis.")
    calendar = pd.date_range(y.index.min(), stop - pd.Timedelta(days=1))
    missing_dates = len(calendar.difference(y.index))
    missing_values = int(y.isna().sum())
    y = y.reindex(calendar)
    if len(y) < 5 * 28 + 35:
        parser.error("Need at least five validation blocks and 35 earlier calendar days.")
    eligible = y.notna() & y.shift(1).rolling(7, min_periods=7).count().eq(7)
    print(f"Development: {calendar[0].date()} through {calendar[-1].date()}")
    print(f"Reserved start: {stop.date()} (60 calendar days; outcomes not audited)")
    print(f"Missing dates: {missing_dates}; missing or invalid recorded values: {missing_values}")
    print(f"Observed zero sales: {y.eq(0).sum()}; eligible development days: {eligible.sum()}")
    for i in range(5):
        start = len(calendar) - (5 - i) * 28
        end = start + 28
        print(f"Fold {i+1}: {calendar[start].date()} to {calendar[end-1].date()}, "
              f"eligible train={eligible.iloc[:start].sum()}, "
              f"eligible validation={eligible.iloc[start:end].sum()}")

if __name__ == "__main__":
    main()
