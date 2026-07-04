from pathlib import Path
from pyspark.sql import SparkSession
from src.config import OUTPUT_DIR
from src.bronze import run_bronze
from src.silver import run_silver
from src.gold import run_gold


def main():
    import shutil
    if OUTPUT_DIR.exists():
        shutil.rmtree(str(OUTPUT_DIR))

    spark = SparkSession.builder \
        .appName("PoliceDataPipeline") \
        .master("local[*]") \
        .config("spark.sql.adaptive.enabled", "true") \
        .getOrCreate()

    try:
        print("=" * 50)
        print("UK Police Data Pipeline (PySpark)")
        print("=" * 50)
        print()

        run_bronze(spark)
        run_silver(spark)
        run_gold(spark)

        print("=" * 50)
        print("Pipeline complete!")
        print(f"Output: {OUTPUT_DIR}")
        print("=" * 50)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
