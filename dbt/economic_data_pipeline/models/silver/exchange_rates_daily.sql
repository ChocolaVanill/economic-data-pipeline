with latest as (
    select raw_data
    from {{ source('bronze', 'exchange_rates_raw') }}
    order by ingestion_timestamp desc
    limit 1
),
records as (
    select jsonb_array_elements((select raw_data from latest)) as obj
),
long_format as (
    select
        (obj->>'date')::date as date,
        kv.key as currency_code,
        nullif(kv.value, '')::numeric as rate
    from records
    cross join lateral jsonb_each_text(obj) as kv(key, value)
    where kv.key not in ('date', 'rate_type')
)
select distinct on (date, currency_code)
    date,
    currency_code,
    rate
from long_format
where date is not null and rate is not null
order by date, currency_code
