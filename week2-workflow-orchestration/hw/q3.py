from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect.deployments import Deployment
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials


@task(retries=3)
def extract_from_gcs(color: str, year: int, month: int) -> pd.DataFrame:
    """Download trip data from GCS"""
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.get_directory(from_path=gcs_path, local_path="../data")
    path = Path(f"{gcs_path}")
    return pd.read_parquet(path)


@task()
def write_bq(df: pd.DataFrame) -> None:
    """Write DataFrame to BigQuery"""
    gcp_credentials_block = GcpCredentials.load("zoom-gcp-creds")

    df.to_gbq(
        destination_table="dezoomcamp.hw2-rides",
        project_id="rational-oasis-375505",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append"
    )
    return


@task(retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read data from web into pandas DataFrame"""
    df = pd.read_csv(dataset_url)
    return df


@task(log_prints=True)
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Fix dtype issues"""
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df


@task()
def write_local(df: pd.DataFrame, color: str, dataset_file: str) -> Path:
    """Write DataFrame out locally as a Parquet file"""
    path = Path(f"data/{color}/{dataset_file}.parquet")
    df.to_parquet(path, compression="gzip")
    return path


@task()
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.upload_from_path(from_path=f"{path}", to_path=path, timeout=120)
    return


@flow()
def etl_web_to_gcs(year: int, month: int, color: str) -> None:
    """ETL flow to load data from web to GCS"""
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    df_clean = clean(df)
    path = write_local(df_clean, color, dataset_file)
    write_gcs(path)
    return


@flow()
def etl_gcs_to_bq(color: str, month: int, year: int):
    """ETL flow to load data into Big Query"""
    df = extract_from_gcs(color, year, month)
    write_bq(df)
    return len(df)


@flow(name="Main flow", log_prints=True)
def main_flow(color: str="yellow", months: list[int]=[2, 3], year: int=2019):
    """Main ETL flow"""
    total_rows = 0
    for month in months:
        etl_web_to_gcs(color=color, month=month, year=year)
        total_rows += etl_gcs_to_bq(color=color, month=month, year=year)
    print("Total rows processed:", total_rows)


if __name__ == "__main__":
    deployment = Deployment.build_from_flow(
        flow=main_flow,
        name="etl-flow",
        parameters={
            "color": "yellow",
            "months": [2, 3],
            "year": 2019
        }
    )
    deployment.apply()
