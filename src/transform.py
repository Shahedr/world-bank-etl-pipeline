import pandas as pd

def transform(records):
    rows=[]
    for r in records:
        if r.get('value') is None: continue
        rows.append({
            'country_code':r.get('countryiso3code'),
            'country':(r.get('country') or {}).get('value'),
            'year':int(r.get('date')),
            'indicator_code':(r.get('indicator') or {}).get('id'),
            'indicator':(r.get('indicator') or {}).get('value'),
            'value':float(r.get('value')),
        })
    df=pd.DataFrame(rows)
    if df.empty: return df
    df=df.drop_duplicates(subset=['country_code','year','indicator_code'])
    df=df.sort_values(['country_code','year']).reset_index(drop=True)
    df['value_billions']=(df['value']/1_000_000_000).round(2)
    df['yoy_pct']=df.groupby(['country_code','indicator_code'])['value'].pct_change(fill_method=None).mul(100).round(2)
    return df
