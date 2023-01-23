terraform {
  required_version = ">= 1.0"
  backend "local" {}  # can change to "gcs" for google or "s3" for aws
  # optional since we are defining providers below
  # this is where your terraform registry is picking publicly available providers from
  # it allows you to create/implement resources based on those predefined configurations
  # it's kind of like importing a python library and then implementing those predefined
  # functions in your script.
  required_providers {
    google = {
      source = "hashicorp/google"
    }
  }
}

# terraform relies on plugins called providers to interact with cloud & SAAS providers
# adds a set of predefined resources types and data sources that terraform can manage
provider "google" {
  project = var.project
  region = var.region
  // credentials = file(var.credentials)  # Use this if you do not set an env-var
}

# Data Lake Bucket
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucketc
resource "google_storage_bucket" "data-lake-bucket" {
  name = "${local.data_lake_bucket}_${var.project}"
  location = var.region

  # Optional, but recommended setting
  storage_class = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled = false
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  # days
    }
  }

  force_destroy = true
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.BQ_DATASET
  project = var.project
  location = var.region
}
