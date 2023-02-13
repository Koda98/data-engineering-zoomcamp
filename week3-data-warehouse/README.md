# Data Warehouse and Big Query

## OLAP vs OLTP

| | OLTP (Online Transaction Processing) | OLAP (Online Analytical Processing) |
| - | - | - |
| Purpose | Type of database used in backend services. Used when you want to group SQL queries together and have the ability to roll back in case one of them fails. Control and run essential business operations in real time|Plan, solve problems, support decisions, discover hidden insights. Used for analytical purposes by data analysts/scientists |
| Data Updates |Short, fast updates initiated by user|Data periodically refreshed with scheduled, long-running batch jobs |
| Database Design | Normalized databases for efficiency | Denormalized databases for analysis |
| Space Requirements | Generally small if historical data is archived | Generally large due to aggregating large datasets |
| Backup and Recovery | Regular backups required to ensure business continuity and meet legal and governance requirements | Lost data can be reloaded from OLTP database as needed in lieu of regular backups |
| Productivity | Increases productivity of end users | Increases productivity of business managers, data analysts, and executives |
| Data View | Lists day-to-day business transactions | Multi-dimensional view of enterprise data |
| User Examples | Customer-facing personnel, clerks, online shoppers | Knowledge workers such as data analysts, business analysts, and executives |

## Data Warehouse

- OLAP Solution
- Used for reporting and data analysis
- Generally consists of raw data, metadata, and summary data
- Generally have many data sources (OS, flat side systems, OLTP database)
- Output can be transformed to data marts

## Big Query

- Serverless data warehouse
  - No servers to manage or database software to install
  - Software as well as infrastructure including
    - **scalability** and **high-availability**
  - Built in features
    - machine learning
    - geospatial analysis
    - business intelligence
  - Maximizes flexibility by separatating the compute engine that analyzes your data from your storage

## BigQuery Parition

- Time-unit column
- `Ingestion time (_PARTITIONTIME)`
- Integer range partitioning
- When using Time unit or ingestion time
  - Daily (default), generally for medium size
  - Hourly, used for a huge amount of data coming in. You may need to consider the number of partitions being created
  - Montly or yearly, for a small amount of data
- Number of partitions limit is 4000

## BigQuery Clustering

- Columns you specify are used to colocated related data
- Order of the column is important
- The order of the specified columns determines the sort order of the data
- Clustering improves
  - Filter queries
  - Aggregate queries
- Table with data size < 1GB, don't show significant improvement with partitioning and clustering
- You can specify up to 4 clusering columns
- Clustering columns must be top-level, non-repeating columns

## Partitioning vs. Clustering

| Clustering | Paritioning |
| - | - |
| Cost benefit unknown | Cost known upfront |
| You need more granularity than partitioning alone allows | You need partition-level management |
| Your queries commonly use filters or aggregation against multiple particular columns | Filter or aggregate on single column |
| The cardinality of the number of values in a column or group of columns is large | |

## When to use clustering over partitioning

- Partitioning results in a small amount of data per partition (less than 1GB)
- Patitioning resluts in a large number of partitions beyond the limits of partitioned tables
- Partitioning results in your mutation operations modifying the majority of partitions in the table frequently (every few minutes)

## Automatic reclustering

- As data is added to a clustered table
  - The newly inserted data can be written to blocks that contain key ranges that overlap with the key ranges in previously written blocks
  - These overlapping keys weaken the sort property of the table
- To maintain the performance characteristics of a clustered table
  - BigQuery performs automatic re-clustering in the background to restore the sort property of the table
  - For partitioned tables, clustering is maintained for data within the scope of each partition.
  - Does not cost the end-user anything

## BigQuery Best Practices

- Cost reduction
  - Avoid SELECT *
  - Price queries before running them
  - Use clustered or partitioned tables
  - Use streaming inserts with caution, can potentially drastically increase costs
  - Materialize query results in stages

- Query Performance
  - Filter on partitioned columns
  - Denormilize data
  - Use nested or repeated columns
  - Use external data sources appropriately
    - Don't use it, in case you want high query performance
  - Reduce data before using a JOIN
  - Do not treat WITH clauses as prepared statements
  - Avoid oversharding tables
  - Avoid JavaScript in user-defined functions
  - Use approximate aggregation functions
  - Use ORDER last, for query operations to maximize performance
  - Optimize join patterns
  - Place tables with largest number of rows first, then table with fewest rows, then the remaining tables by decreasing size
    - The largest table will be distributed evenly
    - The next table will be broadcasted to all nodes

## Internals

- BigQuery stores data in separate data called colossus
  - Generally a cheap storage
  - Stored in a columnar format
  - The storage and compute are separate
- Jupiter Network provides ~1TB/s network speed between compute and storage
- Dremel
  - Query execution engine
  - Divides query into a tree structure
  - Each node can execute an individual subset of the query
  - This is what allows BigQuery to be fast

## BigQuery Model Deployment

- `gcloud auth login`
- `bq --project_id taxi-rides-ny extract -m nytaxi.tip_model gs://taxi_ml_model/tip_model`
- `mkdir /tmp/model`
- `gsutil cp -r gs://taxi_ml_model/tip_model /tmp/model`
- `mkdir -p serving_dir/tip_model/1`
- `cp -r /tmp/model/tip_model/* serving_dir/tip_model/1`
- `docker pull tensorflow/serving`
- `docker run -p 8501:8501 --mount type=bind,source=pwd/serving_dir/tip_model,target= /models/tip_model -e MODEL_NAME=tip_model -t tensorflow/serving &`
- `curl -d '{"instances": [{"passenger_count":1, "trip_distance":12.2, "PULocationID":"193", "DOLocationID":"264", "payment_type":"2","fare_amount":20.4,"tolls_amount":0.0}]}' -X POST http://localhost:8501/v1/models/tip_model:predict`
- `http://localhost:8501/v1/models/tip_model`
