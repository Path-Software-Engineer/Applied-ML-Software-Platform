import pandas as pd


def add_revenue_column(sales_df: pd.DataFrame) -> pd.DataFrame:
    transformed_df = sales_df.copy()
    transformed_df['revenue'] = transformed_df['units_sold'] * transformed_df['unit_price']
    return transformed_df

def add_date_features(sales_df: pd.DataFrame) -> pd.DataFrame:
    transformed_df = sales_df.copy()
    
    transformed_df["date"] = pd.to_datetime(transformed_df["date"])
    transformed_df["day_sold"] = transformed_df["date"].dt.day_name()
    transformed_df["day_of_week"] = transformed_df["date"].dt.dayofweek
    transformed_df["month"] = transformed_df["date"].dt.month
    transformed_df["year"] = transformed_df["date"].dt.year
    
    return transformed_df