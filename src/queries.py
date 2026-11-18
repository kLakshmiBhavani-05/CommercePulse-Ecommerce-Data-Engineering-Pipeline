from sqlalchemy import text
from src.database import get_engine

QUERIES = {
    "Revenue by month": """SELECT order_month, ROUND(SUM(revenue),2) AS revenue
        FROM fact_orders WHERE order_status = 'Delivered'
        GROUP BY order_month ORDER BY order_month""",
    "Top 10 products": """SELECT p.product_name, ROUND(SUM(f.revenue),2) AS revenue
        FROM fact_orders f JOIN dim_products p ON f.product_id=p.product_id
        WHERE f.order_status='Delivered'
        GROUP BY p.product_name ORDER BY revenue DESC LIMIT 10""",
    "Sales by city": """SELECT c.customer_city, ROUND(SUM(f.revenue),2) AS revenue
        FROM fact_orders f JOIN dim_customers c ON f.customer_id=c.customer_id
        WHERE f.order_status='Delivered'
        GROUP BY c.customer_city ORDER BY revenue DESC""",
    "Monthly order ranking": """SELECT order_month, order_id, revenue,
        DENSE_RANK() OVER (PARTITION BY order_month ORDER BY revenue DESC) AS monthly_rank
        FROM fact_orders ORDER BY order_month, monthly_rank""",
    "Order status summary": """SELECT order_status, COUNT(*) AS order_count
        FROM fact_orders GROUP BY order_status ORDER BY order_count DESC""",
}

def run_query(sql: str):
    engine = get_engine()
    with engine.connect() as conn:
        return conn.execute(text(sql)).mappings().all()
