
import pandas as pd
import sqlite3
from pathlib import Path

# Load the cleaned dataset
df = pd.read_csv(
    "data/superstore_sales_cleaned.csv",
    low_memory=False
)

# Convert date columns consistently
for col in ["Order Date", "Ship Date"]:
    df[col] = pd.to_datetime(
        df[col],
        errors="coerce",
        format="mixed"
    ).dt.strftime("%Y-%m-%d")

# Create the database folder
Path("data").mkdir(exist_ok=True)

# Create SQLite database
connection = sqlite3.connect("data/sales_analysis.db")

# Load the dataset into a SQL table
df.to_sql(
    "sales",
    connection,
    if_exists="replace",
    index=False
)

# Verify the table
result = pd.read_sql_query(
    "SELECT COUNT(*) AS total_records FROM sales",
    connection
)

print("SQL table created successfully!")
print(result)

connection.close()
