# 🇲🇾 Malaysia Economic Data Pipeline

Production-grade data engineering pipeline for Malaysian economic indicators sourced from data.gov.my.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-336791)
![dbt](https://img.shields.io/badge/dbt-Transformations-FF694B)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B)
![Docker](https://img.shields.io/badge/Docker-Supported-2496ED)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF)

## Overview

- **Medallion architecture**: Bronze → Silver → Gold
- **5 data sources**: GDP, CPI, Labour Force, Exchange Rates, Population
- **Transformations**: dbt (SQL)
- **Data quality**: Pydantic + custom validators
- **Dashboard**: Streamlit + Plotly

## Architecture

```
┌─────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌───────────────┐
│ data.gov.my │ →  │    Bronze    │ →  │    Silver    │ →  │     Gold     │ →  │   Streamlit   │
│    APIs     │    │  (Raw JSON)  │    │  (Cleaned)   │    │ (Aggregated) │    │   Dashboard   │
└─────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └───────────────┘
                          ↓                   ↓                   ↓
                   ┌──────────────────────────────────────────────────┐
                   │        Data Quality Validation Layer            │
                   │   (Pydantic Schemas + Custom Validators)        │
                   └──────────────────────────────────────────────────┘
```

## Quick Start

### Option 1: Docker (Recommended)

```bash
git clone https://github.com/sofaquitegud/economic-data-pipeline.git
cd economic-data-pipeline

# Configure environment
cp .env.example .env

# Configure dbt profile (reads env vars)
cp dbt/profiles.yml.example dbt/profiles.yml

# Start services (Airflow uses Celery + Redis)
docker compose up -d

# Access services:
# - Streamlit Dashboard: http://localhost:8501
# - Airflow UI: http://localhost:8080 (admin/admin)
```

Notes:
- For Supabase, set `POSTGRES_HOST/PORT/USER/PASSWORD/DB` in `.env`.
- For the Airflow metadata DB, set `AIRFLOW_DB_USER/AIRFLOW_DB_PASSWORD/AIRFLOW_DB_NAME` in `.env`.
- Local Postgres is optional: `docker compose --profile local-db up` (not used with Supabase).

### Option 2: Local Development

```bash
# Clone repository
git clone https://github.com/sofaquitegud/economic-data-pipeline.git
cd economic-data-pipeline

# Set up environment (conda or venv)
conda create -n data-eng python=3.11 -y
conda activate data-eng
pip install -r requirements.txt

# Configure database
cp .env.example .env
# Edit .env with your PostgreSQL credentials

# Load env vars for dbt
set -a
source .env
set +a

# Create database schema (bronze only)
psql -U your_user -h localhost -d malaysia_data -f sql/ddl/01_bronze_schema.sql

# Run ingestion
python -m src.ingestion.gdp_ingestion
python -m src.ingestion.cpi_ingestion

# Configure dbt
cp dbt/profiles.yml.example dbt/profiles.yml

# Run transformations (dbt)
dbt build --project-dir dbt/economic_data_pipeline --profiles-dir dbt

# Launch dashboard
streamlit run dashboards/streamlit/app.py
```

## dbt Workflow

```bash
dbt debug --project-dir dbt/economic_data_pipeline --profiles-dir dbt
dbt build --project-dir dbt/economic_data_pipeline --profiles-dir dbt
```

Notes:
- dbt models read the latest `bronze.*_raw` batch and create `analytics_silver` and `analytics_gold` schemas.
- Only `sql/ddl/01_bronze_schema.sql` is needed for setup.

## Airflow

The Airflow DAG runs ingestion, then executes dbt:

```
dbt build --project-dir dbt/economic_data_pipeline --profiles-dir /opt/airflow/.dbt
```

Docker mounts your dbt profile at `/opt/airflow/.dbt/profiles.yml`.

## Testing

```bash
PYTHONPATH=. pytest tests/ -v
PYTHONPATH=. pytest tests/ -v --cov=src
```

## Project Structure

```
├── config/                     # Configuration & schemas
│   ├── database.py             # Database connection
│   ├── api_endpoints.py        # API endpoint definitions
│   └── schema.py               # Pydantic data models
├── src/
│   ├── ingestion/              # API data ingestion scripts
│   ├── quality/                # Data validation framework
│   │   └── validators.py       # DataQualityValidator class
│   └── utils/                  # Logging & helpers
├── dbt/                        # dbt project (models + profiles example)
├── tests/                      # Unit tests (pytest)
│   ├── test_ingestion.py       # API client tests
│   └── test_quality.py         # Validator tests
├── sql/ddl/                    # Database schema definitions (bronze)
├── dashboards/streamlit/       # Interactive dashboard
├── airflow/                    # Airflow DAGs
├── docker-compose.yml          # Docker orchestration
├── Dockerfile                  # Container definition
└── requirements.txt
```

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.10+ |
| Database | PostgreSQL 14+ |
| Transformations | dbt (SQL) |
| Dashboard | Streamlit, Plotly |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| Testing | Pytest |
| Containerization | Docker, Docker Compose |
| Orchestration | Apache Airflow |

## Data Sources

| Dataset | Frequency | API Endpoint | Gold Metrics |
|---------|-----------|--------------|--------------|
| GDP | Quarterly | `gdp_qtr_real` | YoY growth, moving averages |
| CPI | Monthly | `cpi_headline` | MoM/YoY inflation, trends |
| Labour Force | Monthly | `lfs_month` | Unemployment rate, participation |
| Exchange Rates | Daily | `exchangerates_daily_1700` | Volatility, moving averages |
| Population | Annual | `population_malaysia` | Growth rate, demographics |

## Data Quality

- **Schema Validation**: Pydantic models ensure type safety at ingestion
- **Custom Validators**: Nulls, duplicates, date ranges, outliers
- **Per-Dataset Rules**: Tailored checks per dataset

```python
from src.quality.validators import validate_gdp

report = validate_gdp(df)
passed = report["passed"]
```

## Dashboard

The Streamlit dashboard includes:
- **GDP Overview**: GDP trends with moving averages and YoY growth
- **CPI Trends**: Monthly inflation rates by category with MoM/YoY analysis
- **Labour Market**: Employment statistics and unemployment rate trends
- **Exchange Rates**: Currency analytics with volatility metrics
- Interactive filters and exploration

## Roadmap

- [x] Medallion Architecture (Bronze/Silver/Gold)
- [x] Data Quality Validators
- [x] Pydantic Schema Validation
- [x] Unit Tests (Pytest)
- [x] Docker Support
- [x] dbt Transformations
- [x] CI/CD Pipeline (GitHub Actions)
- [x] Dashboard Pages (GDP, CPI, Labour, Exchange Rates)
- [ ] Alerting & Monitoring
- [ ] Data Lineage Visualization

## License

MIT License

## Author

**Syafiq**  
🐙 [GitHub](https://github.com/sofaquitegud)
