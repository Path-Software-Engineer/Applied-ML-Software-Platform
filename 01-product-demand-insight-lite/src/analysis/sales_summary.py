import pandas as pd

def get_top_product_by_units(sales_df: pd.DataFrame) -> pd.Series:
    product_units = sales_df.groupby("product")["units_sold"].sum()
    product_units = product_units.sort_values(ascending=False)
    
    return product_units.head(1)

def get_top_product_by_revenue(sales_df: pd.DataFrame) -> pd.Series:
    product_revenue = sales_df.groupby("product")["revenue"].sum()
    product_revenue = product_revenue.sort_values(ascending=False)
    
    return product_revenue.head(1)

def get_total_units_sold(sales_df: pd.DataFrame) -> pd.Series:
    total_units_sold = sales_df["units_sold"].sum()
    
    return total_units_sold

def get_total_revenue(sales_df: pd.DataFrame) -> pd.Series:
    total_revenue = sales_df["revenue"].sum()
    
    return total_revenue

def get_best_day_by_units(sales_df: pd.DataFrame) -> pd.Series:
    best_day_units = sales_df.groupby("day_sold")["units_sold"].sum()
    best_day_units = best_day_units.sort_values(ascending=False)
    
    return best_day_units.head(1)


def generate_sales_summary(sales_df: pd.DataFrame) -> dict:
    summary = {
        "top_product_by_units": series_to_name_value(
            get_top_product_by_units(sales_df)
        ),
        "top_product_by_revenue": series_to_name_value(
            get_top_product_by_revenue(sales_df)
        ),
        "total_units_sold": int(get_total_units_sold(sales_df)),
        "total_revenue": float(get_total_revenue(sales_df)),
        "best_day_by_units": series_to_name_value(
            get_best_day_by_units(sales_df)
        )
    }
    
    return summary

def series_to_name_value(result_series: pd.Series) -> dict:
    name = result_series.index[0]
    value = result_series.iloc[0]
    
    if hasattr(value, "item"):
        value = value.item()
    
    return {
        "name": name,
        "value": value
    }