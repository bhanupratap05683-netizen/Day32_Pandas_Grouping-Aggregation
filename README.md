# Day 32 — GroupBy & Aggregation with pandas

**Date:** May 7, 2026 | **Phase:** 2 — pandas Basics | **Roadmap:** 84-Day Python & Excel Mastery

---

## Overview

Practiced the core pandas `groupby` workflow on a 30-row financial sales dataset (Region × Salesperson × Product Category). Built 10 progressively complex aggregations that mirror real finance analyst tasks.

---

## Files

| File | Description |
|---|---|
| `Day32_Sales_Data.xlsx` | Input dataset — 30 sales records, 4 regions, 4 product categories |
| `day32_groupby_aggregation.py` | Practice script — 10 groupby patterns with detailed comments |
| `Day32_GroupBy_Output.xlsx` | Exported results — 3 sheets: Salesperson Summary, Region Revenue, Category Report |

---

## Concepts Covered

- `groupby("col")` — split DataFrame into groups by a column
- `.sum()`, `.mean()`, `.count()`, `.min()`, `.max()` — basic aggregation functions
- Multi-column groupby — `groupby(["col1", "col2"])`
- `.agg()` with named output — compute multiple stats in one step
- `reset_index()` — flatten MultiIndex back to regular columns
- `as_index=False` — shortcut to skip reset_index
- `sort_values()` after groupby — rank results
- `.query()` after groupby — filter aggregated results
- `lambda` in `.agg()` — custom aggregation logic
- `pd.ExcelWriter` — multi-sheet export

---

## Key Output (Category Report)

| Category | Deals | Total Revenue | Avg Margin |
|---|---|---|---|
| Insurance | 7 | ₹10,28,000 | 25.64% |
| Mutual Fund | 7 | ₹10,02,000 | 22.00% |
| Equity | 10 | ₹5,60,000 | 17.75% |
| Bonds | 6 | ₹3,70,500 | 12.00% |

---

## Portfolio Connection

The `.agg()` pattern + multi-sheet export is the exact engine behind the **Financial Dashboard** (Day 78) — grouping portfolio holdings by sector, asset class, or time period to generate summary reports automatically.

---

## Status

✅ Completed | Next: **Day 33 — Merging & Combining Data**
