with pivoted as (
    select
        date,
        max(case when metric = 'lf' then value end) as lf,
        max(case when metric = 'p_rate' then value end) as p_rate,
        max(case when metric = 'u_rate' then value end) as u_rate,
        max(case when metric = 'ep_ratio' then value end) as ep_ratio,
        max(case when metric = 'lf_outside' then value end) as lf_outside,
        max(case when metric = 'lf_employed' then value end) as lf_employed,
        max(case when metric = 'lf_unemployed' then value end) as lf_unemployed
    from {{ ref('labour_monthly') }}
    group by date
)
select
    date,
    lf,
    p_rate,
    u_rate,
    ep_ratio,
    lf_outside,
    lf_employed,
    lf_unemployed,
    avg(u_rate) over (order by date rows between 2 preceding and current row) as unemployment_trend,
    case
        when u_rate - lag(u_rate) over (order by date) < 0 then 'improving'
        when u_rate - lag(u_rate) over (order by date) > 0 then 'worsening'
        else 'stable'
    end as unemployment_direction
from pivoted
