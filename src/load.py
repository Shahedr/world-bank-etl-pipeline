import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

UPSERT_SQL = text(
    """
    INSERT INTO economic_indicators (
        country_code,
        country,
        year,
        indicator_code,
        indicator,
        value,
        value_billions,
        yoy_pct
    )
    VALUES (
        :country_code,
        :country,
        :year,
        :indicator_code,
        :indicator,
        :value,
        :value_billions,
        :yoy_pct
    )
    ON CONFLICT (country_code, year, indicator_code)
    DO UPDATE SET
        country = EXCLUDED.country,
        indicator = EXCLUDED.indicator,
        value = EXCLUDED.value,
        value_billions = EXCLUDED.value_billions,
        yoy_pct = EXCLUDED.yoy_pct
    """
)


def load_csv(df, path="data/processed/indicators.csv"):
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path


def _records_with_nulls(df):
    records = []

    for row in df.to_dict(orient="records"):
        records.append(
            {
                key: None if pd.isna(value) else value
                for key, value in row.items()
            }
        )

    return records


def load_postgres(df):
    database_url = os.environ["DATABASE_URL"]
    engine = create_engine(database_url)
    schema_sql = Path("sql/schema.sql").read_text()

    records = _records_with_nulls(df)

    if not records:
        return 0

    with engine.begin() as connection:
        connection.exec_driver_sql(schema_sql)
        connection.execute(UPSERT_SQL, records)

    return len(records)
