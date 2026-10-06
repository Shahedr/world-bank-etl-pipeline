CREATE TABLE IF NOT EXISTS economic_indicators (
  country_code VARCHAR(3) NOT NULL,
  country TEXT NOT NULL,
  year INTEGER NOT NULL,
  indicator_code TEXT NOT NULL,
  indicator TEXT NOT NULL,
  value DOUBLE PRECISION NOT NULL,
  value_billions NUMERIC(18,2),
  yoy_pct NUMERIC(10,2),
  PRIMARY KEY (country_code, year, indicator_code)
);
