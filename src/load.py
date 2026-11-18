
import pandas as pd
from sqlalchemy import text

from src.database import get_engine, initialize_database


def load_to_warehouse(
    clean,
    rejected=None,
    run_id=None,
    metrics=None,
    engine=None
):
    engine = engine or get_engine()
    initialize_database(engine)

    rejected = rejected if rejected is not None else pd.DataFrame()
    metrics = metrics or {}

    with engine.begin() as conn:
        # Insert customers
        if not clean.empty:
            customers = clean[
                ["customer_id", "customer_city"]
            ].drop_duplicates("customer_id")

            for _, row in customers.iterrows():
                conn.execute(
                    text("""
                        INSERT INTO dim_customers (customer_id, customer_city)
                        VALUES (:customer_id, :customer_city)
                        ON CONFLICT(customer_id)
                        DO UPDATE SET customer_city = excluded.customer_city
                    """),
                    row.to_dict()
                )

            # Insert products
            products = clean[
                ["product_id", "product_name", "category"]
            ].drop_duplicates("product_id")

            for _, row in products.iterrows():
                conn.execute(
                    text("""
                        INSERT INTO dim_products (product_id, product_name, category)
                        VALUES (:product_id, :product_name, :category)
                        ON CONFLICT(product_id)
                        DO UPDATE SET
                            product_name = excluded.product_name,
                            category = excluded.category
                    """),
                    row.to_dict()
                )

            # Insert orders
            for _, row in clean.iterrows():
                conn.execute(
                    text("""
                        INSERT INTO fact_orders (
                            order_id, order_date, order_month,
                            customer_id, product_id, quantity,
                            unit_price, revenue, payment_method,
                            order_status
                        )
                        VALUES (
                            :order_id, :order_date, :order_month,
                            :customer_id, :product_id, :quantity,
                            :unit_price, :revenue, :payment_method,
                            :order_status
                        )
                        ON CONFLICT(order_id)
                        DO UPDATE SET
                            order_date = excluded.order_date,
                            order_month = excluded.order_month,
                            customer_id = excluded.customer_id,
                            product_id = excluded.product_id,
                            quantity = excluded.quantity,
                            unit_price = excluded.unit_price,
                            revenue = excluded.revenue,
                            payment_method = excluded.payment_method,
                            order_status = excluded.order_status
                    """),
                    row.to_dict()
                )

        # Store rejected records
        if not rejected.empty:
            for _, row in rejected.iterrows():
                conn.execute(
                    text("""
                        INSERT INTO rejected_records (
                            run_id, source_row, order_id, rejection_reason
                        )
                        VALUES (
                            :run_id, :source_row, :order_id, :rejection_reason
                        )
                    """),
                    {
                        "run_id": run_id,
                        "source_row": row.get("_source_row"),
                        "order_id": row.get("order_id"),
                        "rejection_reason": row.get("rejection_reason")
                    }
                )

        # Store pipeline run details
        conn.execute(
            text("""
                INSERT INTO pipeline_runs (
                    run_id, input_rows, clean_rows, rejected_rows
                )
                VALUES (
                    :run_id, :input_rows, :clean_rows, :rejected_rows
                )
            """),
            {
                "run_id": run_id,
                "input_rows": metrics.get("input_rows", len(clean) + len(rejected)),
                "clean_rows": metrics.get("clean_rows", len(clean)),
                "rejected_rows": metrics.get("rejected_rows", len(rejected))
            }
        )

    return {
        "loaded_rows": len(clean),
        "rejected_rows": len(rejected)
    }
