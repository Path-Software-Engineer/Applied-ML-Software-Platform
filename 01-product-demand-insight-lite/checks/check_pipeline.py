from src.pipeline import run_data_pipeline


def main():
    raw_data, clean_data = run_data_pipeline()

    print("Pipeline check completed successfully.")
    print(f"Raw rows: {raw_data.shape[0]}")
    print(f"Clean rows: {clean_data.shape[0]}")
    print(f"Raw columns: {raw_data.shape[1]}")
    print(f"Clean columns: {clean_data.shape[1]}")
    print()

    if "units_sold" not in clean_data.columns:
        raise ValueError("units_sold column was not preserved.")

    if clean_data["date"].dtype.kind != "M":
        raise TypeError("date column was not converted to datetime.")

    print("units_sold preserved.")
    print("date converted to datetime.")
    print()
    print(clean_data.head())


if __name__ == "__main__":
    main()