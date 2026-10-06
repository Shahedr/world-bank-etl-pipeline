from pathlib import Path
import json
import requests

BASE_URL='https://api.worldbank.org/v2/country/{countries}/indicator/{indicator}'

def extract_live(countries='USA;CAN;MEX', indicator='NY.GDP.MKTP.CD', start=2018, end=2023):
    url=BASE_URL.format(countries=countries,indicator=indicator)
    params={'format':'json','date':f'{start}:{end}','per_page':500}
    r=requests.get(url,params=params,timeout=30); r.raise_for_status()
    payload=r.json()
    return payload[1] if len(payload)>1 else []

def extract_sample(path='data/raw/sample_world_bank.json'):
    return json.loads(Path(path).read_text())
