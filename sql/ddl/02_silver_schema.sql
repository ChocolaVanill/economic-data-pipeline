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