import json
import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import text
from src.database import get_engine
from src.pipeline import run_pipeline
from src.config import RAW_DIR, PROCESSED_DIR
from src.generate_data import generate_sample_data
from src.queries import QUERIES

st.set_page_config(page_title="CommercePulse | Data Engineering", page_icon="📊", layout="wide")

st.markdown('''
<style>
.block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
[data-testid="stMetric"] {background: #111827; border: 1px solid #263244; padding: 16px; border-radius: 12px;}
div[data-testid="stSidebar"] {background: #0b1220;}
.small-muted {color: #94a3b8; font-size: 0.9rem;}
</style>
''', unsafe_allow_html=True)

st.title("CommercePulse")
st.caption("E-commerce data engineering pipeline | Extract · Transform · Load · Analyze")

with st.sidebar:
    st.header("Pipeline controls")
    st.write("Use the demo dataset to run the complete local pipeline.")
    if st.button("1 · Generate sample data", use_container_width=True):
        generate_sample_data()
        st.success("Sample CSV created in data/raw/orders.csv")
    if st.button("2 · Run ETL pipeline", type="primary", use_container_width=True):
        try:
            with st.spinner("Extracting, cleaning and loading data..."):
                report = run_pipeline()
            st.session_state["last_report"] = report
            st.success("Pipeline completed successfully.")
        except Exception as exc:
            st.error(f"Pipeline failed: {exc}")
    st.divider()
    st.markdown("**Data source**")
    st.code("data/raw/orders.csv")
    st.markdown("**Warehouse**")
    st.code("DATABASE_URL from .env")

engine = get_engine()

def load_table(sql):
    try:
        with engine.connect() as conn:
            return pd.read_sql(text(sql), conn)
    except Exception:
        return pd.DataFrame()

orders = load_table("SELECT * FROM fact_orders")
if orders.empty:
    st.info("No warehouse data found yet. In the sidebar, click **Generate sample data**, then **Run ETL pipeline**.")
    st.stop()

orders["order_date"] = pd.to_datetime(orders["order_date"], errors="coerce")
delivered = orders[orders["order_status"] == "Delivered"].copy()

st.subheader("Business performance overview")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Delivered revenue", f"₹{delivered['revenue'].sum():,.0f}")
c2.metric("Total orders", f"{len(orders):,}")
c3.metric("Delivered orders", f"{len(delivered):,}")
c4.metric("Unique customers", f"{orders['customer_id'].nunique():,}")

left, right = st.columns(2)
with left:
    monthly = delivered.groupby("order_month", as_index=False)["revenue"].sum().sort_values("order_month")
    fig = px.line(monthly, x="order_month", y="revenue", markers=True,
                  title="Monthly delivered revenue", labels={"order_month":"Month","revenue":"Revenue (₹)"})
    st.plotly_chart(fig, use_container_width=True)
with right:
    status = orders.groupby("order_status", as_index=False).size()
    fig = px.pie(status, names="order_status", values="size", hole=0.55, title="Order status distribution")
    st.plotly_chart(fig, use_container_width=True)

products = load_table("""SELECT p.product_name, p.category, SUM(f.revenue) AS revenue
FROM fact_orders f JOIN dim_products p ON f.product_id=p.product_id
WHERE f.order_status='Delivered'
GROUP BY p.product_name, p.category ORDER BY revenue DESC""")
cities = load_table("""SELECT c.customer_city, SUM(f.revenue) AS revenue
FROM fact_orders f JOIN dim_customers c ON f.customer_id=c.customer_id
WHERE f.order_status='Delivered'
GROUP BY c.customer_city ORDER BY revenue DESC""")
left, right = st.columns(2)
with left:
    st.plotly_chart(px.bar(products, x="product_name", y="revenue", color="category",
                           title="Revenue by product", labels={"product_name":"Product","revenue":"Revenue (₹)"}),
                    use_container_width=True)
with right:
    st.plotly_chart(px.bar(cities, x="customer_city", y="revenue",
                           title="Revenue by customer city", labels={"customer_city":"City","revenue":"Revenue (₹)"}),
                    use_container_width=True)

st.subheader("Explore orders")
statuses = ["All"] + sorted(orders["order_status"].dropna().unique().tolist())
selected_status = st.selectbox("Filter by order status", statuses)
filtered = orders if selected_status == "All" else orders[orders["order_status"] == selected_status]
st.dataframe(filtered.sort_values("order_date", ascending=False), use_container_width=True, hide_index=True)

st.subheader("SQL query explorer")
query_name = st.selectbox("Choose a prebuilt analytical query", list(QUERIES.keys()))
if st.button("Run selected SQL query"):
    result = load_table(QUERIES[query_name])
    st.dataframe(result, use_container_width=True, hide_index=True)

report_path = PROCESSED_DIR / "pipeline_report.json"
if report_path.exists():
    st.subheader("Latest data quality report")
    report = json.loads(report_path.read_text(encoding="utf-8"))
    st.json(report)
