CREATE SCHEMA IF NOT EXISTS gold;

-- Economic Indicators Monthly Summary
CREATE TABLE IF NOT EXISTS gold.economic_indicators_monthly (
    indicator_month DATE PRIMARY KEY,
    gdp_value DECIMAL(15,2),
    gdp_growth_yoy DECIMAL(5,2),
    gdp_growth_qoq DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS gold.gdp_trends (
    trend_date DATE PRIMARY KEY,
    gdp_value DECIMAL(15,2),
    ma_3_quarter DECIMAL(15,2),
    yoy_change_pct DECIMAL(5,2),
    trend_direction VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);