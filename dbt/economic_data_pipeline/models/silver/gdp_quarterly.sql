with latest as (
    select raw_data
    from {{ source('bronze', 'gdp_raw') }}
    order by ingestion_timestamp desc
    limit 1
),
records as (
    select *
    from jsonb_to_recordset((select raw_data from latest))
         as x(date text, value text, series text)
)
select distinct on (date, series)
    date::date as date,
    nullif(value, '')::numeric as value,
    series
from records
where date is not null
order by date, series
