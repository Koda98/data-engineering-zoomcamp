# Week 3 Homework

## Setup

Create an external table using the fhv 2019 data.

```sql
-- Create external table
CREATE OR REPLACE EXTERNAL TABLE `rational-oasis-375505.dezoomcamp.external_fhv_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dtc_data_lake_rational-oasis-375505/data/fhv/fhv_tripdata_2019-*.parquet']
);
```

Create a table in BQ using the fhv 2019 data (do not partition or cluster this table).

```sql
-- Create a table in BQ
CREATE OR REPLACE TABLE rational-oasis-375505.dezoomcamp.fhv_tripdata AS
SELECT * FROM rational-oasis-375505.dezoomcamp.external_fhv_tripdata;
```

## Question 1

What is the count for fhv vehicle records for year 2019?

```sql
SELECT count(*) FROM rational-oasis-375505.dezoomcamp.external_fhv_tripdata;
```

**Answer: 43,244,696**

## Question 2

Write a query to count the distinct number of affiliated_base_number for the entire dataset on both the tables. What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

```sql
-- count the distinct number of affiliated_base_number for the entire dataset on the external table.
SELECT DISTINCT COUNT(Affiliated_base_number) FROM `rational-oasis-375505.dezoomcamp.external_fhv_tripdata`;

-- count the distinct number of affiliated_base_number for the entire dataset on the BQ table.
SELECT DISTINCT COUNT(Affiliated_base_number) FROM `rational-oasis-375505.dezoomcamp.fhv_tripdata`;
```

**Answer: 0 MB for the External Table and 317.94MB for the BQ Table**

## Question 3

How many records have both a blank (null) PUlocationID and DOlocationID in the entire dataset?

```sql
-- records with both a blank (null) PUlocationID and DOlocationID
SELECT
  COUNT(*)
FROM 
  `rational-oasis-375505.dezoomcamp.external_fhv_tripdata`
WHERE PUlocationID IS NULL AND DOlocationID IS NULL;
```

**Answer: 717,748**

## Question 4

What is the best strategy to optimize the table if query always filter by pickup_datetime and order by affiliated_base_number?

**Answer: Partition by pickup_datetime Cluster on affiliated_base_number**

## Quesiton 5

Implement the optimized solution you chose for question 4. Write a query to retrieve the distinct affiliated_base_number between pickup_datetime 2019/03/01 and 2019/03/31 (inclusive).
Use the BQ table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed. What are these values? Choose the answer which most closely matches.

```sql
-- Not partitioned or clustered
SELECT
  DISTINCT COUNT(Affiliated_base_number)
FROM
  `rational-oasis-375505.dezoomcamp.fhv_tripdata` fhv
WHERE DATE(fhv.pickup_datetime) BETWEEN '2019-03-01' AND '2019-03-31';
-- Will process 652.6 MB

-- Partitioned and clustered
SELECT
  DISTINCT COUNT(Affiliated_base_number)
FROM
  `rational-oasis-375505.dezoomcamp.fhv_tripdata_partitioned_clustered` fhv
WHERE DATE(fhv.pickup_datetime) BETWEEN '2019-03-01' AND '2019-03-31';
-- Will process 23.07 MB
```

**Answer: 647.87 MB for non-partitioned table and 23.06 MB for the partitioned table**

## Question 6

Where is the data stored in the External Table you created?

**Answer: GCP Bucket**

## Question 7

It is best practice in Big Query to always cluster your data:

**Answer: False**
