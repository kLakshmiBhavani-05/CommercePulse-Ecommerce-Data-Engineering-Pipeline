import pandas as pd
from src.logger import get_logger

logger = get_logger()

def transform_orders(raw: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Clean and transform raw order records; invalid rows are excluded and counted."""
    df = raw.copy()
    input_rows = len(df)

    # Normalize text fields.
    for col in ["order_id", "customer_id", "customer_city", "product_id",
                "product_name", "category", "payment_method", "order_status"]:
        df[col] = df[col].astype("string").str.strip()

    # Remove duplicate order IDs; keep the first record.
    duplicate_count = int(df.duplicated(subset=["order_id"]).sum())
    df = df.drop_duplicates(subset=["order_id"], keep="first")

    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

    # Required field validation.
    required = ["order_id", "order_date", "customer_id", "product_id",
                "quantity", "unit_price", "order_status"]
    before_required = len(df)
    df = df.dropna(subset=required)
    missing_required_dropped = before_required - len(df)

    # Business rules: quantity and price must be positive.
    invalid_numeric = (df["quantity"] <= 0) | (df["unit_price"] <= 0)
    invalid_numeric_dropped = int(invalid_numeric.sum())
    df = df.loc[~invalid_numeric].copy()

    # Optional descriptive fields receive safe defaults.
    for col in ["customer_city", "product_name", "category", "payment_method"]:
        df[col] = df[col].fillna("Unknown").replace("", "Unknown")

    df["quantity"] = df["quantity"].astype(int)
    df["unit_price"] = df["unit_price"].round(2)
    df["revenue"] = (df["quantity"] * df["unit_price"]).round(2)
    df["order_date"] = df["order_date"].dt.date.astype(str)
    df["order_month"] = pd.to_datetime(df["order_date"]).dt.to_period("M").astype(str)

    metrics = {
        "input_rows": input_rows,
        "output_rows": len(df),
        "duplicates_removed": duplicate_count,
        "missing_required_dropped": int(missing_required_dropped),
        "invalid_numeric_dropped": invalid_numeric_dropped,
        "rows_removed_total": input_rows - len(df),
    }
    logger.info("Transform complete: %s", metrics)
    return df.reset_index(drop=True), metrics
