# CommercePulse — E-commerce End-to-End Data Engineering Pipeline

A portfolio-ready local data engineering project demonstrating CSV ingestion, Python/Pandas ETL, data quality checks, a dimensional SQL warehouse, analytical SQL, and an interactive Streamlit dashboard. Optional configuration supports MySQL and Amazon S3.

## Architecture

CSV → Extract (Pandas) → Transform & Validate → MySQL/SQLite warehouse → SQL analytics → Streamlit dashboard

## 1. Requirements

- Python 3.10 or newer
- VS Code
- MySQL Server only if you choose MySQL; SQLite works out of the box
- Optional: AWS account and configured AWS credentials for S3 upload

## 2. Open in VS Code

1. Extract the ZIP.
2. VS Code → File → Open Folder → select `ecommerce-data-engineering`.
3. Open Terminal → New Terminal.

## 3. Create and activate a virtual environment

Windows PowerShell:
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```
If PowerShell blocks activation, use:
```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m src.generate_data
.venv\Scripts\python.exe -m src.pipeline
.venv\Scripts\python.exe -m streamlit run app.py
```
Or change the execution policy for the current terminal only:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

## 4. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Configure environment

Copy `.env.example` to `.env`. The default is SQLite, so no database server is required.

To use MySQL instead:
1. Start MySQL Server.
2. Create the database: `CREATE DATABASE ecommerce_dw;`
3. In `.env`, set:
   `DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/ecommerce_dw`
4. Replace `YOUR_PASSWORD` with your local MySQL password. Do not commit `.env` to GitHub.

## 6. Run the complete pipeline

```powershell
python -m src.generate_data
python -m src.pipeline
```

Expected outputs:
- `data/raw/orders.csv` — demo source data
- `data/processed/clean_orders.csv` — cleaned data
- `data/processed/pipeline_report.json` — quality and load metrics
- `data/warehouse.db` — SQLite warehouse (if using default config)
- `logs/pipeline.log` — execution log

The demo generator intentionally adds a duplicate, a missing optional field and an invalid quantity so you can demonstrate data-quality handling. The pipeline removes duplicates and invalid records and fills optional descriptive fields with `Unknown`.

## 7. Launch the interactive dashboard

```powershell
streamlit run app.py
```

The app opens in your browser. Use the sidebar buttons in order:
1. Generate sample data.
2. Run ETL pipeline.

Explore KPI cards, monthly revenue, order status, product/city charts, order filters, SQL query explorer and data-quality report.

## 8. Run tests

```powershell
pytest -q
```

## 9. Optional AWS S3 upload

1. Create an S3 bucket in AWS.
2. Configure AWS credentials securely using an IAM user/role and AWS CLI (`aws configure`); never hardcode keys in code or commit them.
3. Add bucket and region to `.env`:
   `S3_BUCKET=your-unique-bucket-name`
4. Run:
```powershell
python -m src.s3_upload
```
This uploads `data/processed/clean_orders.csv` to the configured S3 bucket. This optional script does not create Glue jobs, Redshift clusters or an EMR cluster.

## 10. GitHub publishing

```powershell
git init
git add .
git commit -m "Build end-to-end e-commerce data engineering pipeline"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ecommerce-data-engineering.git
git push -u origin main
```

Before pushing, check that `.env` and database files are not staged. Never publish passwords, AWS keys, customer personal data, or confidential datasets.

## Data model

- `dim_customers`: one row per customer
- `dim_products`: one row per product
- `fact_orders`: one row per order

This is a compact dimensional model for portfolio demonstration. For production, add surrogate keys, date dimension, incremental/CDC loading, orchestration, schema evolution, retries, monitoring, and access controls.

## Resume wording (only after implementation)

**CommercePulse — E-commerce Data Engineering Pipeline** | Python, Pandas, SQL, MySQL/SQLite, Streamlit, Plotly, AWS S3 (if implemented)

- Built a Python/Pandas ETL workflow to ingest, clean, validate and transform e-commerce order data.
- Designed a dimensional SQL warehouse with customer and product dimensions and an order fact table.
- Developed analytical SQL queries using joins, aggregations and window functions.
- Created an interactive dashboard to explore revenue trends, product performance, city-level sales and order quality.
- Added structured logging, pipeline metrics and automated transformation tests.

Be precise in interviews: the included AWS integration uploads a processed file to S3; it does not implement Glue, Redshift, EMR or Spark.
