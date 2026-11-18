from pathlib import Path
import numpy as np
import pandas as pd
from src.config import RAW_DIR
from src.logger import get_logger

logger = get_logger()

def generate_sample_data(rows: int = 2500, output_path: Path | None = None) -> Path:
    """Create reproducible demo orders. Replace this file with real, permitted data later."""
    rng = np.random.default_rng(42)
    customers = [f"C{n:05d}" for n in range(1, 401)]
    products = {
        "P100": ("Wireless Mouse", "Electronics", 699.0),
        "P101": ("Mechanical Keyboard", "Electronics", 2499.0),
        "P102": ("Water Bottle", "Home", 399.0),
        "P103": ("Running Shoes", "Fashion", 3299.0),
        "P104": ("Notebook Set", "Stationery", 249.0),
        "P105": ("Desk Lamp", "Home", 1199.0),
        "P106": ("USB-C Hub", "Electronics", 1799.0),
        "P107": ("Backpack", "Fashion", 1499.0),
    }
    cities = ["Hyderabad", "Bengaluru", "Chennai", "Mumbai", "Pune", "Delhi", "Noida"]
    start = np.datetime64("2025-01-01")
    dates = start + rng.integers(0, 365, size=rows).astype("timedelta64[D]")
    product_ids = rng.choice(list(products), size=rows)
    qty = rng.integers(1, 5, size=rows)
    records = []
    for i in range(rows):
        pid = product_ids[i]
        name, category, price = products[pid]
        records.append({
            "order_id": f"O{100000+i}",
            "order_date": str(dates[i]),
            "customer_id": rng.choice(customers),
            "customer_city": rng.choice(cities),
            "product_id": pid,
            "product_name": name,
            "category": category,
            "quantity": int(qty[i]),
            "unit_price": float(price * rng.uniform(0.90, 1.10)),
            "payment_method": rng.choice(["UPI", "Card", "Net Banking", "COD"]),
            "order_status": rng.choice(["Delivered", "Delivered", "Delivered", "Cancelled", "Returned"]),
        })
    df = pd.DataFrame(records)
    # Inject a small number of realistic data quality issues for the pipeline to detect.
    if rows >= 20:
        df.loc[3, "customer_city"] = None
        df.loc[7, "quantity"] = -1
        df = pd.concat([df, df.iloc[[0]]], ignore_index=True)  # duplicate order line
    output_path = output_path or RAW_DIR / "orders.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info("Generated %s sample rows at %s", len(df), output_path)
    return output_path

if __name__ == "__main__":
    generate_sample_data()
