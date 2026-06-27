from pathlib import Path

import pandas as pd


def load_sales_data(file_path: str) -> pd.DataFrame:
    """
    Load sales data from a CSV file.

    Parameters
    ----------
    file_path : str
        Path to the raw sales CSV file.

    Returns
    -------
    pd.DataFrame
        Sales data loaded as a DataFrame.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Sales data file not found: {file_path}")

    data = pd.read_csv(path)

    return data