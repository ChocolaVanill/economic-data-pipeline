# Malaysia Economic & Social Indicators Data Pipeline

A production-grade data engineering project that ingests, transforms, and visualizes real-world economic and social indicators from Malaysia's official open data portal (data.gov.my).

## 🎯 Project Overview

This project demonstrates a complete end-to-end data engineering pipeline using **real, messy, changing data** from Malaysian government APIs. It implements the Medallion Architecture (Bronze → Silver → Gold) to transform raw API data into actionable business intelligence.

### Why This Dataset?

- **Real-world complexity**: Multiple data sources with different update frequencies (daily, monthly, quarterly)
- **Data quality challenges**: Handling nulls, inconsistent formatting, and API changes
- **Business relevance**: Tracks Malaysia's economic health through multiple interconnected indicators
- **Scalability**: Can expand to 400+ datasets available on data.gov.my

## 📊 Key Metrics & Questions Answered

### Business Questions
1. **Economic Health**: How is Malaysia's GDP, unemployment, and inflation trending?
2. **Labor Market**: What's the relationship between job markets and household income?
3. **Price Stability**: How do consumer prices vary across states and categories?
4. **Social Indicators**: What's the relationship between healthcare access and population demographics?

### Dashboard KPIs
- GDP Growth Rate (YoY, QoQ)
- Unemployment Rate by State
- CPI Inflation by Category
- Labor Force Participation Rate
- Exchange Rate Trends (MYR vs Major Currencies)
- Population Growth & Migration Patterns

## 🏗️ Architecture

```
┌─────────────────┐
│   data.gov.my   │
│   Public APIs   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│     Python Ingestion Layer              │
│  (requests, pandas, sqlalchemy)         │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│     🥉 BRONZE LAYER (PostgreSQL)        │
│  • Raw JSON/CSV dumps                   │
│  • Minimal transformation               │
│  • Append-only audit trail              │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│     🥈 SILVER LAYER (PostgreSQL)        │
│  • Data type enforcement                │
│  • Null handling & deduplication        │
│  • Standardized schemas                 │
│  • Basic validations                    │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│     🥇 GOLD LAYER (PostgreSQL)          │
│  • Aggregated metrics                   │
│  • Business-ready tables                │
│  • Pre-calculated KPIs                  │
│  • Dimensional modeling                 │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│   Business Intelligence Layer           │
│   (Power BI / Metabase / Streamlit)    │
└─────────────────────────────────────────┘
```

## 🔧 Tech Stack

### Core Stack
- **Language**: Python 3.10+
- **Database**: PostgreSQL 14+
- **Orchestration**: Apache Airflow / Prefect
- **Visualization**: Power BI / Metabase / Streamlit
- **Version Control**: Git + GitHub

### Python Libraries
```
requests          # API calls
pandas            # Data manipulation
sqlalchemy        # Database ORM
psycopg2-binary   # PostgreSQL adapter
python-dotenv     # Environment variables
pydantic          # Data validation
great-expectations # Data quality checks
```

### Infrastructure (Optional)
- Docker & Docker Compose
- PostgreSQL (local or cloud)
- Airflow (local or managed)

## 📁 Project Structure

```
malaysia-data-pipeline/
│
├── README.md
├── requirements.txt
├── .env.example
├── docker-compose.yml
│
├── config/
│   ├── database.py          # DB connection settings
│   ├── api_endpoints.py     # API URLs and parameters
│   └── schemas.py           # Pydantic validation models
│
├── src/
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── api_client.py            # API wrapper with retry logic
│   │   ├── gdp_ingestion.py         # GDP data ingestion
│   │   ├── cpi_ingestion.py         # CPI data ingestion
│   │   ├── labour_ingestion.py      # Labour force data
│   │   ├── exchange_rate_ingestion.py
│   │   └── population_ingestion.py
│   │
│   ├── transformation/
│   │   ├── __init__.py
│   │   ├── bronze_to_silver.py      # Cleaning & standardization
│   │   └── silver_to_gold.py        # Business logic & aggregations
│   │
│   ├── quality/
│   │   ├── __init__.py
│   │   ├── validators.py            # Data quality checks
│   │   └── expectations.py          # Great Expectations suite
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py                # Logging configuration
│       └── helpers.py               # Common utilities
│
├── sql/
│   ├── ddl/
│   │   ├── 01_bronze_schema.sql
│   │   ├── 02_silver_schema.sql
│   │   └── 03_gold_schema.sql
│   │
│   └── dml/
│       ├── silver_transformations.sql
│       └── gold_aggregations.sql
│
├── airflow/
│   └── dags/
│       ├── daily_ingestion_dag.py
│       └── weekly_aggregation_dag.py
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_quality_analysis.ipynb
│   └── 03_visualization_prototypes.ipynb
│
├── tests/
│   ├── test_ingestion.py
│   ├── test_transformation.py
│   └── test_data_quality.py
│
└── dashboards/
    ├── power_bi/
    │   └── malaysia_economic_dashboard.pbix
    └── streamlit/
        └── app.py
```

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL 14+
- Git
- (Optional) Docker & Docker Compose

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/malaysia-data-pipeline.git
cd malaysia-data-pipeline
```

2. **Set up virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your PostgreSQL credentials
```

4. **Set up the database**
```bash
# Create database
createdb malaysia_data

# Run DDL scripts
psql -d malaysia_data -f sql/ddl/01_bronze_schema.sql
psql -d malaysia_data -f sql/ddl/02_silver_schema.sql
psql -d malaysia_data -f sql/ddl/03_gold_schema.sql
```

5. **Run initial data ingestion**
```bash
python src/ingestion/gdp_ingestion.py
python src/ingestion/cpi_ingestion.py
python src/ingestion/labour_ingestion.py
```

6. **Transform data through medallion layers**
```bash
python src/transformation/bronze_to_silver.py
python src/transformation/silver_to_gold.py
```

## 📊 Data Sources

### Selected APIs from data.gov.my

| Dataset | Update Frequency | API Endpoint | Business Value |
|---------|-----------------|--------------|----------------|
| **GDP (Quarterly)** | Quarterly | `/gdp_qtr_real` | Economic growth tracking |
| **CPI (Monthly)** | Monthly | `/cpi_headline` | Inflation monitoring |
| **Labour Force** | Monthly | `/lfs_month` | Employment trends |
| **Exchange Rates** | Daily | `/exchangerates_daily_1700` | Currency stability |
| **Population** | Annual | `/population_malaysia` | Demographic trends |
| **Household Income** | Annual | `/hh_income` | Income inequality tracking |

### API Authentication
The data.gov.my APIs are **open and do not require authentication**, making this project accessible to everyone. However, implement rate limiting and caching to be respectful of their infrastructure.

## 🥉 Bronze Layer

### Purpose
Store raw API responses with minimal transformation for audit trail and reprocessing capability.

### Schema Design
```sql
CREATE TABLE bronze.gdp_raw (
    id SERIAL PRIMARY KEY,
    ingestion_timestamp TIMESTAMP DEFAULT NOW(),
    api_endpoint VARCHAR(255),
    response_status INT,
    raw_data JSONB,
    row_count INT,
    ingestion_batch_id UUID
);
```

### Key Principles
- **Immutable**: Never delete or update bronze records
- **Complete**: Store entire API response including metadata
- **Timestamped**: Track when data was ingested
- **Batch tracking**: Use UUIDs to track ingestion runs

## 🥈 Silver Layer

### Purpose
Clean, deduplicated, validated data with enforced data types and business rules.

### Transformations
1. **Data Type Enforcement**
   - Convert string dates to DATE/TIMESTAMP
   - Cast numeric strings to DECIMAL/INTEGER
   - Standardize boolean representations

2. **Null Handling**
   - Identify null patterns in source data
   - Apply business rules (e.g., 0 vs NULL for economic indicators)
   - Flag incomplete records

3. **Deduplication**
   - Composite keys based on date + dimension
   - Use ROW_NUMBER() to identify duplicates
   - Keep most recent record based on ingestion_timestamp

4. **Validation**
   - Range checks (e.g., unemployment rate 0-100%)
   - Referential integrity (e.g., state codes exist)
   - Logical consistency (e.g., employed + unemployed = labour force)

### Schema Example
```sql
CREATE TABLE silver.gdp_quarterly (
    gdp_id SERIAL PRIMARY KEY,
    year INT NOT NULL,
    quarter INT NOT NULL CHECK (quarter BETWEEN 1 AND 4),
    gdp_value DECIMAL(15,2),
    gdp_growth_rate DECIMAL(5,2),
    sector VARCHAR(100),
    data_quality_flag VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(year, quarter, sector)
);
```

## 🥇 Gold Layer

### Purpose
Business-ready aggregated tables optimized for analytics and reporting.

### Key Tables

#### 1. Economic Health Dashboard
```sql
CREATE TABLE gold.economic_indicators_monthly (
    indicator_month DATE PRIMARY KEY,
    gdp_growth_yoy DECIMAL(5,2),
    gdp_growth_qoq DECIMAL(5,2),
    unemployment_rate DECIMAL(4,2),
    inflation_rate DECIMAL(5,2),
    labour_participation_rate DECIMAL(4,2),
    avg_exchange_rate_usd DECIMAL(8,4),
    population_employed INT,
    population_unemployed INT
);
```

#### 2. State-Level Comparative Analysis
```sql
CREATE TABLE gold.state_comparison (
    state_code VARCHAR(3),
    state_name VARCHAR(100),
    latest_month DATE,
    unemployment_rate DECIMAL(4,2),
    avg_household_income DECIMAL(12,2),
    cpi_index DECIMAL(8,2),
    population INT,
    labour_force INT,
    rank_by_income INT,
    rank_by_unemployment INT
);
```

#### 3. Time-Series Trends
```sql
CREATE TABLE gold.gdp_trends (
    trend_date DATE,
    gdp_value DECIMAL(15,2),
    ma_3_quarter DECIMAL(15,2),      -- 3-quarter moving average
    ma_12_month DECIMAL(15,2),        -- 12-month moving average
    yoy_change_pct DECIMAL(5,2),
    trend_direction VARCHAR(20)        -- 'increasing', 'decreasing', 'stable'
);
```

### Business Logic Examples

1. **GDP Growth Calculation**
```python
# Year-over-Year Growth
yoy_growth = ((current_quarter_gdp - same_quarter_last_year) / same_quarter_last_year) * 100

# Quarter-over-Quarter Growth
qoq_growth = ((current_quarter_gdp - previous_quarter_gdp) / previous_quarter_gdp) * 100
```

2. **Inflation Rate**
```python
# CPI-based inflation
inflation_rate = ((current_month_cpi - same_month_last_year_cpi) / same_month_last_year_cpi) * 100
```

## 🔄 Orchestration

### Airflow DAG Structure

#### Daily Ingestion DAG
```python
# High-frequency data sources
dag_daily = DAG(
    'malaysia_daily_ingestion',
    schedule_interval='0 18 * * *',  # 6 PM daily (after API updates)
    default_args={...}
)

# Tasks:
# 1. Ingest exchange rates (updates daily)
# 2. Check API health
# 3. Transform to silver layer
# 4. Run data quality checks
# 5. Update gold layer if needed
# 6. Send alerts on failures
```

#### Monthly Aggregation DAG
```python
# Monthly economic indicators
dag_monthly = DAG(
    'malaysia_monthly_aggregation',
    schedule_interval='0 2 1 * *',  # 2 AM on 1st of each month
    default_args={...}
)

# Tasks:
# 1. Ingest CPI data
# 2. Ingest labour force statistics
# 3. Transform bronze → silver
# 4. Calculate monthly KPIs
# 5. Update gold layer dashboards
# 6. Generate monthly report
```

## ✅ Data Quality Checks

### Validation Framework

#### 1. Schema Validation
```python
from pydantic import BaseModel, validator

class GDPRecord(BaseModel):
    year: int
    quarter: int
    gdp_value: float
    
    @validator('quarter')
    def quarter_must_be_valid(cls, v):
        if v not in [1, 2, 3, 4]:
            raise ValueError('Quarter must be 1, 2, 3, or 4')
        return v
    
    @validator('gdp_value')
    def gdp_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('GDP must be positive')
        return v
```

#### 2. Data Quality Metrics
- **Completeness**: % of non-null values
- **Uniqueness**: Check for duplicate records
- **Validity**: Range and format checks
- **Timeliness**: Data freshness checks
- **Consistency**: Cross-table referential integrity

#### 3. Automated Alerts
```python
# Alert conditions
ALERT_CONDITIONS = {
    'null_threshold': 5,           # Alert if >5% nulls
    'duplicate_threshold': 0,      # Alert on any duplicates
    'freshness_hours': 48,         # Alert if data >48 hours old
    'row_count_variance': 0.2      # Alert if ±20% from expected
}
```

### Monitoring Dashboard Metrics
- Pipeline success rate (last 30 days)
- Average execution time per DAG
- Data quality score by layer
- Row counts and growth trends
- API response times and errors

## 📈 Dashboard & Visualization

### Power BI Dashboard Pages

#### Page 1: Economic Overview
- GDP trend line (with YoY and QoQ growth)
- Unemployment rate by state (map visual)
- CPI inflation heatmap by category
- Key metrics cards (latest values)

#### Page 2: Labour Market Deep Dive
- Labour force participation trends
- Employment by sector (stacked area)
- Unemployment duration distribution
- State-by-state comparison table

#### Page 3: Price Stability
- CPI by main category (line charts)
- State-level price comparison
- Core vs headline inflation
- Currency exchange rate trends

### Streamlit Alternative
Build an interactive web dashboard:
```python
# streamlit/app.py
import streamlit as st
import plotly.express as px

st.title("Malaysia Economic Indicators Dashboard")

# GDP Trend
gdp_data = fetch_gold_data("gdp_trends")
fig = px.line(gdp_data, x='trend_date', y='gdp_value',
              title='Malaysia GDP Trend')
st.plotly_chart(fig)

# State comparison
state_data = fetch_gold_data("state_comparison")
fig2 = px.bar(state_data, x='state_name', y='unemployment_rate',
              title='Unemployment Rate by State')
st.plotly_chart(fig2)
```

## 🧪 Testing Strategy

### Unit Tests
```python
# tests/test_ingestion.py
def test_gdp_api_response():
    response = fetch_gdp_data(year=2024, quarter=1)
    assert response.status_code == 200
    assert 'data' in response.json()

def test_data_transformation():
    raw_data = mock_bronze_data()
    silver_data = transform_to_silver(raw_data)
    assert silver_data['gdp_value'].dtype == 'float64'
    assert silver_data['gdp_value'].notna().all()
```

### Integration Tests
- End-to-end pipeline execution
- Database connectivity checks
- API endpoint availability

### Data Quality Tests
- Great Expectations suite validation
- Row count reconciliation across layers
- Business logic correctness

## 📝 Development Workflow

### Git Workflow
1. **Branch naming**: `feature/gdp-ingestion`, `fix/null-handling`
2. **Commit messages**: Follow conventional commits
3. **Pull requests**: Require code review + passing tests
4. **CI/CD**: GitHub Actions for automated testing

### Code Quality
- **Linting**: Black, flake8, mypy
- **Documentation**: Docstrings for all functions
- **Type hints**: Use typing module consistently

## 🎓 Learning Outcomes

By completing this project, you'll demonstrate:

✅ **API Integration**: Handling real-world API data with error handling and retry logic  
✅ **Data Modeling**: Implementing Medallion Architecture in practice  
✅ **SQL Proficiency**: Complex transformations, window functions, CTEs  
✅ **Python Engineering**: Clean, modular, testable code  
✅ **Data Quality**: Validation, monitoring, and alerting  
✅ **Orchestration**: Building production-grade data pipelines  
✅ **Business Intelligence**: Translating data into actionable insights  
✅ **DevOps Basics**: Docker, environment management, CI/CD  

## 📚 Resources

### data.gov.my Documentation
- [API Documentation](https://developer.data.gov.my)
- [Data Catalogue](https://data.gov.my/data-catalogue)

### Learning Materials
- [Medallion Architecture by Databricks](https://www.databricks.com/glossary/medallion-architecture)
- [Apache Airflow Tutorial](https://airflow.apache.org/docs/apache-airflow/stable/tutorial.html)
- [Great Expectations Docs](https://docs.greatexpectations.io/)

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Add more data sources from data.gov.my
- Implement additional data quality checks
- Create more sophisticated gold-layer metrics
- Add machine learning forecasting models
- Improve dashboard visualizations

## 📄 License

MIT License - feel free to use this project for learning and portfolio purposes.

## 👤 Author

**[Your Name]**  
📧 [your.email@example.com]  
🔗 [LinkedIn](https://linkedin.com/in/yourprofile)  
🐙 [GitHub](https://github.com/yourusername)

---

## 🎯 Next Steps

1. ✅ Set up local environment
2. ✅ Connect to data.gov.my APIs
3. ✅ Build bronze layer ingestion
4. ✅ Implement silver transformations
5. ✅ Create gold aggregations
6. ✅ Set up Airflow orchestration
7. ✅ Build Power BI dashboard
8. ✅ Write comprehensive tests
9. ✅ Document everything
10. ✅ Deploy and monitor

**Start building today and showcase real data engineering skills!** 🚀