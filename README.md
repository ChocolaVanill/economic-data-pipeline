# 🇲🇾 Malaysia Economic Data Pipeline

A production-grade data engineering project that ingests, transforms, and visualizes real-world economic indicators from Malaysia's official open data portal ([data.gov.my](https://data.gov.my)).

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-336791)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B)
![Tests](https://img.shields.io/badge/Tests-12%20Passing-brightgreen)
![Docker](https://img.shields.io/badge/Docker-Supported-2496ED)

## 🎯 Overview

This project implements the **Medallion Architecture** (Bronze → Silver → Gold) to transform raw API data into actionable business intelligence, featuring:

- **5 Data Sources**: GDP, CPI, Labour Force, Exchange Rates, Population
- **3-Layer Architecture**: Raw → Cleaned → Aggregated
- **Data Quality Framework**: Pydantic schema validation + custom validators
- **Interactive Dashboard**: Built with Streamlit & Plotly
- **Docker Support**: Containerized deployment with Docker Compose

## 🏗️ Architecture

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

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
git clone https://github.com/sofaquitegud/economic-data-pipeline.git
cd economic-data-pipeline

# Start all services
docker-compose up -d

# Access services:
# - Streamlit Dashboard: http://localhost:8501
# - PostgreSQL: localhost:5432
```

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

# Create database schemas
psql -U your_user -h localhost -d malaysia_data -f sql/ddl/01_bronze_schema.sql
psql -U your_user -h localhost -d malaysia_data -f sql/ddl/02_silver_schema.sql
psql -U your_user -h localhost -d malaysia_data -f sql/ddl/03_gold_schema.sql

# Run ingestion
python -m src.ingestion.gdp_ingestion
python -m src.ingestion.cpi_ingestion

# Run transformations
python -m src.transformation.bronze_to_silver
python -m src.transformation.silver_to_gold

# Launch dashboard
streamlit run dashboards/streamlit/app.py
```

## 🧪 Testing

```bash
# Run all tests
PYTHONPATH=. pytest tests/ -v

# Run with coverage
PYTHONPATH=. pytest tests/ -v --cov=src
```

**Current status:** 12/12 tests passing ✅

## 📁 Project Structure

```
├── config/                     # Configuration & schemas
│   ├── database.py             # Database connection
│   ├── api_endpoints.py        # API endpoint definitions
│   └── schema.py               # Pydantic data models
├── src/
│   ├── ingestion/              # API data ingestion scripts
│   ├── transformation/         # Bronze → Silver → Gold transforms
│   ├── quality/                # Data validation framework
│   │   └── validators.py       # DataQualityValidator class
│   └── utils/                  # Logging & helpers
├── tests/                      # Unit tests (pytest)
│   ├── test_ingestion.py       # API client tests
│   └── test_transformation.py  # Transform & validator tests
├── sql/ddl/                    # Database schema definitions
├── dashboards/streamlit/       # Interactive dashboard
├── airflow/                    # Airflow DAGs (WIP)
├── docker-compose.yml          # Docker orchestration
├── Dockerfile                  # Container definition
└── requirements.txt
```

## 🔧 Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.10+ |
| Database | PostgreSQL 14+ |
| Dashboard | Streamlit, Plotly |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| Testing | Pytest |
| Containerization | Docker, Docker Compose |
| Orchestration | Apache Airflow (WIP) |

## 📊 Data Sources

| Dataset | Frequency | API Endpoint | Gold Metrics |
|---------|-----------|--------------|--------------|
| GDP | Quarterly | `gdp_qtr_real` | YoY growth, moving averages |
| CPI | Monthly | `cpi_headline` | MoM/YoY inflation, trends |
| Labour Force | Monthly | `lfs_month` | Unemployment rate, participation |
| Exchange Rates | Daily | `exchangerates_daily_1700` | Volatility, moving averages |
| Population | Annual | `population_malaysia` | Growth rate, demographics |

## ✅ Data Quality

The project includes a robust data quality framework:

- **Schema Validation**: Pydantic models ensure type safety at ingestion
- **Custom Validators**: Pre-built checks for nulls, duplicates, date ranges, and outliers
- **Per-Dataset Rules**: Each dataset has tailored validation rules

```python
from src.quality.validators import DataQualityValidator

validator = DataQualityValidator.for_gdp()
is_valid, report = validator.validate(df)
```

## 📈 Dashboard Features

The Streamlit dashboard displays:
- GDP trends with 4-quarter moving averages
- Year-over-Year and Month-over-Month growth rates
- CPI inflation breakdown
- Exchange rate volatility
- Interactive data exploration with filters

## 🗺️ Roadmap

- [x] Medallion Architecture (Bronze/Silver/Gold)
- [x] Data Quality Validators
- [x] Pydantic Schema Validation
- [x] Unit Tests (Pytest)
- [x] Docker Support
- [ ] Airflow DAGs for scheduling
- [ ] CI/CD Pipeline
- [ ] Additional dashboard pages

## 📄 License

MIT License

## 👤 Author

**Syafiq**  
🐙 [GitHub](https://github.com/sofaquitegud)
