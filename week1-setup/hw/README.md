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
Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash. Now check the python modules that are installed ( use pip list). How many python packages/modules are installed?
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
WHERE (lpep_pickup_datetime BETWEEN '2019-01-15 00:00:00' AND '2019-01-15 23:59:59') AND
	(lpep_dropoff_datetime BETWEEN '2019-01-15 00:00:00' AND '2019-01-15 23:59:59')
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
SELECT
	t."tip_amount" tip,
	(
		SELECT z2."Zone"
		FROM zones as z2
		WHERE t."DOLocationID" = z2."LocationID"
	)
FROM 
	green_taxi as t,
	zones as z
WHERE 
	t."PULocationID" = z."LocationID" AND
	z."Zone" = 'Astoria' 
ORDER BY tip DESC
```
**Answer: Long Island City/Queens Plaza**
