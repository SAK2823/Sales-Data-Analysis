
import pandas as pd

file_path = "data/superstore_sales_cleaned.csv"

# Read the file consistently
df = pd.read_csv(file_path, low_memory=False)

print("Order Date column type:")
print(df["Order Date"].map(type).value_counts())

print("\nSample original date values:")
print(df["Order Date"].head(15).to_list())

# Convert dates and identify values that fail
original_dates = df["Order Date"].copy()
parsed_dates = pd.to_datetime(original_dates, errors="coerce")

invalid = original_dates.notna() & parsed_dates.isna()

print("\nInvalid date count:", invalid.sum())

if invalid.any():
    print("\nExamples of invalid dates:")
    print(original_dates[invalid].head(20).to_list())

print("\nEarliest date:", parsed_dates.min())
print("Latest date:", parsed_dates.max())
