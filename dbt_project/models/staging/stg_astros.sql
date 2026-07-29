{{ config(materialized='view') }}

with source_data as (
    select
        craft,
        name,
        _inserted_at
    from {{ source('raw_data', 'people') }}
)

select
    trim(craft) as craft,
    trim(name) as name,
    _inserted_at
from source_data