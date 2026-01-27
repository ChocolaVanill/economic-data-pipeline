with latest as (
    select raw_data
    from {{ source('bronze', 'labour_raw') }}
    order by ingestion_timestamp desc
    limit 1
),
records as (
    select *
    from jsonb_to_recordset((select raw_data from latest))
         as x(
            date text,
            lf text,
            p_rate text,
            u_rate text,
            ep_ratio text,
            lf_outside text,
            lf_employed text,
            lf_unemployed text
         )
),
long_format as (
    select
        date::date as date,
        metric,
        nullif(value, '')::numeric as value
    from records
    cross join lateral (
        values
            ('lf', lf),
            ('p_rate', p_rate),
            ('u_rate', u_rate),
            ('ep_ratio', ep_ratio),
            ('lf_outside', lf_outside),
            ('lf_employed', lf_employed),
            ('lf_unemployed', lf_unemployed)
    ) as metrics(metric, value)
)
select distinct on (date, metric)
    date,
    metric,
    value
from long_format
where date is not null
order by date, metric
