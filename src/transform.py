import pandas as pd

OUTPUT_COLUMNS = [
    "country_code",
    "country",
    "year",
    "indicator_code",
    "indicator",
    "value",
    "value_billions",
    "yoy_pct",
]


def transform(records):
    rows = []

    for record in records:
        if record.get("value") is None:
            continue

        rows.append(
            {
                "country_code": record.get("countryiso3code"),
                "country": (record.get("country") or {}).get("value"),
                "year": int(record.get("date")),
                "indicator_code": (record.get("indicator") or {}).get("id"),
                "indicator": (record.get("indicator") or {}).get("value"),
                "value": float(record.get("value")),
            }
        )

    if not rows:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)

    df = pd.DataFrame(rows)
    df = df.drop_duplicates(
        subset=["country_code", "year", "indicator_code"]
    )
    df = df.sort_values(["country_code", "year"]).reset_index(drop=True)

    df["value_billions"] = (df["value"] / 1_000_000_000).round(2)
    df["yoy_pct"] = (
        df.groupby(["country_code", "indicator_code"])["value"]
        .pct_change(fill_method=None)
        .mul(100)
        .round(2)
    )

    return df[OUTPUT_COLUMNS]
