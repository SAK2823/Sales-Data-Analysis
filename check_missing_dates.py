
import pandas as pd

files = {
    "Original": "superstore_sales.csv",
    "Cleaned": "data/superstore_sales_cleaned.csv"
}

for name, path in files.items():
    print(f"\n===== {name} DATASET =====")

    try:
        # Try the common Windows-compatible encoding first
        try:
            df = pd.read_csv(
                path,
                encoding="utf-8",
                low_memory=False
            )
        except UnicodeDecodeError:
            df = pd.read_csv(
                path,
                encoding="cp1252",
                low_memory=False
            )

        df.columns = df.columns.str.strip()

        print("Total rows:", len(df))

        if "Order Date" in df.columns:
            dates = df["Order Date"]

            print("Missing Order Dates:", dates.isna().sum())
            print(
                "Missing percentage:",
                round(dates.isna().mean() * 100, 2),
                "%"
            )

            print("Sample non-empty dates:")
            print(dates.dropna().head(5).to_list())
        else:
            print("Order Date column not found.")
            print("Available columns:", df.columns.tolist())

    except Exception as error:
        print("Error reading file:", error)
