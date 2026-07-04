from pyspark.sql import SparkSession
from src.ingest import ingest_to_bronze


def run_bronze(spark: SparkSession) -> None:
    print("[Bronze Layer]")
    ingest_to_bronze(spark)
    print()
