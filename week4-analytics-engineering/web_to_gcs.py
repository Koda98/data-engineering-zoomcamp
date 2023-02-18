from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
import os
import yaml


@task()
def get_schema(filename: str) -> dict:
    """Read and return a dictionary of schemas from yaml file"""
    with open(filename) as f:
        schemas = yaml.safe_load(f)
    return schemas


@task(retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read data from web into pandas DataFrame"""
    return pd.read_csv(dataset_url, compression='gzip', engine="pyarrow")


@task(log_prints=True)
def fix_dtypes(df: pd.DataFrame, schema: dict) -> pd.DataFrame:
    """Fix dtype issues"""
    return df.astype(schema)


@task(log_prints=True)
def write_local(df: pd.DataFrame, dataset_file: str, service: str) -> Path:
    """Write DataFrame out locally as a Parquet file"""
    Path(f"data/{service}").mkdir(parents=True, exist_ok=True)
    path = Path(f"data/{service}/{dataset_file}.parquet")
    df.to_parquet(path, compression="gzip")
    print(f"Parquet file written to {path}")
    return path


@task()
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.upload_from_path(from_path=f"{path}", to_path=path, timeout=120)
    return


@task(log_prints=True)
def remove_downloaded_file(path: Path) -> None:
    """Delete downloaded local parquet files"""
    if os.path.isfile(path):
        print(f"Removing {path}...")
        os.remove(path)


@flow()
def web_to_gcs(year: int, month: int, service: str, schema_: dict) -> None:
    """ETL flow to load data from web to GCS"""
    dataset_file = f"{service}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{service}/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    df_clean = fix_dtypes(df, schema_)
    path = write_local(df_clean, dataset_file, service)
    write_gcs(path)
    remove_downloaded_file(path)
    return


@flow(name="main-flow", log_prints=True)
def ingest(year: int=2019, service: str="fhv") -> None:
    """Main ETL flow"""
    schema = get_schema("schemas.yaml").get(service)
    for month in range(1, 13):
        web_to_gcs(
            month=month,
            year=year,
            service=service,
            schema_=schema
        )


if __name__ == "__main__":
    ingest(year=2019, service="green")
    ingest(year=2020, service="green")
    ingest(year=2019, service="yellow")
    ingest(year=2020, service="yellow")
    ingest(year=2019, service="fhv")
