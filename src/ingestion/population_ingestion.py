# Import libraries
import json
import uuid

from sqlalchemy import text

from config.api_endpoints import ENDPOINTS
from config.database import get_engine
from src.ingestion.api_client import APIClient
from src.utils.logger import get_logger

logger = get_logger(__name__)


def ingest_population_data() -> str:
    client = APIClient()
    engine = get_engine()
    batch_id = str(uuid.uuid4())

    logger.info("Fetching population data from API...")
    data = client.fetch(ENDPOINTS["population"])

    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO bronze.population_raw
                (api_endpoint, response_status, raw_data, row_count, ingestion_batch_id)
                VALUES (:endpoint, :status, :data, :count, :batch_id)
                """),
            {
                "endpoint": ENDPOINTS["population"],
                "status": 200,
                "data": json.dumps(data),
                "count": len(data) if isinstance(data, list) else 1,
                "batch_id": batch_id,
            },
        )
        conn.commit()

    logger.info(f"Ingested {len(data)} population records with batch_id: {batch_id}")
    return batch_id


if __name__ == "__main__":
    ingest_population_data()
