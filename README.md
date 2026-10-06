# World Bank ETL Pipeline

Data-engineering project that extracts economic indicator data from the World Bank API, transforms it into an analytics-ready model, and loads it to CSV or PostgreSQL.

## Architecture
```text
World Bank API / sample JSON
          |
       Extract
          |
       Transform
   clean + dedupe + YoY
          |
        Load
   CSV / PostgreSQL
```

## Features
- Public REST API extraction with request validation
- Offline sample mode for reproducible runs
- Data cleaning and schema normalization with pandas
- Duplicate handling and year-over-year calculation
- PostgreSQL loading through SQLAlchemy
- Docker Compose PostgreSQL environment
- Pytest data-quality test

## Tools
**Python · REST APIs · pandas · PostgreSQL · SQLAlchemy · Docker · pytest · ETL**

## Repository structure
```text
world-bank-etl-pipeline/
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── pipeline.py
├── data/raw/sample_world_bank.json
├── sql/schema.sql
├── tests/test_transform.py
├── docker-compose.yml
└── README.md
```

## Run locally — no database required
```bash
pip install -r requirements.txt
python src/pipeline.py
```

## Run against the live World Bank API
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

## What this demonstrates
A clean extract-transform-load workflow, API ingestion, relational loading, reproducibility, data-quality checks, and a foundation that can later be extended with dbt and Airflow.
