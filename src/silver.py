from pyspark.sql import SparkSession


def run_silver(spark: SparkSession) -> None:
    print("[Silver Layer]")

    spark.sql("""
        CREATE OR REPLACE TEMP VIEW silver_crimes AS
        SELECT
            NULLIF(TRIM(`Crime ID`), '') AS crime_id,
            TO_DATE(NULLIF(TRIM(`Month`), ''), 'yyyy-MM') AS month,
            TRIM(`Reported by`) AS reported_by,
            TRIM(`Falls within`) AS falls_within,
            TRY_CAST(NULLIF(TRIM(`Longitude`), '') AS DOUBLE) AS longitude,
            TRY_CAST(NULLIF(TRIM(`Latitude`), '') AS DOUBLE) AS latitude,
            NULLIF(TRIM(`Location`), '') AS location,
            NULLIF(TRIM(`LSOA code`), '') AS lsoa_code,
            NULLIF(TRIM(`LSOA name`), '') AS lsoa_name,
            NULLIF(TRIM(`Crime type`), '') AS crime_type,
            NULLIF(TRIM(`Last outcome category`), '') AS last_outcome_category
        FROM bronze_street_crime
    """)

    spark.sql("""
        CREATE OR REPLACE TEMP VIEW silver_outcomes AS
        SELECT
            NULLIF(TRIM(`Crime ID`), '') AS crime_id,
            TO_DATE(NULLIF(TRIM(`Month`), ''), 'yyyy-MM') AS month,
            TRIM(`Reported by`) AS reported_by,
            TRIM(`Falls within`) AS falls_within,
            TRY_CAST(NULLIF(TRIM(`Longitude`), '') AS DOUBLE) AS longitude,
            TRY_CAST(NULLIF(TRIM(`Latitude`), '') AS DOUBLE) AS latitude,
            NULLIF(TRIM(`Location`), '') AS location,
            NULLIF(TRIM(`LSOA code`), '') AS lsoa_code,
            NULLIF(TRIM(`LSOA name`), '') AS lsoa_name,
            NULLIF(TRIM(`Outcome type`), '') AS outcome_type
        FROM bronze_outcomes
    """)

    crime_count = spark.table("silver_crimes").count()
    outcome_count = spark.table("silver_outcomes").count()
    print(f"  Cleaned {crime_count:,} crime records")
    print(f"  Cleaned {outcome_count:,} outcome records")

    null_coords = spark.sql("""
        SELECT count(*) AS cnt FROM silver_crimes
        WHERE longitude IS NULL OR latitude IS NULL
    """).first()[0]
    print(f"  Records with missing coordinates: {null_coords:,}")
    print()
