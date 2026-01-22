# 🇲🇾 Malaysia Economic Data Pipeline

A production-grade data engineering project that ingests, transforms, and visualizes real-world economic indicators from Malaysia's official open data portal ([data.gov.my](https://data.gov.my)).

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-336791)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B)

## 🎯 Overview

This project implements the **Medallion Architecture** (Bronze → Silver → Gold) to transform raw API data into actionable business intelligence, featuring:

- **5 Data Sources**: GDP, CPI, Labour Force, Exchange Rates, Population
- **3-Layer Architecture**: Raw → Cleaned → Aggregated
- **Interactive Dashboard**: Built with Streamlit & Plotly

## 🏗️ Architecture

```
data.gov.my APIs → Bronze (Raw JSON) → Silver (Cleaned) → Gold (Aggregated) → Streamlit Dashboard
```

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/sofaquitegud/economic-data-pipeline.git
cd economic-data-pipeline

# Set up environment
python -m venv venv
source venv/bin/activate
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

## 📁 Project Structure

```
├── config/                 # Database & API configuration
├── src/
│   ├── ingestion/          # API data ingestion scripts
│   ├── transformation/     # Bronze → Silver → Gold transformations
│   └── utils/              # Logging & helpers
├── sql/ddl/                # Database schema definitions
├── dashboards/streamlit/   # Interactive dashboard
└── requirements.txt
```

## 🔧 Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.10+ |
| Database | PostgreSQL 14+ |
| Dashboard | Streamlit, Plotly |
| ORM | SQLAlchemy |

## 📊 Data Sources

| Dataset | Frequency | API Endpoint |
|---------|-----------|--------------|
| GDP | Quarterly | `gdp_qtr_real` |
| CPI | Monthly | `cpi_headline` |
| Labour Force | Monthly | `lfs_month` |
| Exchange Rates | Daily | `exchangerates_daily_1700` |
| Population | Annual | `population_malaysia` |

## 📈 Dashboard Preview

The Streamlit dashboard displays:
- GDP trends with moving averages
- Year-over-Year growth rates
- Interactive data exploration

## 📄 License

MIT License

## 👤 Author

**Syafiq**  
🐙 [GitHub](https://github.com/sofaquitegud)
