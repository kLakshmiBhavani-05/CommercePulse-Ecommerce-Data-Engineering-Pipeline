import json
from src.config import RAW_DIR, PROCESSED_DIR
from src.extract import extract_orders
from src.transform import transform_orders
from src.load import load_to_warehouse
from src.logger import get_logger

logger = get_logger()

def run_pipeline():
    raw = extract_orders()
    clean, quality = transform_orders(raw)
    processed_path = PROCESSED_DIR / "clean_orders.csv"
    clean.to_csv(processed_path, index=False)
    load_counts = load_to_warehouse(clean)
    report = {"data_quality": quality, "warehouse_load": load_counts,
              "processed_file": str(processed_path)}
    report_path = PROCESSED_DIR / "pipeline_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logger.info("Pipeline finished successfully. Report: %s", report_path)
    return report

if __name__ == "__main__":
    print(json.dumps(run_pipeline(), indent=2))
