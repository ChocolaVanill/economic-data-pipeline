# Import libraries
import pandas as pd
from sqlalchemy import text
from config.database import get_engine
from src.utils.logger import get_logger


logger = get_logger(__name__)


def transform_gdp_to_gold():
    engine = get_engine()

    # Read silver GDP data
    query = """
        SELECT date, value, series
        FROM silver.gdp_quarterly
        WHERE series = 'abs'
        ORDER BY date
    """
    df = pd.read_sql(query, engine)

    if df.empty:
        logger.warning("No GDP data in silver layer")
        return

    # Calculate metrics
    df['yoy_change_pct'] = df['value'].pct_change(4) * 100
    df['ma_3_quarter'] = df['value'].rolling(window=3).mean()
    df['trend_direction'] = df['value'].diff().apply(lambda x: 'increasing' if x > 0 else ('decreasing' if x < 0 else 'stable'))

    # Prepare gold table data
    gold_df = df[['date', 'value', 'ma_3_quarter', 'yoy_change_pct', 'trend_direction']].copy()
    gold_df.columns = ['trend_date', 'gdp_value', 'ma_3_quarter', 'yoy_change_pct', 'trend_direction']

    # Load to gold
    gold_df.to_sql('gdp_trends', engine, schema='gold', if_exists='replace', index=False)

    logger.info(f"Transformed {len(gold_df)} records to gold.gdp_trends")


if __name__ == "__main__":
    transform_gdp_to_gold()