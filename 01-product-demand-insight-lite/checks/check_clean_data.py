from src.data.clean_data import clean_sales_data
from src.data.load_data import load_sales_data

DATA_PATH = "data/raw/sales_raw.csv"

def main():
    raw_data = load_sales_data(DATA_PATH)
    clean_data = clean_sales_data(raw_data)
    
    print("Data cleaned successfully.")
    print(f"Rows: {clean_data.shape[0]}")
    print(f"Columns: {clean_data.shape[1]}")
    print()
    print(clean_data.head())
    print()
    print(clean_data.dtypes)
    
    
if __name__ == "__main__":
    main()
