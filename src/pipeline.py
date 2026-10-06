import argparse
from extract import extract_live, extract_sample
from transform import transform
from load import load_csv, load_postgres

def run(sample=True, postgres=False):
    records=extract_sample() if sample else extract_live()
    df=transform(records)
    path=load_csv(df)
    if postgres:
        rows=load_postgres(df)
        print(f'Loaded {rows} rows to PostgreSQL')
    print(f'Processed {len(df)} rows -> {path}')
    print(df.to_string(index=False))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--live',action='store_true')
    p.add_argument('--postgres',action='store_true')
    a=p.parse_args(); run(sample=not a.live,postgres=a.postgres)
