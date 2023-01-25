# Week 1 Homework

## Question 1

Run the command to get information on Docker

`docker --help`

Now run the command to get help on the "docker build" command

Which tag has the following text? - Write the image ID to the file

``` 
$ docker build --help | grep "Write the image ID to the file"
      --iidfile string          Write the image ID to the file
```

**Answer: `--iidfile string`**

## Question 2

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash. Now check the python modules
that are installed ( use pip list). How many python packages/modules are installed?

```
$ docker run -it --entrypoint=bash python:3.9
root@cd3f20f31999:/# pip list
Package    Version
---------- -------
pip        22.0.4
setuptools 58.1.0
wheel      0.38.4
```

**Answer: 3**

## Question 3

How many taxi trips were totally made on January 15th?

```sql
SELECT COUNT(1)
FROM green_taxi t
WHERE (lpep_pickup_datetime BETWEEN '2019-01-15 00:00:00' AND '2019-01-15 23:59:59')
  AND (lpep_dropoff_datetime BETWEEN '2019-01-15 00:00:00' AND '2019-01-15 23:59:59')
```

**Answer: 20530**

# Question 4

Which was the day with the largest trip distance? Use the pick up time for your calculations.

```sql
SELECT DATE_TRUNC('day', lpep_pickup_datetime) pickup, MAX(trip_distance) dist
FROM green_taxi as t
GROUP BY pickup
ORDER BY dist DESC
```

**Answer: 2019-01-15**

# Question 5

In 2019-01-01 how many trips had 2 and 3 passengers?

```sql
SELECT passenger_count, COUNT(*)
FROM green_taxi as t
WHERE DATE_TRUNC('day', lpep_pickup_datetime) = '2019-01-01'
GROUP BY passenger_count
```

**Answer: 2: 1282 ; 3: 254**

# Question 6

For the passengers picked up in the Astoria Zone which was the drop off zone that had the largest tip? We want the name
of the zone, not the id.

```sql
SELECT t."tip_amount" tip,
       (SELECT z2."Zone"
        FROM zones as z2
        WHERE t."DOLocationID" = z2."LocationID")
FROM green_taxi as t,
    zones as z
WHERE t."PULocationID" = z."LocationID"
    AND z."Zone" = 'Astoria'
ORDER BY tip DESC
```

**Answer: Long Island City/Queens Plaza**

# Part B
Result from `$ terraform apply`.

```
var.project
  Your GCP Project ID

  Enter a value: rational-oasis-375505


Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.dataset will be created
  + resource "google_bigquery_dataset" "dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "trips_data_all"
      + delete_contents_on_destroy = false
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + labels                     = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "europe-west6"
      + project                    = "rational-oasis-375505"
      + self_link                  = (known after apply)

      + access {
          + domain         = (known after apply)
          + group_by_email = (known after apply)
          + role           = (known after apply)
          + special_group  = (known after apply)
          + user_by_email  = (known after apply)

          + dataset {
              + target_types = (known after apply)

              + dataset {
                  + dataset_id = (known after apply)
                  + project_id = (known after apply)
                }
            }

          + routine {
              + dataset_id = (known after apply)
              + project_id = (known after apply)
              + routine_id = (known after apply)
            }

          + view {
              + dataset_id = (known after apply)
              + project_id = (known after apply)
              + table_id   = (known after apply)
            }
        }
    }

  # google_storage_bucket.data-lake-bucket will be created
  + resource "google_storage_bucket" "data-lake-bucket" {
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "EUROPE-WEST6"
      + name                        = "dtc_data_lake_rational-oasis-375505"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + uniform_bucket_level_access = true
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type = "Delete"
            }

          + condition {
              + age                   = 30
              + matches_prefix        = []
              + matches_storage_class = []
              + matches_suffix        = []
              + with_state            = (known after apply)
            }
        }

      + versioning {
          + enabled = true
        }

      + website {
          + main_page_suffix = (known after apply)
          + not_found_page   = (known after apply)
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

google_bigquery_dataset.dataset: Creating...
google_storage_bucket.data-lake-bucket: Creating...
╷
│ Error: googleapi: Error 409: The requested bucket name is not available. The bucket namespace is shared by all users of the system. Please select a different name and try again., conflict
│ 
│   with google_storage_bucket.data-lake-bucket,
│   on main.tf line 19, in resource "google_storage_bucket" "data-lake-bucket":
│   19: resource "google_storage_bucket" "data-lake-bucket" {
│ 
╵
╷
│ Error: Error creating Dataset: googleapi: Error 409: Already Exists: Dataset rational-oasis-375505:trips_data_all, duplicate
│ 
│   with google_bigquery_dataset.dataset,
│   on main.tf line 45, in resource "google_bigquery_dataset" "dataset":
│   45: resource "google_bigquery_dataset" "dataset" {
│ 
╵
```