with latest as (
    select raw_data
    from {{ source('bronze', 'population_raw') }}
    order by ingestion_timestamp desc
    limit 1
),
records as (
    select *
    from jsonb_to_recordset((select raw_data from latest))
         as x(
            date text,
            state text,
            ethnicity text,
            sex text,
            age text,
            population text
         )
)
select
    date::date as date,
    nullif(state, '') as state,
    nullif(ethnicity, '') as ethnicity,
    nullif(sex, '') as sex,
    nullif(age, '') as age,
    nullif(population, '')::numeric as population
from records
where date is not null
