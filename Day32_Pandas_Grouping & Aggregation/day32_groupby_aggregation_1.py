"""
Day 32: GroupBy & Aggregation with pandas
Finance Dataset: Sales performance across regions, products, and salespersons
"""

import pandas as pd

# ─────────────────────────────────────────────
# SECTION 0: Load Data
# ─────────────────────────────────────────────
df = pd.read_excel("Day32_Sales_Data.xlsx")
df["Date"] = pd.to_datetime(df["Date"])

print("=" * 55)
print("DATASET OVERVIEW")
print("=" * 55)
print(df.head(5))
print(f"\nShape: {df.shape}")

# ─────────────────────────────────────────────
# SECTION 1: Basic groupby — single column
# ─────────────────────────────────────────────
# groupby("column") splits the DataFrame into groups
# .sum() / .mean() / .count() collapses each group into 1 row

print("\n" + "=" * 55)
print("1. TOTAL REVENUE BY REGION")
print("=" * 55)
region_revenue = df.groupby("Region")["Revenue"].sum()
print(region_revenue)
# Output → Region name : Total Revenue (one row per unique Region)

print("\n" + "=" * 55)
print("2. AVERAGE PROFIT MARGIN BY PRODUCT CATEGORY")
print("=" * 55)
cat_margin = df.groupby("Product_Category")["Profit_Margin_%"].mean().round(2)
print(cat_margin)

# ─────────────────────────────────────────────
# SECTION 2: groupby on multiple columns
# ─────────────────────────────────────────────
# Pass a LIST of columns → creates a MultiIndex result
print("\n" + "=" * 55)
print("3. REVENUE BREAKDOWN: REGION × PRODUCT CATEGORY")
print("=" * 55)
region_cat = df.groupby(["Region", "Product_Category"])["Revenue"].sum()
print(region_cat)
# Output has a 2-level index: (Region, Product_Category) → Revenue

# ─────────────────────────────────────────────
# SECTION 3: .agg() — multiple stats at once
# ─────────────────────────────────────────────
# Instead of calling .sum() alone, pass a DICT to compute several stats in one shot
print("\n" + "=" * 55)
print("4. SALESPERSON PERFORMANCE SUMMARY")
print("=" * 55)
sales_summary = df.groupby("Salesperson").agg(
    Total_Revenue=("Revenue", "sum"),          # sum of Revenue column
    Total_Units=("Units_Sold", "sum"),         # sum of Units_Sold
    Avg_Margin=("Profit_Margin_%", "mean"),    # average margin
    Num_Deals=("Revenue", "count")             # how many rows (deals)
).round(2)
print(sales_summary)

# Syntax:  New_Col_Name = ("source_column", "aggregation_function")
# Common functions: "sum", "mean", "median", "min", "max", "count", "std", "first", "last"

# ─────────────────────────────────────────────
# SECTION 4: reset_index() — flatten MultiIndex
# ─────────────────────────────────────────────
# After groupby, the group keys become the INDEX (not regular columns).
# reset_index() converts them back to normal columns → easier to export / filter.
print("\n" + "=" * 55)
print("5. RESET INDEX DEMO")
print("=" * 55)
flat = region_revenue.reset_index()  # Region becomes a column again
flat.columns = ["Region", "Total_Revenue"]
print(flat)
print(f"\nType before reset: {type(region_revenue)}")  # Series
print(f"Type after reset:  {type(flat)}")              # DataFrame

# ─────────────────────────────────────────────
# SECTION 5: as_index=False — skip reset_index
# ─────────────────────────────────────────────
# Shortcut: set as_index=False directly in groupby → result is always a flat DataFrame
print("\n" + "=" * 55)
print("6. AS_INDEX=FALSE SHORTCUT")
print("=" * 55)
flat2 = df.groupby("Region", as_index=False)["Revenue"].sum()
print(flat2)

# ─────────────────────────────────────────────
# SECTION 6: Sorting grouped results
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("7. TOP REGIONS BY REVENUE (SORTED)")
print("=" * 55)
top_regions = (
    df.groupby("Region", as_index=False)["Revenue"]
    .sum()
    .sort_values("Revenue", ascending=False)  # highest revenue first
)
print(top_regions)

# ─────────────────────────────────────────────
# SECTION 7: Chaining — filter AFTER groupby
# ─────────────────────────────────────────────
# You can chain normal DataFrame operations after groupby
print("\n" + "=" * 55)
print("8. CATEGORIES WITH AVG MARGIN > 20%")
print("=" * 55)
high_margin = (
    df.groupby("Product_Category", as_index=False)["Profit_Margin_%"]
    .mean()
    .query("`Profit_Margin_%` > 20")  # backticks needed for % in column name
    .round(2)
)
print(high_margin)

# ─────────────────────────────────────────────
# SECTION 8: Custom aggregation with lambda
# ─────────────────────────────────────────────
# "lambda x:" lets you write your own formula on the group
print("\n" + "=" * 55)
print("9. REVENUE RANGE (MAX - MIN) BY REGION")
print("=" * 55)
rev_range = df.groupby("Region")["Revenue"].agg(lambda x: x.max() - x.min())
print(rev_range)
# lambda x: x.max() - x.min()  →  for each group, compute the spread

# ─────────────────────────────────────────────
# SECTION 9: Named aggregation — clean output
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("10. FULL CATEGORY REPORT (NAMED AGG)")
print("=" * 55)
category_report = df.groupby("Product_Category").agg(
    Deals=("Revenue", "count"),
    Total_Revenue=("Revenue", "sum"),
    Avg_Revenue=("Revenue", "mean"),
    Best_Deal=("Revenue", "max"),
    Avg_Units=("Units_Sold", "mean"),
    Avg_Margin=("Profit_Margin_%", "mean")
).round(2)
print(category_report)

# ─────────────────────────────────────────────
# SECTION 10: Export grouped result to Excel
# ─────────────────────────────────────────────
with pd.ExcelWriter("Day32_GroupBy_Output.xlsx", engine="openpyxl") as writer:
    sales_summary.reset_index().to_excel(writer, sheet_name="Salesperson_Summary", index=False)
    top_regions.to_excel(writer, sheet_name="Region_Revenue", index=False)
    category_report.reset_index().to_excel(writer, sheet_name="Category_Report", index=False)

print("\n✅ Output exported → Day32_GroupBy_Output.xlsx (3 sheets)")
