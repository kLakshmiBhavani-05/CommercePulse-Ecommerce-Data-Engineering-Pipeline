import pandas as pd
from pathlib import Path
from src.config import RAW_DIR
from src.logger import get_logger

logger = get_logger()

REQUIRED_COLUMNS = [
    "order_id", "order_date", "customer_id", "customer_city",
    "product_id", "product_name", "category", "quantity",
    "unit_price", "payment_method", "order_status"
]

def extract_orders(path: Path | None = None) -> pd.DataFrame:
    path = path or RAW_DIR / "orders.csv"
    if not path.exists():
        raise FileNotFoundError(f"Raw dataset not found: {path}. Run: python -m src.generate_data")
    df = pd.read_csv(path)
    missing = sorted(set(REQUIRED_COLUMNS) - set(df.columns))
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")
    logger.info("Extracted %s rows from %s", len(df), path)
    return df
