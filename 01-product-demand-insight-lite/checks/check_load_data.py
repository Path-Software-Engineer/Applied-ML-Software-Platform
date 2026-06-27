from src.data.load_data import load_sales_data

DATA_PATH = "data/raw/sales_raw.csv"

def main():
    data = load_sales_data(DATA_PATH)
    
    print("Data loaded successfully")
    print(f"Rows: {data.shape[0]}")
    print(f"Columns: {data.shape[1]}")
    print()
    print(data.head())
    
    
if __name__ == "__main__":
    main()