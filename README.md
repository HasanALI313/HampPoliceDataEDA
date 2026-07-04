# UK Police Crime Data Pipeline (Hampshire)

Cleans and analyses monthly crime data from [data.police.uk](https://data.police.uk/) for Hampshire Constabulary using **PySpark**.

## Data Source

- **Street-level crime** — individual crime records with location, type, and outcome
- **Outcomes** — case resolution data linked by Crime ID

Data is organised by month under `source/YYYY-MM/` as `.csv` files.

## Pipeline Stages (Bronze → Silver → Gold)

### Bronze (`src/bronze.py` → `src/ingest.py`)
Reads all raw CSV files from `source/` into Spark temp views (`bronze_street_crime`, `bronze_outcomes`) with all columns as strings.

### Silver (`src/silver.py`)
Cleans and standardises the data — trims whitespace, casts coordinates to doubles, parses dates, and handles nulls.

### Gold (`src/gold.py`)
Builds analytics tables and writes them as **Parquet** files to `output/gold/`:
- `crime_counts_by_type` — crimes grouped by type
- `crime_counts_by_month` — monthly totals
- `crime_counts_by_lsoa` — crimes by area
- `outcome_summary` — outcome distribution
- `monthly_crime_outcomes` — cross-tabulation of month, crime type, and outcome

## How to Run Locally

```bash
uv sync
uv run python main.py
```

Output Parquet files are written to `output/gold/`.

## How to Run with Docker

```bash
docker compose up --build
```

Mounts `source/` for input CSVs and `output/` for the Parquet results. Override paths via `POLICE_SOURCE_DIR` and `POLICE_OUTPUT_DIR` environment variables.


Proj_Structure 
project/
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── docker.yml
│
├── src/
│   ├── bronze.py
│   ├── silver.py
│   └── gold.py
│
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
├── main.py
├── README.md
└── data/
