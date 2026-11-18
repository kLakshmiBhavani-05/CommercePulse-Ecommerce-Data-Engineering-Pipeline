
import pandas as pd

from src.database import get_engine, initialize_database
from src.load import load_to_warehouse


def test_warehouse_upsert_is_idempotent(tmp_path):
    engine = get_engine(f"sqlite:///{tmp_path / 'test.db'}")
    initialize_database(engine)

    clean = pd.DataFrame([{
        "order_id": "O1",
        "order_date": "2025-01-01",
        "order_month": "2025-01",
        "customer_id": "C1",
        "customer_city": "Hyderabad",
        "product_id": "P1",
        "product_name": "Mouse",
        "category": "Electronics",
        "quantity": 2,
        "unit_price": 10.0,
        "revenue": 20.0,
        "payment_method": "UPI",
        "order_status": "Delivered"
    }])

    rejected = pd.DataFrame(
        columns=["_source_row", "order_id", "rejection_reason"]
    )

    metrics = {
        "input_rows": 1,
        "clean_rows": 1,
        "rejected_rows": 0
    }

    load_to_warehouse(clean, rejected, "run-1", metrics, engine)
    load_to_warehouse(clean, rejected, "run-2", metrics, engine)

    with engine.connect() as conn:
        order_count = conn.exec_driver_sql(
            "SELECT COUNT(*) FROM fact_orders"
        ).scalar_one()

        run_count = conn.exec_driver_sql(
            "SELECT COUNT(*) FROM pipeline_runs"
        ).scalar_one()

    assert order_count == 1
    assert run_count == 2
