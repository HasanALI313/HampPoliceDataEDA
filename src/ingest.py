from pathlib import Path
from pyspark.sql import SparkSession
from src.config import SOURCE_DIR


def _get_csv_files(suffix: str) -> list[str]:
    return sorted(str(p) for p in SOURCE_DIR.rglob(f"*{suffix}"))


def ingest_to_bronze(spark: SparkSession) -> None:
    street_files = _get_csv_files("-street.csv")
    outcome_files = _get_csv_files("-outcomes.csv")

    street_df = spark.read.option("header", "true") \
        .option("inferSchema", "false") \
        .option("quote", "\"") \
        .csv(street_files)

    outcome_df = spark.read.option("header", "true") \
        .option("inferSchema", "false") \
        .option("quote", "\"") \
        .csv(outcome_files)

    street_df.createOrReplaceTempView("bronze_street_crime")
    outcome_df.createOrReplaceTempView("bronze_outcomes")

    print(f"  Ingested {street_df.count():,} street crime records")
    print(f"  Ingested {outcome_df.count():,} outcome records")


def drop_bronze(spark: SparkSession) -> None:
    spark.catalog.dropTempView("bronze_street_crime")
    spark.catalog.dropTempView("bronze_outcomes")
    print("  Bronze views dropped")
