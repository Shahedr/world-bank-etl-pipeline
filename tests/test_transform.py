import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from extract import extract_sample
from transform import transform

EXPECTED_COLUMNS = {
    "country_code",
    "country",
    "year",
    "indicator_code",
    "indicator",
    "value",
    "value_billions",
    "yoy_pct",
}


def test_transform_has_expected_columns_and_values():
    df = transform(extract_sample())

    assert EXPECTED_COLUMNS.issubset(df.columns)
    assert len(df) > 0
    assert df["value"].notna().all()
    assert df["country_code"].notna().all()
    assert df["indicator_code"].notna().all()


def test_transform_removes_duplicate_business_keys():
    df = transform(extract_sample())

    duplicate_count = df.duplicated(
        subset=["country_code", "year", "indicator_code"]
    ).sum()

    assert duplicate_count == 0
