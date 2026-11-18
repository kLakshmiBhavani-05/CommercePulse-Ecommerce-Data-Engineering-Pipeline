
CREATE TABLE IF NOT EXISTS dim_customers (
    customer_id TEXT PRIMARY KEY,
    customer_city TEXT
);

CREATE TABLE IF NOT EXISTS dim_products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT,
    category TEXT
);

CREATE TABLE IF NOT EXISTS fact_orders (
    order_id TEXT PRIMARY KEY,
    order_date TEXT,
    order_month TEXT,
    customer_id TEXT,
    product_id TEXT,
    quantity INTEGER,
    unit_price REAL,
    revenue REAL,
    payment_method TEXT,
    order_status TEXT,
    FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES dim_products(product_id)
);

CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id TEXT PRIMARY KEY,
    input_rows INTEGER,
    clean_rows INTEGER,
    rejected_rows INTEGER
);

CREATE TABLE IF NOT EXISTS rejected_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT,
    source_row INTEGER,
    order_id TEXT,
    rejection_reason TEXT
);
