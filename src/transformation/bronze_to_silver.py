# Import libraries
import pandas as pd
from sqlalchemy import text
from config.database import get_engine
from src.utils.logger import get_logger


logger = get_logger(__name__)


def transform_gdp_to_silver():
    engine = get_engine()

    # Read latest bronze data
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT raw_data
            FROM bronze.gdp_raw
            ORDER BY ingestion_timestamp DESC
            LIMIT 1
        """))
        row = result.fetchone()

    if not row:
        logger.warning("No GDP data in bronze layer")
        return

    # Transform
    data = row[0]
    df = pd.DataFrame(data)

    # Clean and transform
    df['date'] = pd.to_datetime(df['date'])
    df['value'] = pd.to_numeric(df['value'], errors='coerce')

    # Deduplicate
    df = df.drop_duplicates(subset=['date', 'series'], keep='last')

    # Load to silver
    df.to_sql('gdp_quarterly', engine, schema='silver', if_exists='append', index=False)

    logger.info(f"Transformed {len(df)} records to silver.gdp_quarterly")


if __name__ == "__main__":
    transform_gdp_to_silver()