CREATE SCHEMA IF NOT EXISTS bronze;

-- GDP Raw Table
CREATE TABLE IF NOT EXISTS bronze.gdp_raw (
    id SERIAL PRIMARY KEY,
    ingestion_timestamp TIMESTAMP DEFAULT NOW(),
    api_endpoint VARCHAR(255),
    response_status INT,
    raw_data JSONB,
    row_count INT,
    ingestion_batch_id UUID
);

-- CPI Raw Table
CREATE TABLE IF NOT EXISTS bronze.cpi_raw (
    id SERIAL PRIMARY KEY,
    ingestion_timestamp TIMESTAMP DEFAULT NOW(),
    api_endpoint VARCHAR(255),
    response_status INT,
    raw_data JSONB,
    row_count INT,
    ingestion_batch_id UUID
);

-- Labour Force Raw Table
CREATE TABLE IF NOT EXISTS bronze.labour_raw (
    id SERIAL PRIMARY KEY,
    ingestion_timestamp TIMESTAMP DEFAULT NOW(),
    api_endpoint VARCHAR(255),
    response_status INT,
    raw_data JSONB,
    row_count INT,
    ingestion_batch_id UUID
);

-- Exchange Rates Raw Table
CREATE TABLE IF NOT EXISTS bronze.exchange_rates_raw (
    id SERIAL PRIMARY KEY,
    ingestion_timestamp TIMESTAMP DEFAULT NOW(),
    api_endpoint VARCHAR(255),
    response_status INT,
    raw_data JSONB,
    row_count INT,
    ingestion_batch_id UUID
);

-- Population Raw Table
CREATE TABLE IF NOT EXISTS bronze.population_raw (
    id SERIAL PRIMARY KEY,
    ingestion_timestamp TIMESTAMP DEFAULT NOW(),
    api_endpoint VARCHAR(255),
    response_status INT,
    raw_data JSONB,
    row_count INT,
    ingestion_batch_id UUID
);