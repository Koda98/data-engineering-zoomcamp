#!/usr/bin/env python

import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import os


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    trips_table_name = params.trips_table_name
    zones_table_name = params.zones_table_name
    trips_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz"
    zones_url = "https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv"
    trips_csv_name = "green_tripdata.csv.gz"
    zones_csv_name = "zones.csv"

    # download csv files
    os.system(f"wget {trips_url} -O {trips_csv_name}")
    os.system(f"wget {zones_url} -O {zones_csv_name}")

    # creat engine
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # load trips csv to database
    print("Ingesting trip data to postgres database...")
    t_start = time()
    df_trips = pd.read_csv(trips_csv_name, parse_dates=["lpep_pickup_datetime", "lpep_dropoff_datetime"])
    df_trips.drop('ehail_fee', inplace=True, axis=1)  # Drop column with all null values
    df_trips.head(n=0).to_sql(name=trips_table_name, con=engine, if_exists="replace")
    df_trips.to_sql(name=trips_table_name, con=engine, if_exists="append", chunksize=100_000)
    t_end = time()
    print(f"Finished trip ingesting data, took {t_end-t_start} seconds")

    # load zones csv to database
    print("Ingesting zones data to postgres database...")
    t_start = time()
    df_zones = pd.read_csv(zones_csv_name)
    df_zones.to_sql(name=zones_table_name, con=engine, if_exists="replace")
    t_end = time()
    print(f"Finished zones ingesting data, took {t_end-t_start} seconds")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', help='username for postgres', default="root")
    parser.add_argument('--password', help='password for postgres', default="root")
    parser.add_argument('--host', help='host for postgres', default="localhost")
    parser.add_argument('--port', help='port for postgres', default="5432")
    parser.add_argument('--db', help='database name for postgres', default="ny_taxi")
    parser.add_argument('--trips_table_name', help='name of the trips table where we will write results to',
                        default="green_taxi")
    parser.add_argument('--zones_table_name', help='name of the zones table where we will write results to',
                        default="zones")

    args = parser.parse_args()
    main(args)
