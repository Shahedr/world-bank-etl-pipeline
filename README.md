# World Bank ETL Pipeline

I built this project to practice a small but complete data-pipeline pattern using a public API: **extract data, normalize it, calculate a derived field, and load the result somewhere useful**.

I chose the World Bank API because it is public, easy to query without API keys, and gives the project a real external data source instead of another generated CSV.

## Pipeline

```text
World Bank API / local sample JSON
            |
         Extract
            |
         Transform
   normalize + dedupe + YoY
            |
          Load
      CSV / PostgreSQL
```

## What the pipeline does

- calls the World Bank REST API with basic request validation
- supports an offline sample mode so the project can still be run without network access
- normalizes the API response into a tabular structure
- removes duplicate business keys
- calculates year-over-year change
- writes the transformed data to CSV
- optionally loads the result to PostgreSQL with SQLAlchemy
- uses a PostgreSQL **upsert** on country/year/indicator so rerunning the same data does not create duplicate rows
- includes pytest checks for expected fields and duplicate business keys

## Why I added an offline mode

A portfolio project should still be reproducible if an external API is slow or temporarily unavailable. The sample JSON gives me a stable local input for testing the transform and load logic while keeping the live API option available.

## Run locally

```bash
pip install -r requirements.txt
python src/pipeline.py
```

This uses the local sample input and does not require a database.

## Run against the live API

```bash
python src/pipeline.py --live
```

## PostgreSQL mode

```bash
docker compose up -d
cp .env.example .env
# export DATABASE_URL from .env
python src/pipeline.py --live --postgres
```

The loader creates the table from `sql/schema.sql` if needed and then inserts or updates rows using `(country_code, year, indicator_code)` as the business key.

## Project structure

```text
world-bank-etl-pipeline/
├── data/raw/sample_world_bank.json
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── pipeline.py
├── sql/schema.sql
├── tests/test_transform.py
├── docker-compose.yml
├── .env.example
├── requirements.txt
└── README.md
```

## Stack

Python · REST APIs · pandas · PostgreSQL · SQLAlchemy · Docker · pytest

## What I would add in a production version

This is intentionally a small pipeline, not a production orchestration system. The next pieces I would add are retries/backoff, structured logging, incremental loads, stronger schema tests, scheduling, and lineage/transform management.

That is where tools such as **Airflow** and **dbt** would fit; they are not presented here as if they are already implemented.
