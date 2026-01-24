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


def transform_cpi_to_gold():
    engine = get_engine()

    query = """
        SELECT date, value, category
        FROM silver.cpi_monthly
        ORDER BY date
    """
    df = pd.read_sql(query, engine)

    if df.empty:
        logger.warning("No CPI data in silver layer")
        return

    # Calculate metrics per category
    results = []
    for category, group in df.groupby('category'):
        group = group.sort_values('date')
        group['mom_change_pct'] = group['value'].pct_change() * 100
        group['yoy_change_pct'] = group['value'].pct_change(12) * 100
        group['ma_3_month'] = group['value'].rolling(window=3).mean()
        results.append(group)

    gold_df = pd.concat(results)
    gold_df = gold_df[['date', 'category', 'value', 'mom_change_pct', 'yoy_change_pct', 'ma_3_month']]
    gold_df.to_sql('cpi_trends', engine, schema='gold', if_exists='replace', index=False)

    logger.info(f"Transformed {len(gold_df)} records to gold.cpi_trends")


def transform_labour_to_gold():
    engine = get_engine()

    query = """
        SELECT date, metric, value
        FROM silver.labour_monthly
        ORDER BY date
    """
    df = pd.read_sql(query, engine)

    if df.empty:
        logger.warning("No Labour data in silver layer")
        return

    # Pivot to wide format for analysis
    pivot_df = df.pivot(index='date', columns='metric', values='value').reset_index()

    # Calculate trends
    if 'u_rate' in pivot_df.columns:
        pivot_df['unemployment_trend'] = pivot_df['u_rate'].rolling(window=3).mean()
        pivot_df['unemployment_direction'] = pivot_df['u_rate'].diff().apply(lambda x: 'improving' if x < 0 else ('worsening' if x > 0 else 'stable'))
        pivot_df.to_sql('labour_summary', engine, schema='gold', if_exists='replace', index=False)

        logger.info(f"Transformed {len(pivot_df)} records to gold.labour_summary")


def transform_exchange_rates_to_gold():
    engine = get_engine()

    query = """
        SELECT date, currency_code, rate
        FROM silver.exchange_rates_daily
        ORDER BY date
    """
    df = pd.read_sql(query, engine)

    if df.empty:
        logger.warning("No Exchange Rates data in silver layer")
        return

    # Calculate metrics per currency
    results = []
    for currency, group in df.groupby('currency_code'):
        group = group.sort_values('date')
        group['daily_change_pct'] = group['rate'].pct_change() * 100
        group['ma_7_day'] = group['rate'].rolling(window=7).mean()
        group['volatility_7d'] = group['rate'].rolling(window=7).std()
        results.append(group)

    gold_df = pd.concat(results)
    gold_df = gold_df[['date', 'currency_code', 'rate', 'daily_change_pct', 'ma_7_day', 'volatility_7d']]
    gold_df.to_sql('exchange_rate_analytics', engine, schema='gold', if_exists='replace', index=False)

    logger.info(f"Transformed {len(gold_df)} records to gold.exchange_rate_analytics")


def transform_population_to_gold():
    engine = get_engine()

    query = """
        SELECT date, sex, ethnicity, population
        FROM silver.population_annual
        ORDER BY date
    """
    df = pd.read_sql(query, engine)

    if df.empty:
        logger.warning("No Population data in silver layer")
        return

    # Aggregate by year
    summary = df.groupby('date').agg(total_population=('population', 'sum')).reset_index()
    summary['yoy_growth_pct'] = summary['total_population'].pct_change() * 100
    summary['yoy_growth_abs'] = summary['total_population'].diff()
    summary.to_sql('population_trends', engine, schema='gold', if_exists='replace', index=False)

    logger.info(f"Transformed {len(summary)} records to gold.population_trends")


if __name__ == "__main__":
    transform_gdp_to_gold()
    transform_cpi_to_gold()
    transform_labour_to_gold()
    transform_exchange_rates_to_gold()
    transform_population_to_gold()