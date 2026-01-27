with base as (
    select
        date,
        value
    from {{ ref('gdp_quarterly') }}
    where series = 'abs'
)
select
    date as trend_date,
    value as gdp_value,
    avg(value) over (order by date rows between 2 preceding and current row) as ma_3_quarter,
    (value / nullif(lag(value, 4) over (order by date), 0) - 1) * 100 as yoy_change_pct,
    case
        when value - lag(value) over (order by date) > 0 then 'increasing'
        when value - lag(value) over (order by date) < 0 then 'decreasing'
        else 'stable'
    end as trend_direction
from base
