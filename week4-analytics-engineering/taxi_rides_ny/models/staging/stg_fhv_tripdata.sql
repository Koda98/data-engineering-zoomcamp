{{ config(materialized='view') }}

select
    -- identifiers
    dispatching_base_num,
    Affiliated_base_number,
    cast(pulocationid as integer) as  pickup_locationid,
    cast(dolocationid as integer) as dropoff_locationid,
    
    -- timestamps
    cast(pickup_datetime as timestamp) as pickup_datetime,
    cast(dropoff_datetime as timestamp) as dropoff_datetime,
    
    -- trip info
    cast(SR_Flag as integer) as sr_flag
    
from {{ source('staging','fhv_tripdata') }}
where pickup_datetime >= "2019-01-01 00:00:00" AND pickup_datetime <= "2029-12-31 23:59:59"


-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}
