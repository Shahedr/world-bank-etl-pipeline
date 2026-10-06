import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))
from extract import extract_sample
from transform import transform

def test_transform_has_expected_columns():
    df=transform(extract_sample())
    expected={'country_code','country','year','indicator_code','indicator','value','value_billions','yoy_pct'}
    assert expected.issubset(df.columns)
    assert len(df) > 0
    assert df['value'].notna().all()
