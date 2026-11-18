import pandas as pd
from src.transform import transform_orders

def test_transform_removes_duplicate_and_invalid_rows():
    raw = pd.DataFrame([
        {"order_id":"1","order_date":"2025-01-01","customer_id":"C1","customer_city":"Hyd",
         "product_id":"P1","product_name":"Mouse","category":"Electronics","quantity":2,
         "unit_price":100,"payment_method":"UPI","order_status":"Delivered"},
        {"order_id":"1","order_date":"2025-01-01","customer_id":"C1","customer_city":"Hyd",
         "product_id":"P1","product_name":"Mouse","category":"Electronics","quantity":2,
         "unit_price":100,"payment_method":"UPI","order_status":"Delivered"},
        {"order_id":"2","order_date":"2025-01-01","customer_id":"C2","customer_city":"Hyd",
         "product_id":"P2","product_name":"Book","category":"Books","quantity":-1,
         "unit_price":50,"payment_method":"COD","order_status":"Delivered"},
    ])
    clean, metrics = transform_orders(raw)
    assert len(clean) == 1
    assert clean.iloc[0]["revenue"] == 200
    assert metrics["duplicates_removed"] == 1
    assert metrics["invalid_numeric_dropped"] == 1
