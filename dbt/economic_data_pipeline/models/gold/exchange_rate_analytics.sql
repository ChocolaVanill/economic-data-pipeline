select
    date,
    currency_code,
    rate,
    (rate / nullif(lag(rate) over (partition by currency_code order by date), 0) - 1) * 100 as daily_change_pct,
    avg(rate) over (partition by currency_code order by date rows between 6 preceding and current row) as ma_7_day,
    stddev_samp(rate) over (partition by currency_code order by date rows between 6 preceding and current row) as volatility_7d
from {{ ref('exchange_rates_daily') }}
