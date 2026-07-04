from pathlib import Path
from pyspark.sql import SparkSession
from src.config import GOLD_DIR


def run_gold(spark: SparkSession) -> None:
    print("[Gold Layer]")

    GOLD_DIR.mkdir(parents=True, exist_ok=True)

    queries = {
        "crime_counts_by_type": """
            SELECT crime_type, count(*) AS total_crimes
            FROM silver_crimes
            WHERE crime_type IS NOT NULL
            GROUP BY crime_type
            ORDER BY total_crimes DESC
        """,
        "crime_counts_by_month": """
            SELECT month, count(*) AS total_crimes, count(DISTINCT crime_id) AS unique_crimes
            FROM silver_crimes
            WHERE month IS NOT NULL
            GROUP BY month
            ORDER BY month
        """,
        "crime_counts_by_lsoa": """
            SELECT lsoa_code, lsoa_name, count(*) AS total_crimes,
                   count(DISTINCT crime_id) AS unique_crimes
            FROM silver_crimes
            WHERE lsoa_code IS NOT NULL
            GROUP BY lsoa_code, lsoa_name
            ORDER BY total_crimes DESC
        """,
        "outcome_summary": """
            SELECT outcome_type, count(*) AS total_outcomes
            FROM silver_outcomes
            WHERE outcome_type IS NOT NULL
            GROUP BY outcome_type
            ORDER BY total_outcomes DESC
        """,
        "monthly_crime_outcomes": """
            SELECT s.month, s.crime_type, o.outcome_type, count(*) AS total
            FROM silver_crimes s
            LEFT JOIN silver_outcomes o ON s.crime_id = o.crime_id
            WHERE s.month IS NOT NULL AND s.crime_type IS NOT NULL
            GROUP BY s.month, s.crime_type, o.outcome_type
            ORDER BY s.month, total DESC
        """,
    }

    for name, sql in queries.items():
        df = spark.sql(sql)
        path = str(GOLD_DIR / name)
        df.write.mode("overwrite").parquet(path)
        cnt = df.count()
        print(f"  gold.{name}: {cnt:,} rows")

    print()
