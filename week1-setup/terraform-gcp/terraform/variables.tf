# locals are like constants
locals {
  data_lake_bucket = "dtc_data_lake"
}

# variables are generally passed at runtime
# variables that have a default are optional runtime arguments, ones w/o are mandatory
variable "project" {
  description = "Your GCP Project ID"
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location"
  default = "us-west2"
  type = string
}

variable "bucket_name" {
  description = "The name of the Google Cloud Storage bucket. Must be globally unique"
  default = ""
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info"
  default = "STANDARD"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type = string
  default = "trips_data_all"
}

variable "TABLE_NAME" {
  description = "BigQuery Table"
  type = string
  default = "ny_trips"
}
