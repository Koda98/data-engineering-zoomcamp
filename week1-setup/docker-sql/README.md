# Docker + Postgres

## [Intro to Docker](https://www.youtube.com/watch?v=EYNwNlOrpr0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)

* ### Why do we need Docker?
    * Local experiments
    * Reproducibility
    * Running pipelines in the cloud
    * Integration tests
    * Spark
    * Serverless

* ### Simple data pipeline

  #### Basic Dockerfile
    ```dockerfile
    FROM python:3.9

    RUN pip install pandas

    WORKDIR /app
    COPY pipeline.py pipeline.py

    ENTRYPOINT [ "python", "pipeline.py" ]
    ```

  #### Basic pipeline
    ```python
    import sys
    import pandas as pd

    day = sys.argv[1]
    print(day)

    print(f'Job finished for day {day}')
    ```

  The following command will build the image

    ```
    $ docker build -t test:pandas .
    ```

  Then we can run it

    ```
    $ docker run -it test:pandas 1-20-23
    1-20-23
    Job finished for day 1-20-23
    ```

## [Ingesting Data to Postgres](https://www.youtube.com/watch?v=2JM-ziJt0WI&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)

* ### Running Postgres locally with Docker

  #### Using `pgcli` for connecting to the database
  Run postgres with docker:
    ```
    docker run -it \
      -e POSTGRES_USER="root" \
      -e POSTGRES_PASSWORD="root" \
      -e POSTGRES_DB="ny_taxi" \
      -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
      -p 5432:5432 \
      postgres:13
    ```
  Connect to postgres with pgcli:
    ```
    pgcli -h localhost -p 5432 -u root -d ny_taxi
    ```
* ### Ingesting the data into the database
    ```python
    import pandas as pd
    from sqlalchemy import create_engine
    from time import time

    df = pd.read_csv('yellow_tripdata_2021-01.csv', nrows=100)
    engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

    df_iter = pd.read_csv('yellow_tripdata_2021-01.csv', iterator=True, chunksize=100_000)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')
    df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')

    for df in df_iter:
        t_start = time()

        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')

        t_end = time()

        print(f'inserted chunk..., took {(t_end - t_start):.3f} seconds')
    ```

## [Connecting pgAdmin and Postgres](https://www.youtube.com/watch?v=hCAIVe9N0ow&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)
* ### The pgAdmin tool
    ```
    docker run -it \
      -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
      -e PGADMIN_DEFAULT_PASSWORD="root" \
      -p 8080:80 \
      dpage/pgadmin4
    ```
* ### Docker networks
  Create a network
    ``` 
    $ docker create network pg-network
    ```
  Run postgres
    ``` 
    docker run -it \
      -e POSTGRES_USER="root" \
      -e POSTGRES_PASSWORD="root" \
      -e POSTGRES_DB="ny_taxi" \
      -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
      -p 5432:5432 \
      --network=pg-network \
      --name pg-database \
      postgres:13
    ```
  Run pgadmin
    ``` 
    docker run -it \
      -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
      -e PGADMIN_DEFAULT_PASSWORD="root" \
      -p 8080:80 \
      --network=pg-network \
      --name pgadmin-2 \
      dpage/pgadmin4
    ```

## [Putting the ingestion script into Docker](https://www.youtube.com/watch?v=B1WwATwf-vY&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)
* ### Converting the Jupyter notebook to a Python script
    ```
    jupyter nbconvert --to=script upload-data.ipynb
    ```
* ### Parametrizing the script with argparse
    ```python
    import argparse
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table where we will write results to')
    parser.add_argument('--url', help='url of the csv file')

    args = parser.parse_args()
    ```
* Dockerizing the ingestion script
    ``` 
    URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

    docker run -it \
      --network=pg-network \
      taxi_ingest:v001 \
        --user=root \
        --password=root \
        --host=pg-database \
        --port=5432 \
        --db=ny_taxi \
        --table_name=yellow_taxi_trips \
        --url=${URL}
    ```

## [Running Postgres and pgAdmin with Docker-Compose](https://www.youtube.com/watch?v=hKI6PkPhpa0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)
* ### Why do we need Docker-compose
    * Docker compose is a utility that allows us to put configurations for multiple containers in one file
* ### Docker-compose YAML file
    ```yaml
    services:
      pgdatabase:
        image: postgres:13
        environment:
          - POSTGRES_USER=root
          - POSTGRES_PASSWORD=root
          - POSTGRES_DB=ny_taxi
        volumes:
          - "./ny_taxi_postgres_data:/var/lib/postgresql/data:rw"
        ports:
          - "5432:5432"
      pgadmin:
        image: dpage/pgadmin4
        environment:
          - PGADMIN_DEFAULT_EMAIL=admin@admin.com
          - PGADMIN_DEFAULT_PASSWORD=root
        volumes:
          - "pgadmin_conn_data:/var/lib/pgadmin:rw"
        ports:
          - "8080:80"

    volumes:
      pgadmin_conn_data:
    ```
* ### Running multiple containers with `docker-compose up`
    * Run it: `docker-compose up`
    * Run in detached mode: `docker-compose up -d`
    * Shut it down: `docker-compose down`

## [SQL refresher](https://www.youtube.com/watch?v=QEcps_iskgg&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)

* ### Adding the Zones table
    ```python
    os.system(f"wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv")
    df_zones = pd.read_csv('taxi+_zone_lookup.csv')
    df_zones.to_sql(name='zones', con=engine, if_exists='replace')
    ```

* ### Inner joins
    ```sql
    SELECT 
        tpep_pickup_datetime,
        tpep_dropoff_datetime,
        total_amount,
        CONCAT(zpu."Borough", ' / ', zpu."Zone") AS "pickup_loc",
        CONCAT(zdo."Borough", ' / ', zdo."Zone") AS "dropoff_loc"
    FROM 
        yellow_taxi_trips t
        zones zpu,
        zones zdo
    WHERE
        t."PULocationID" = zpu."LocationID" AND
        t."DOLocationID" = zdo."LocationID"
    ```
  or
    ```sql
    SELECT 
        tpep_pickup_datetime,
        tpep_dropoff_datetime,
        total_amount,
        CONCAT(zpu."Borough", ' / ', zpu."Zone") AS "pickup_loc",
        CONCAT(zdo."Borough", ' / ', zdo."Zone") AS "dropoff_loc"
    FROM 
        yellow_taxi_trips t JOIN zones zpu
            ON t."PULocationID" = zpu."LocationID"
        JOIN zones zdo
            ON t."DOLocationID" = zdo."LocationID"
    WHERE
        t."PULocationID" = zpu."LocationID" AND
        t."DOLocationID" = zdo."LocationID"
    LIMIT 100
    ```

* ### Basic data quality checks
    * Checking for records with location ID not in trips table
      ```sql
      SELECT 
          tpep_pickup_datetime,
          tpep_dropoff_datetime,
          total_amount,
          "PULocationID",
          "DOLocationID"
      FROM 
          yellow_taxi_trips t
      WHERE
          "PULocationID" is NULL
      LIMIT 100
      ```
    * Checking for location IDs in zones table not in trips table
      ```sql
      SELECT 
          tpep_pickup_datetime,
          tpep_dropoff_datetime,
          total_amount,
          "PULocationID",
          "DOLocationID"
      FROM 
          yellow_taxi_trips t
      WHERE
          "DOLocationID" NOT IN (SELECT "LocationID" FROM zones)
      LIMIT 100
      ```

* ### Left, Right and Outer joins
  ![](sql-table-joins.png "SQL Joins")

* ### Group by
    * Calculate the number of trips per day
    ```sql
    SELECT 
        CAST(tpep_dropoff_datetime AS DATE) as "day",
        COUNT(1) as "count",
    FROM 
        yellow_taxi_trips t
    GROUP BY
        CAST(tpep_dropoff_datetime AS DATE)
    ORDER BY "count" DESC;
    ```
    * Other aggregations
    ```sql
    SELECT 
        CAST(tpep_dropoff_datetime AS DATE) as "day",
        COUNT(1) as "count",
        MAX(total_amount),
        MAX(passenger_count)
    FROM 
        yellow_taxi_trips t
    GROUP BY
        CAST(tpep_dropoff_datetime AS DATE)
    ORDER BY "count" DESC;
    ```
    * Group by multiple field
    ```sql
    SELECT 
        CAST(tpep_dropoff_datetime AS DATE) as "day",
        "DOLocationID",
        COUNT(1) as "count",
        MAX(total_amount),
        MAX(passenger_count)
    FROM 
        yellow_taxi_trips t
    GROUP BY
        1, 2
    ORDER BY 
        "day" ASC,
        "DOLocationID" ASC;
    ```
