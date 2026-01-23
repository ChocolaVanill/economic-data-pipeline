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
    df.to_sql('gdp_quarterly', engine, schema='silver', if_exists='replace', index=False)

    logger.info(f"Transformed {len(df)} records to silver.gdp_quarterly")


def transform_cpi_to_silver():
    engine = get_engine()

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT raw_data
            FROM bronze.cpi_raw
            ORDER BY ingestion_timestamp DESC
            LIMIT 1
        """))
        row = result.fetchone()

    if not row:
        logger.warning("No CPI data in bronze layer")
        return

    data = row[0]
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df['value'] = pd.to_numeric(df['index'], errors='coerce')
    df['category'] = df['division']
    df = df[['date', 'value', 'category']]
    df = df.drop_duplicates(subset=['date', 'category'], keep='last')

    df.to_sql('cpi_monthly', engine, schema='silver', if_exists='replace', index=False)
    logger.info(f"Transformed {len(df)} records to silver.cpi_monthly")


def transform_labour_to_silver():
    engine = get_engine()

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT raw_data
            FROM bronze.labour_raw
            ORDER BY ingestion_timestamp DESC
            LIMIT 1
        """))
        row = result.fetchone()

    if not row:
        logger.warning("No Labour data in bronze layer")
        return

    data = row[0]
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    
    # Melt to long format (metric + value)
    metrics = ['lf', 'p_rate', 'u_rate', 'ep_ratio', 'lf_outside', 'lf_employed', 'lf_unemployed']
    df_melted = df.melt(id_vars=['date'], value_vars=metrics, var_name='metric', value_name='value')
    df_melted['value'] = pd.to_numeric(df_melted['value'], errors='coerce')
    df_melted = df_melted.drop_duplicates(subset=['date', 'metric'], keep='last')

    df_melted.to_sql('labour_monthly', engine, schema='silver', if_exists='replace', index=False)
    logger.info(f"Transformed {len(df_melted)} records to silver.labour_monthly")


def transform_exchange_rates_to_silver():
    engine = get_engine()

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT raw_data
            FROM bronze.exchange_rates_raw
            ORDER BY ingestion_timestamp DESC
            LIMIT 1
        """))
        row = result.fetchone()

    if not row:
        logger.warning("No Exchange Rates data in bronze layer")
        return

    data = row[0]
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    
    # Get currency columns (exclude date and rate_type)
    currency_cols = [col for col in df.columns if col not in ['date', 'rate_type']]
    
    # Melt to long format
    df_melted = df.melt(id_vars=['date'], value_vars=currency_cols, var_name='currency_code', value_name='rate')
    df_melted['rate'] = pd.to_numeric(df_melted['rate'], errors='coerce')
    df_melted = df_melted.dropna(subset=['rate'])
    df_melted = df_melted.drop_duplicates(subset=['date', 'currency_code'], keep='last')

    df_melted.to_sql('exchange_rates_daily', engine, schema='silver', if_exists='replace', index=False)
    logger.info(f"Transformed {len(df_melted)} records to silver.exchange_rates_daily")


def transform_population_to_silver():
    engine = get_engine()

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT raw_data
            FROM bronze.population_raw
            ORDER BY ingestion_timestamp DESC
            LIMIT 1
        """))
        row = result.fetchone()

    if not row:
        logger.warning("No Population data in bronze layer")
        return

    data = row[0]
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df['population'] = pd.to_numeric(df['population'], errors='coerce')
    # Columns: age, sex, date, ethnicity, population - already match schema!

    df.to_sql('population_annual', engine, schema='silver', if_exists='replace', index=False)
    logger.info(f"Transformed {len(df)} records to silver.population_annual")


if __name__ == "__main__":
    transform_gdp_to_silver()
    transform_cpi_to_silver()
    transform_labour_to_silver()
    transform_exchange_rates_to_silver()
    transform_population_to_silver()