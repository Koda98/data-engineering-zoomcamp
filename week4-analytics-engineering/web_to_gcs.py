from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect.deployments import Deployment
from prefect_gcp.cloud_storage import GcsBucket
import os


@task(retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read data from web into pandas DataFrame"""
    df = pd.read_csv(dataset_url, compression='gzip', engine="pyarrow")
    return df


@task(log_prints=True)
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Fix dtype issues"""
    df = df.convert_dtypes()
    return df


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
def web_to_gcs(year: int, month: int, service: str) -> None:
    """ETL flow to load data from web to GCS"""
    dataset_file = f"{service}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{service}/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    df_clean = clean(df)
    path = write_local(df_clean, dataset_file, service)
    write_gcs(path)
    remove_downloaded_file(path)
    return


@flow(name="main-flow", log_prints=True)
def main_flow(year: int=2019, start_month: int=1, end_month: int=12, service: str="fhv") -> None:
    """Main ETL flow"""
    for month in range(start_month, end_month + 1):
        web_to_gcs(month=month, year=year, service=service)


if __name__ == "__main__":
    deployment = Deployment.build_from_flow(
        flow=main_flow,
        name="ingest-taxi-data",
        parameters={
            "year": 2019,
            "start_month": 1,
            "end_month": 12,
            "service": "green"
        }
    )
    deployment.apply()
