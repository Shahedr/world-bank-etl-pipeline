from pathlib import Path
import os
from sqlalchemy import create_engine

def load_csv(df, path='data/processed/indicators.csv'):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    df.to_csv(path,index=False)
    return path

def load_postgres(df, table='economic_indicators'):
    url=os.environ['DATABASE_URL']
    engine=create_engine(url)
    df.to_sql(table,engine,if_exists='append',index=False,method='multi')
    return len(df)
