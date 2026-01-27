select
    date,
    category,
    value,
    (value / nullif(lag(value) over (partition by category order by date), 0) - 1) * 100 as mom_change_pct,
    (value / nullif(lag(value, 12) over (partition by category order by date), 0) - 1) * 100 as yoy_change_pct,
    avg(value) over (partition by category order by date rows between 2 preceding and current row) as ma_3_month
from {{ ref('cpi_monthly') }}
