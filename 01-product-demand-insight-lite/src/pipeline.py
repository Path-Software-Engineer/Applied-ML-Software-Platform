from src.data.clean_data import clean_sales_data
from src.data.load_data import load_sales_data


DEFAULT_DATA_PATH = "data/raw/sales_raw.csv"


def run_data_pipeline(file_path: str = DEFAULT_DATA_PATH):
    """
    Run the initial data pipeline.

    Flow:
    raw CSV -> load data -> clean data

    This pipeline does not create features yet.
    It only connects loading and cleaning.
    """
    raw_data = load_sales_data(file_path)
    clean_data = clean_sales_data(raw_data)

    return raw_data, clean_data


def main():
    raw_data, clean_data = run_data_pipeline()

    print("Data pipeline executed successfully.")
    print(f"Raw shape: {raw_data.shape}")
    print(f"Clean shape: {clean_data.shape}")
    print()

    print("Clean columns:")
    print(list(clean_data.columns))
    print()

    print("Clean data types:")
    print(clean_data.dtypes)
    print()

    if "units_sold" not in clean_data.columns:
        raise ValueError("units_sold column was not preserved.")

    print("units_sold column preserved.")
    print()
    print(clean_data.head())


if __name__ == "__main__":
    main()