# Workflow Orchestration

## Data Lake (GCS)

* What is a Data Lake
  * A central respository that holds big data from many sources
  * Data can be structured, semi-structured, or unstructured
  * Its purpose is to ingest data as quick as possible and make it available to others
  * Used for machine learning/ analytics
  * Needs to be secure and scalable

* Data Lake vs. Data Warehouse
  * | Data Lake | Data Warehouse |
    | --------- | -------------- |
    | Unstructured Data | Structured data |
    | Users are data scientists/analysts | Users are business analysts |
    | Stores huge amounts of data (petabytes) | Data size is small|
    | Use cases include stream processing, machine learning, real time analytics | Use cases include batch processing or BI reporting|

* Why do we need data lakes?
  * Used to store and access data quickly
  * You can't always define the structure of the data
  * Increase in data scientists
  * Cheap storage of Big Data

* | ETL | ELT |
  | --- | --- |
  | Extract Transform Load | Extract Load Transform |
  | used for small amounts of data (data warehouse) | large amounts of data (data lake) |
  | schema on write. define the schema and relationships, then write the data | schema on read. write the data first, determine the schema on read |

* Cons of Data lake
  * Converts into a Data Swamp
  * No versioning
  * Incompatible schemas for same data without versioning
  * No metadata
  * Joins not possible

* Alternatives to components (S3/HDFS, Redshift, Snowflake etc.)
* [Video](https://www.youtube.com/watch?v=W3Zm6rjOq70&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)
* [Slides](https://docs.google.com/presentation/d/1RkH-YhBz2apIjYZAxUz2Uks4Pt51-fVWVN9CcH9ckyY/edit?usp=sharing)

### 1. Introduction to Workflow orchestration

* What is orchestration?
  * Governing your data flow in a way that respects orchestration rules and business logic
    * Data flow: binds an otherwise disparate set of applications together
  * A workflow orchestration tool will allow you to turn any code into a workflow that can be scheduled, run, and observed
  * A good workflow orchestration system should be scalable and available
* Core features of a workflow orchestration tool
  * Remote execution
  * Scheduling
  * Retries
  * Caching
  * Integration with external systems (APIs, databases)
  * Ad-hoc runs
  * Parameterization
  * Alerts when something fails
* Different types of workflow orchestration tools that currently exist
  * Airflow
  * Prefect
  * Flyte
  * dagster
  * astronomer
  * etc

:movie_camera: [Video](https://www.youtube.com/watch?v=8oLs6pzHp68&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=16)

### 2. Introduction to Prefect concepts

* What is Prefect?
* Installing Prefect
* Prefect flow
* Creating an ETL
* Prefect task
* Blocks and collections
* Orion UI

:movie_camera: [Video](https://www.youtube.com/watch?v=jAwRCyGLKOY&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=17)

### 3. ETL with GCP & Prefect

* Flow 1: Putting data to Google Cloud Storage

:movie_camera: [Video](https://www.youtube.com/watch?v=W-rMz_2GwqQ&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=18)

### 4. From Google Cloud Storage to Big Query

* Flow 2: From GCS to BigQuery

:movie_camera: [Video](https://www.youtube.com/watch?v=Cx5jt-V5sgE&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=19)

### 5. Parametrizing Flow & Deployments

* Parametrizing the script from your flow
* Parameter validation with Pydantic
* Creating a deployment locally
* Setting up Prefect Agent
* Running the flow
* Notifications

:movie_camera: [Video](https://www.youtube.com/watch?v=QrDxPjX10iw&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=20)

### 6. Schedules & Docker Storage with Infrastructure

* Scheduling a deployment
* Flow code storage
* Running tasks in Docker

:movie_camera: [Video](https://www.youtube.com/watch?v=psNSzqTsi-s&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=21)

### 7. Prefect Cloud and Additional Resources

* Using Prefect Cloud instead of local Prefect
* Workspaces
* Running flows on GCP

:movie_camera: [Video](https://www.youtube.com/watch?v=gGC23ZK7lr8&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=22)

* [Prefect docs](https://docs.prefect.io/)
* [Pefect Discourse](https://discourse.prefect.io/)
* [Prefect Cloud](https://app.prefect.cloud/)
* [Prefect Slack](https://prefect-community.slack.com)
