# Import libraries
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

# Default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

# DAG definition
with DAG(
    dag_id='economic_data_pipeline',
    default_args=default_args,
    description='Daily ingestion and transformation of Malaysian economic data',
    schedule_interval='0 6 * * *',  # Daily at 6 AM
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['economic', 'malaysia', 'etl']
) as dag:

    # Ingest GDP data
    ingest_gdp = BashOperator(
        task_id='ingest_gdp',
        bash_command='cd /opt/airflow/pipeline && python -m src.ingestion.gdp_ingestion'
    )

    # Ingest CPI data
    ingest_cpi = BashOperator(
        task_id='ingest_cpi',
        bash_command='cd /opt/airflow/pipeline && python -m src.ingestion.cpi_ingestion'
    )

    # Ingest Labour data
    ingest_labour = BashOperator(
        task_id='ingest_labour',
        bash_command='cd /opt/airflow/pipeline && python -m src.ingestion.labour_ingestion'
    )

    # Ingest Exchange Rate data
    ingest_exchange = BashOperator(
        task_id='ingest_exchange_rates',
        bash_command='cd /opt/airflow/pipeline && python -m src.ingestion.exchange_rate_ingestion'
    )

    # Ingest Population data
    ingest_population = BashOperator(
        task_id='ingest_population',
        bash_command='cd /opt/airflow/pipeline && python -m src.ingestion.population_ingestion'
    )

    # Transform Bronze to Silver
    transform_silver = BashOperator(
        task_id='transform_bronze_to_silver',
        bash_command='cd /opt/airflow/pipeline && python -m src.transformation.bronze_to_silver'
    )

    # Transform Silver to Gold
    transform_gold = BashOperator(
        task_id='transform_silver_to_gold',
        bash_command='cd /opt/airflow/pipeline && python -m src.transformation.silver_to_gold'
    )

    # Task dependencies
    [ingest_gdp, ingest_cpi, ingest_labour, ingest_exchange, ingest_population] >> transform_silver >> transform_gold