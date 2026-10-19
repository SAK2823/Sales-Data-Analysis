
import sqlite3
import pandas as pd
from pathlib import Path

database_path = "data/sales_analysis.db"
query_file = Path("sql/analysis_queries.sql")

if not Path(database_path).exists():
    raise FileNotFoundError(
        "Database not found. Run 07_load_sqlite.py first."
    )

if not query_file.exists():
    raise FileNotFoundError(
        "Create sql/analysis_queries.sql first."
    )

connection = sqlite3.connect(database_path)

sql_text = query_file.read_text(encoding="utf-8")

# Execute each query separately
queries = [
    query.strip()
    for query in sql_text.split(";")
    if query.strip()
]

for number, query in enumerate(queries, start=1):
    print(f"\n===== SQL ANALYSIS {number} =====")

    result = pd.read_sql_query(query, connection)
    print(result.to_string(index=False))

connection.close()
