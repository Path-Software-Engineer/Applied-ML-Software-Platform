import pandas as pd

REQUIRED_COLUMNS = [
    "date",
    "product",
    "category",
    "units_sold",
    "unit_price",
]

def clean_sales_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw sales data.

    This function validates the minimum required columns,
    converts date to datetime, removes extra spaces in text columns,
    and checks for invalid values.

    Parameters
    ----------
    data : pd.DataFrame
        Raw sales data.

    Returns
    -------
    pd.DataFrame
        Clean sales data.
    """
    
    clean_data = data.copy()
    
    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in clean_data.columns
    ]
    
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    if clean_data[REQUIRED_COLUMNS].isna().any().any():
        null_counts = clean_data[REQUIRED_COLUMNS].isna().sum()
        raise ValueError(f"Null values found:\n{null_counts}")
    
    clean_data["date"] = pd.to_datetime(clean_data["date"], errors="coerce")
    
    if clean_data["date"].isna().any():
        raise ValueError("Invalid date values found in date column.")
    
    clean_data["product"] = clean_data["product"].astype(str).str.strip()
    clean_data["category"] = clean_data["category"].astype(str).str.strip()
    
    if (clean_data["product"] == "").any():
        raise ValueError("Empty product values found.")
    if (clean_data["category"] == "").any():
        raise ValueError("Empty category values found.")
    if (clean_data["units_sold"] < 0).any():
        raise ValueError("Units of product cannot be lower than zero.")
    if (clean_data["unit_price"] <= 0).any():
        raise ValueError("Prices must be greater than zero.")
    
    return clean_data
    
    
    