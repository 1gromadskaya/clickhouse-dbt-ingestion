{{ config(materialized='table') }}

with staging as (
    select * from {{ ref('stg_astros') }}
)

select
    craft,
    count(distinct name) as crew_count,
    max(_inserted_at) as last_updated_at
from staging
group by craft
order by crew_count desc