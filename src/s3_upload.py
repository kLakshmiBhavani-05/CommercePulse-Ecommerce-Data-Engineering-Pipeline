from pathlib import Path
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from src.config import AWS_REGION, S3_BUCKET, S3_PREFIX
from src.logger import get_logger

logger = get_logger()

def upload_file_to_s3(file_path: Path):
    if not S3_BUCKET:
        raise RuntimeError("S3_BUCKET is empty. Set it in your .env file before uploading.")
    client = boto3.client("s3", region_name=AWS_REGION)
    key = f"{S3_PREFIX}/{file_path.name}" if S3_PREFIX else file_path.name
    try:
        client.upload_file(str(file_path), S3_BUCKET, key)
        logger.info("Uploaded %s to s3://%s/%s", file_path, S3_BUCKET, key)
        return f"s3://{S3_BUCKET}/{key}"
    except (BotoCoreError, ClientError) as exc:
        logger.exception("S3 upload failed")
        raise RuntimeError(f"S3 upload failed: {exc}") from exc

if __name__ == "__main__":
    from src.config import PROCESSED_DIR
    print(upload_file_to_s3(PROCESSED_DIR / "clean_orders.csv"))
