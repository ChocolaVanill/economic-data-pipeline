# Import libraries
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup

# Default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=30)
}

# Pipeline base path
PIPELINE_PATH = '/opt/airflow/pipeline'

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

    # INGESTION TASKS
    with TaskGroup('ingestion', tooltip='Ingest data from data.gov.my') as ingestion_group:

        ingest_gdp = BashOperator(
            task_id='gdp',
            bash_command=f'cd {PIPELINE_PATH} && python -m src.ingestion.gdp_ingestion'
        )

        ingest_cpi = BashOperator(
            task_id='cpi',
            bash_command=f'cd {PIPELINE_PATH} && python -m src.ingestion.cpi_ingestion'
        )

        ingest_labour = BashOperator(
            task_id='labour',
            bash_command=f'cd {PIPELINE_PATH} && python -m src.ingestion.labour_ingestion'
        )

        ingest_exchange = BashOperator(
            task_id='exchange_rates',
            bash_command=f'cd {PIPELINE_PATH} && python -m src.ingestion.exchange_rate_ingestion'
        )

        ingest_population = BashOperator(
            task_id='population',
            bash_command=f'cd {PIPELINE_PATH} && python -m src.ingestion.population_ingestion'
        )

    # TRANSFORMATION TASKS
    with TaskGroup('transformation', tooltip='Bronze -> Silver -> Gold') as transform_group:

        transform_silver = BashOperator(
            task_id='bronze_to_silver',
            bash_command=f'cd {PIPELINE_PATH} && python -m src.transformation.bronze_to_silver'
        )

        transform_gold = BashOperator(
            task_id='silver_to_gold',
            bash_command=f'cd {PIPELINE_PATH} && python -m src.transformation.silver_to_gold'
        )

        transform_silver >> transform_gold

    # DATA QUALITY CHECK
    def run_data_quality_checks():
        """Run data quality validators on gold tables"""
        import sys
        sys.path.insert(0, PIPELINE_PATH)

        from src.quality.validators import validate_gdp, validate_cpi
        from config.database import get_engine
        import pandas as pd

        engine = get_engine()

        # Validate GDP
        gdp_df = pd.read_sql('SELECT * FROM gold.gdp_trends', engine)
        gdp_report = validate_gdp(gdp_df)
        if not gdp_report['passed']:
            raise ValueError(f"GDP quality check failed: {gdp_report['issues']}")

        # Validate CPI
        cpi_df = pd.read_sql('SELECT * FROM gold.cpi_trends', engine)
        cpi_report = validate_cpi(cpi_df)
        if not cpi_report['passed']:
            raise ValueError(f"CPI quality check failed: {cpi_report['issues']}")

        print("✅ All data quality checks passed!")

    quality_check = PythonOperator(
        task_id='data_quality_check',
        python_callable=run_data_quality_checks
    )

    # TASK DEPENDENCIES
    ingestion_group >> transform_group >> quality_check