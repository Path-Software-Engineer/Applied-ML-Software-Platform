import pandas as pd

def load_sales_data(file_path: str) -> pd.DataFrame:
    sales_df = pd.read_csv(file_path)
    return sales_df