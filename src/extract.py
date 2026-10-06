import json
from pathlib import Path

import requests

BASE_URL = "https://api.worldbank.org/v2/country/{countries}/indicator/{indicator}"


def extract_live(
    countries="USA;CAN;MEX",
    indicator="NY.GDP.MKTP.CD",
    start=2018,
    end=2023,
):
    url = BASE_URL.format(countries=countries, indicator=indicator)
    params = {
        "format": "json",
        "date": f"{start}:{end}",
        "per_page": 500,
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()

    if not isinstance(payload, list) or len(payload) < 2:
        raise ValueError("Unexpected response format from the World Bank API.")

    return payload[1] or []


def extract_sample(path="data/raw/sample_world_bank.json"):
    return json.loads(Path(path).read_text())
