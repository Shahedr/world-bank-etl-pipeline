import argparse

from extract import extract_live, extract_sample
from load import load_csv, load_postgres
from transform import transform


def run(use_sample=True, load_to_postgres=False):
    records = extract_sample() if use_sample else extract_live()
    df = transform(records)

    output_path = load_csv(df)

    if load_to_postgres:
        rows_loaded = load_postgres(df)
        print(f"Loaded {rows_loaded} rows to PostgreSQL")

    print(f"Processed {len(df)} rows -> {output_path}")
    print(df.to_string(index=False))


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract, transform, and load World Bank indicator data."
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Use the live World Bank API instead of the bundled sample response.",
    )
    parser.add_argument(
        "--postgres",
        action="store_true",
        help="Also load the transformed data to PostgreSQL.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(
        use_sample=not args.live,
        load_to_postgres=args.postgres,
    )
