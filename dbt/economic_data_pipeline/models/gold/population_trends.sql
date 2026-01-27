with summary as (
    select
        date,
        sum(population) as total_population
    from {{ ref('population_annual') }}
    group by date
)
select
    date,
    total_population,
    (total_population / nullif(lag(total_population) over (order by date), 0) - 1) * 100 as yoy_growth_pct,
    total_population - lag(total_population) over (order by date) as yoy_growth_abs
from summary
