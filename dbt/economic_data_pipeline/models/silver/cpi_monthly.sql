with latest as (
    select raw_data
    from {{ source('bronze', 'cpi_raw') }}
    order by ingestion_timestamp desc
    limit 1
),
records as (
    select *
    from jsonb_to_recordset((select raw_data from latest))
         as x(date text, "index" text, division text)
)
select distinct on (date, category)
    date::date as date,
    nullif("index", '')::numeric as value,
    division as category
from records
where date is not null
order by date, category
