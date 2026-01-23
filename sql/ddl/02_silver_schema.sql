CREATE SCHEMA IF NOT EXISTS silver;

-- GDP Quarterly cleaned
CREATE TABLE IF NOT EXISTS silver.gdp_quarterly (
    gdp_id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    value DECIMAL(15,2),
    series VARCHAR(50),
    year INT GENERATED ALWAYS AS (EXTRACT(YEAR from date)) STORED,
    quarter INT GENERATED ALWAYS AS (EXTRACT(QUARTER FROM date)) STORED,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(date, series)
);

-- CPI Headline cleaned
CREATE TABLE IF NOT EXISTS silver.cpi_monthly (
    cpi_id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    value DECIMAL(10,2),
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(date, category)
);

-- Labour Force Monthly
CREATE TABLE IF NOT EXISTS silver.labour_monthly (
    labour_id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    metric VARCHAR(100),
    value DECIMAL(15,2),
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(date, metric)
);

-- Exchange Rates Daily
CREATE TABLE IF NOT EXISTS silver.exchange_rates_daily (
    rate_id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    currency_code VARCHAR(10),
    rate DECIMAL(12,6),
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(date, currency_code)
);

-- Population Annual
CREATE TABLE IF NOT EXISTS silver.population_annual (
    pop_id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    state VARCHAR(100),
    ethnicity VARCHAR(100),
    sex VARCHAR(20),
    age VARCHAR(50),
    population INT,
    created_at TIMESTAMP DEFAULT NOW()
);