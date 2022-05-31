#!/usr/bin/env python
# coding: utf-8

# # Part 1: BigQuery and SQL

# ## Python Solutions
# 

# To test my sql queries I wrote python scripts to interface directly with the Big Query API.  This permitted me to run a test driven development environment to automate most of the work.  

# ### Import Statements

# In[1]:


from google.cloud import bigquery
from pprint import pprint
import os


# ### Utility Big Query Function

# In[2]:


def query_big_query(query_string):
    client = bigquery.Client()
    query_job = client.query(query_string)

    results = query_job.result()  # Waits for job to complete.
    return results


# In[3]:


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/jnapolitano/Projects/pmc-submission/creds.json"


# ## Question 1
# 1) Use the publicly available BigQuery dataset named `nyc-tlc.green.trips_2015`, provide SQL queries to answer the following questions:
# * What is the total amount and passenger counts for the months of February, March and April?
# * What has been the average hourly passenger count throughout the year?  
# * What has been the change/delta in total amount billed over days? What we would like see is how much (positive or negative)
# * What hour of the day has seen the longest rides in April?

# ## Question 1.1 
# * What is the total amount and passenger counts for the months of February, March and April?

# ### Discussion of the Problem
# 
# I initally approached this problem somewhat naively.  I did not consider the possibliity of taxi rides overlapping per hour.  
# 
# For example the code below simply considered the pickup_datetime in the analysis.

# In[4]:


def naive_query_passengers_by_month():
    query_string = """
        SELECT date_trunc(dropoff_datetime,MONTH) as Month,
        sum(passenger_count) as Sum_PASS,
        sum(total_amount) as TOTAL_AMOUNT_SUM
        FROM `nyc-tlc.green.trips_2015` 
        where dropoff_datetime BETWEEN '2015-02-01' AND '2015-04-30'
        GROUP BY Month;
        """

    result = query_big_query(query_string = query_string)

    return result.to_dataframe()
naive_df = naive_query_passengers_by_month()    


# In[22]:


naive_df 


# I then attempted to create intervals to unpiviot the table with the following code.  

# In[108]:


def total_passenger_total_ammount():

    query_string = """
        #standardSQL
        select timestamp_trunc(int, month) month, 
        count(pickup_datetime) rides,
        sum(passenger_count) as passenger_count,
        avg(passenger_count) as avg_passenger_count,
        sum(total_amount) as total_amount,
        avg(total_amount) as avg_total_amount
        from `nyc-tlc.green.trips_2015`, 
        unnest(generate_timestamp_array(
        pickup_datetime, 
        dropoff_datetime, 
        interval 1 hour)) int
        where pickup_datetime BETWEEN '2015-02-01' AND '2015-04-30'
        group by month
        order by month
         """
    result = query_big_query(query_string)
    return result.to_dataframe()

df_first_try = total_passenger_total_ammount()


# In[109]:


df_first_try


# ### The Problem with this Approach.
# 
# Firstly the data extends to 2021 for some reason.  There are also negative values within the return set.  I spent a full day tinkering the query to clean the data.  

# ### Cleaning the data

# In[135]:


def clean_up_data():

  query_string = """
      SELECT 
      t.*,
      FROM
      (
      SELECT *,
      TIMESTAMP_DIFF(dropoff_datetime,pickup_datetime,SECOND) as time_duration_in_secs,
      TIMESTAMP_DIFF(dropoff_datetime,pickup_datetime,MINUTE) as time_duration_in_mins,
      ROUND(trip_distance/TIMESTAMP_DIFF(dropoff_datetime,pickup_datetime,SECOND),2)*3600 as driving_speed_miles_per_hour,
      (CASE WHEN total_amount=0 THEN 0
      ELSE ROUND(tip_amount*100/total_amount,2) END) as tip_rate,
      EXTRACT(YEAR from pickup_datetime) as pickup_year,
      EXTRACT(MONTH from pickup_datetime) as pickup_month,
      CONCAT(CAST(EXTRACT(YEAR from pickup_datetime) as STRING),"-",CAST(EXTRACT(MONTH from pickup_datetime) AS STRING)) as pickup_yearmonth,
      EXTRACT(DATE from pickup_datetime) as pickup_date,
      FORMAT_DATE('%A',DATE(pickup_datetime)) as pickup_weekday_name,
      EXTRACT(HOUR from pickup_datetime) as pickup_hour,
      EXTRACT(YEAR from dropoff_datetime) as dropoff_year,
      EXTRACT(MONTH from dropoff_datetime) as dropoff_month,
      CONCAT(CAST(EXTRACT(YEAR from dropoff_datetime) as STRING),"-",CAST(EXTRACT(MONTH from dropoff_datetime) AS STRING)) as dropoff_yearmonth,
      EXTRACT(DATE from dropoff_datetime) as dropoff_date,
      FORMAT_DATE('%A',DATE(dropoff_datetime)) as dropoff_weekday_name,
      EXTRACT(HOUR from dropoff_datetime) as dropoff_hour
      FROM `nyc-tlc.green.trips_2015`
      ) t
      WHERE 
      pickup_datetime BETWEEN '2015-01-01' AND '2016-12-31' 
      AND dropoff_datetime BETWEEN '2015-01-01' AND '2016-12-31'
      AND TIMESTAMP_DIFF(dropoff_datetime,pickup_datetime,SECOND) > 0
      AND passenger_count > 0
      AND trip_distance >= 0 
      AND tip_amount >= 0 
      AND tolls_amount >= 0 
      AND mta_tax >= 0 
      AND fare_amount >= 0
      AND total_amount >= 0
      order by pickup_date DESC
      limit 100000
      """


  result = query_big_query(query_string)
      
  return result.to_dataframe()

clean_df = clean_up_data()


# In[198]:


clean_df.columns


# ### Discussion of the Clean Data
# 
# As we can the see the cleaned data is far more usable.  Typically, I would have performed analysis across a spark cluster or pandas if the resource requirements were not too great. 
# 
# Another approach would have been to export the table to another bigtable instance.   I may experiment with this approach if I have time. 
# 
# 
# For the sake of the problem given to me, I include the table above as a tmp table within the following working queries.  

# In[156]:


def total_passenger_total_ammount():

    query_string = """
        #standardSQL
        select timestamp_trunc(int, month) month, 
        count(pickup_datetime) rides,
        sum(passenger_count) as passenger_count,
        avg(passenger_count) as avg_passenger_count,
        sum(total_amount) as total_amount,
        avg(total_amount) as avg_total_amount
        from `nyc-tlc.green.trips_2015`, 
        unnest(generate_timestamp_array(
        pickup_datetime, 
        dropoff_datetime, 
        interval 1 hour)) int
        where pickup_datetime BETWEEN '2015-02-01' AND '2015-04-30'
        group by month
        order by month
         """

    query_string_2 = """
        with clean as (      
            SELECT 
            t.*,
            FROM
            (
            SELECT *,
            TIMESTAMP_DIFF(dropoff_datetime,pickup_datetime,SECOND) as time_duration_in_secs,
            TIMESTAMP_DIFF(dropoff_datetime,pickup_datetime,MINUTE) as time_duration_in_mins,
            ROUND(trip_distance/TIMESTAMP_DIFF(dropoff_datetime,pickup_datetime,SECOND),2)*3600 as driving_speed_miles_per_hour,
            (CASE WHEN total_amount=0 THEN 0
            ELSE ROUND(tip_amount*100/total_amount,2) END) as tip_rate,
            EXTRACT(YEAR from pickup_datetime) as pickup_year,
            EXTRACT(MONTH from pickup_datetime) as pickup_month,
            CONCAT(CAST(EXTRACT(YEAR from pickup_datetime) as STRING),"-",CAST(EXTRACT(MONTH from pickup_datetime) AS STRING)) as pickup_yearmonth,
            EXTRACT(DATE from pickup_datetime) as pickup_date,
            FORMAT_DATE('%A',DATE(pickup_datetime)) as pickup_weekday_name,
            EXTRACT(HOUR from pickup_datetime) as pickup_hour,
            EXTRACT(YEAR from dropoff_datetime) as dropoff_year,
            EXTRACT(MONTH from dropoff_datetime) as dropoff_month,
            CONCAT(CAST(EXTRACT(YEAR from dropoff_datetime) as STRING),"-",CAST(EXTRACT(MONTH from dropoff_datetime) AS STRING)) as dropoff_yearmonth,
            EXTRACT(DATE from dropoff_datetime) as dropoff_date,
            FORMAT_DATE('%A',DATE(dropoff_datetime)) as dropoff_weekday_name,
            EXTRACT(HOUR from dropoff_datetime) as dropoff_hour
            FROM `nyc-tlc.green.trips_2015`
            /* filter by latitude & longitude that are within the correct range */
            WHERE 
                ((pickup_latitude BETWEEN -90 AND 90) AND
                (pickup_longitude BETWEEN -180 AND 180)) 
            AND
                ((dropoff_latitude BETWEEN -90 AND 90) AND
                (dropoff_longitude BETWEEN -180 AND 180))
            ) t
            /* find the boroughs and zone names for dropoff locations */
            INNER JOIN `bigquery-public-data.new_york_taxi_trips.taxi_zone_geom` tz_do ON 
            (ST_DWithin(tz_do.zone_geom,ST_GeogPoint(dropoff_longitude, dropoff_latitude), 0))
            /* find the boroughs and zone names for pickup locations */
            INNER JOIN `bigquery-public-data.new_york_taxi_trips.taxi_zone_geom` tz_pu ON 
            (ST_DWithin(tz_pu.zone_geom,ST_GeogPoint(pickup_longitude, pickup_latitude), 0))
            WHERE 
            pickup_datetime BETWEEN '2015-01-01' AND '2016-12-31' 
            AND dropoff_datetime BETWEEN '2015-01-01' AND '2016-12-31'
            AND TIMESTAMP_DIFF(dropoff_datetime,pickup_datetime,SECOND) > 0
            AND passenger_count > 0
            AND trip_distance >= 0 
            AND tip_amount >= 0 
            AND tolls_amount >= 0 
            AND mta_tax >= 0 
            AND fare_amount >= 0
            AND total_amount >= 0
            )

            #standardSQL
            select date_trunc(int, MONTH) Month_Datetime,
            count(pickup_datetime) rides,
            sum(passenger_count) as passenger_count,
            avg(passenger_count) as avg_passenger_count,
            sum(total_amount) as total_amount,
            avg(total_amount) as avg_total_amount
            from clean,
            unnest(generate_timestamp_array(
            pickup_datetime, 
            dropoff_datetime, 
            interval 1 hour)) as int
            where pickup_datetime BETWEEN '2015-02-01' AND '2015-04-30'
            group by Month_Datetime
            order by Month_Datetime
            
        
         """

## In theory the interval could be as small as 1 minute.  Doing so could in theory be more accurate, however, it may also overcount the total ammount billed and the passenger count in the group by.

    result = query_big_query(query_string=query_string_2)
    df = result.to_dataframe()
    return df

df = total_passenger_total_ammount()
    


# In[157]:


df


# ### Discussion of the Solution to Problem 1.1
# 
# The resulting data can is accurate to the month.  It is also account for cases when rides overlap across datetimes.  For example, if a ride begins at 12:00 but ends at 14:00, the query above will count the ridership at hours 12 and 13.   
# 
# The one drawback to this approach is that it can in theory inflate the total_amount value.  If considering 1 minute intervals as opposed to an hour the rate of hour expands the total_amount value too greatly.  The solution to the problem would be to work with the rate to recalculate the total amount per hour, minute, etc.  Thankfully, as most rides are less than an hour long, it is uncecessary for the question posed.  

# ## Question 1.2
# 
# What has been the average hourly passenger count throughout the year?

# In[169]:


def hourly_count_through_year():


    query_string_2 = """
        with clean as (      
            SELECT 
            t.*,
            FROM
            (
            SELECT *,
            TIMESTAMP_DIFF(dropoff_datetime,pickup_datetime,SECOND) as time_duration_in_secs,
            TIMESTAMP_DIFF(dropoff_datetime,pickup_datetime,MINUTE) as time_duration_in_mins,
            ROUND(trip_distance/TIMESTAMP_DIFF(dropoff_datetime,pickup_datetime,SECOND),2)*3600 as driving_speed_miles_per_hour,
            (CASE WHEN total_amount=0 THEN 0
            ELSE ROUND(tip_amount*100/total_amount,2) END) as tip_rate,
            EXTRACT(YEAR from pickup_datetime) as pickup_year,
            EXTRACT(MONTH from pickup_datetime) as pickup_month,
            CONCAT(CAST(EXTRACT(YEAR from pickup_datetime) as STRING),"-",CAST(EXTRACT(MONTH from pickup_datetime) AS STRING)) as pickup_yearmonth,
            EXTRACT(DATE from pickup_datetime) as pickup_date,
            FORMAT_DATE('%A',DATE(pickup_datetime)) as pickup_weekday_name,
            EXTRACT(HOUR from pickup_datetime) as pickup_hour,
            EXTRACT(YEAR from dropoff_datetime) as dropoff_year,
            EXTRACT(MONTH from dropoff_datetime) as dropoff_month,
            CONCAT(CAST(EXTRACT(YEAR from dropoff_datetime) as STRING),"-",CAST(EXTRACT(MONTH from dropoff_datetime) AS STRING)) as dropoff_yearmonth,
            EXTRACT(DATE from dropoff_datetime) as dropoff_date,
            FORMAT_DATE('%A',DATE(dropoff_datetime)) as dropoff_weekday_name,
            EXTRACT(HOUR from dropoff_datetime) as dropoff_hour
            FROM `nyc-tlc.green.trips_2015`
            /* filter by latitude & longitude that are within the correct range */
            WHERE 
                ((pickup_latitude BETWEEN -90 AND 90) AND
                (pickup_longitude BETWEEN -180 AND 180)) 
            AND
                ((dropoff_latitude BETWEEN -90 AND 90) AND
                (dropoff_longitude BETWEEN -180 AND 180))
            ) t
            WHERE 
            pickup_datetime BETWEEN '2015-01-01' AND '2016-12-31' 
            AND dropoff_datetime BETWEEN '2015-01-01' AND '2016-12-31'
            AND passenger_count > 0
            AND trip_distance >= 0 
            AND tip_amount >= 0 
            AND tolls_amount >= 0 
            AND mta_tax >= 0 
            AND fare_amount >= 0
            AND total_amount >= 0
            )
            #standardSQL
            select date_trunc(int, hour) Hour_Datetime,
            count(pickup_datetime) rides,
            sum(passenger_count) as passenger_count,
            avg(passenger_count) as avg_passenger_count,
            from clean,
            unnest(generate_timestamp_array(
            pickup_datetime, 
            dropoff_datetime, 
            interval 1 hour)) as int
            group by Hour_Datetime
            order by Hour_Datetime
            
            """

## In theory the interval could be as small as 1 minute.  Doing so could in theory be more accurate, however, it may also overcount the total ammount billed and the passenger count in the group by.

    result = query_big_query(query_string=query_string_2)
    df = result.to_dataframe()
    return df

df = hourly_count_through_year()
    


# In[170]:


df


# ### Discussion of Question 1.2
# 
# At first, I was confused why the data terminated at 2015-07-01.  I thought, I had made a mistake. I tested the data on the yellow line data without error.  I then reviewed the big query table to find that it actually terminates at 2015-07-01. 
# 
# 

# ## Question 1.3
# 
# * What has been the change/delta in total amount billed over days? What we would like see is how much (positive or negative)?

# In[188]:


def difference_by_day():


    query_string_2 = """
        with clean as (      
            SELECT 
            t.*,
            FROM
            (
            SELECT *,
            TIMESTAMP_DIFF(dropoff_datetime,pickup_datetime,SECOND) as time_duration_in_secs,
            TIMESTAMP_DIFF(dropoff_datetime,pickup_datetime,MINUTE) as time_duration_in_mins,
            ROUND(trip_distance/TIMESTAMP_DIFF(dropoff_datetime,pickup_datetime,SECOND),2)*3600 as driving_speed_miles_per_hour,
            (CASE WHEN total_amount=0 THEN 0
            ELSE ROUND(tip_amount*100/total_amount,2) END) as tip_rate,
            EXTRACT(YEAR from pickup_datetime) as pickup_year,
            EXTRACT(MONTH from pickup_datetime) as pickup_month,
            CONCAT(CAST(EXTRACT(YEAR from pickup_datetime) as STRING),"-",CAST(EXTRACT(MONTH from pickup_datetime) AS STRING)) as pickup_yearmonth,
            EXTRACT(DATE from pickup_datetime) as pickup_date,
            FORMAT_DATE('%A',DATE(pickup_datetime)) as pickup_weekday_name,
            EXTRACT(HOUR from pickup_datetime) as pickup_hour,
            EXTRACT(YEAR from dropoff_datetime) as dropoff_year,
            EXTRACT(MONTH from dropoff_datetime) as dropoff_month,
            CONCAT(CAST(EXTRACT(YEAR from dropoff_datetime) as STRING),"-",CAST(EXTRACT(MONTH from dropoff_datetime) AS STRING)) as dropoff_yearmonth,
            EXTRACT(DATE from dropoff_datetime) as dropoff_date,
            FORMAT_DATE('%A',DATE(dropoff_datetime)) as dropoff_weekday_name,
            EXTRACT(HOUR from dropoff_datetime) as dropoff_hour
            FROM `nyc-tlc.green.trips_2015`
            /* filter by latitude & longitude that are within the correct range */
            WHERE 
                ((pickup_latitude BETWEEN -90 AND 90) AND
                (pickup_longitude BETWEEN -180 AND 180)) 
            AND
                ((dropoff_latitude BETWEEN -90 AND 90) AND
                (dropoff_longitude BETWEEN -180 AND 180))
            ) t
            /* find the boroughs and zone names for dropoff locations */
            INNER JOIN `bigquery-public-data.new_york_taxi_trips.taxi_zone_geom` tz_do ON 
            (ST_DWithin(tz_do.zone_geom,ST_GeogPoint(dropoff_longitude, dropoff_latitude), 0))
            /* find the boroughs and zone names for pickup locations */
            INNER JOIN `bigquery-public-data.new_york_taxi_trips.taxi_zone_geom` tz_pu ON 
            (ST_DWithin(tz_pu.zone_geom,ST_GeogPoint(pickup_longitude, pickup_latitude), 0))
            WHERE 
            pickup_datetime BETWEEN '2015-01-01' AND '2016-12-31' 
            AND dropoff_datetime BETWEEN '2015-01-01' AND '2016-12-31'
            AND TIMESTAMP_DIFF(dropoff_datetime,pickup_datetime,SECOND) > 0
            AND passenger_count > 0
            AND trip_distance >= 0 
            AND tip_amount >= 0 
            AND tolls_amount >= 0 
            AND mta_tax >= 0 
            AND fare_amount >= 0
            AND total_amount >= 0
            ),
            daily as(
            #standardSQL
            select date_trunc(int, DAY) DAY_Datetime,
            count(pickup_datetime) rides,
            sum(total_amount) as total_amount,
            avg(total_amount) as avg_total_amount
            from clean,
            unnest(generate_timestamp_array(
            pickup_datetime, 
            dropoff_datetime, 
            interval 1 hour)) as int
            group by DAY_Datetime
            order by DAY_Datetime
            )

            select *,
            total_amount - LAG(total_amount) OVER (ORDER BY DAY_Datetime) AS Difference
            FROM daily;
            
        
         """

## In theory the interval could be as small as 1 minute.  Doing so could in theory be more accurate, however, it may also overcount the total ammount billed and the passenger count in the group by.

    result = query_big_query(query_string=query_string_2)
    df = result.to_dataframe()
    return df

df = difference_by_day()
    


# In[189]:


df


# ### Discussion of Question 1.3
# 
# The approach is almost identical to my previous answers.  The only major difference is the inclusion of the lag function to determine the running differences.  

# 

# ## Question 1.4
# 
# * What hour of the day has seen the longest rides in April?
# 

# ### Date_trunc Method
# 
# Date_trunc will return the requested results per date per hour.

# In[209]:


def longest_rides_per_hour():


    query_string_2 = """
        with clean as (      
            SELECT 
            t.*,
            FROM
            (
            SELECT *,
            TIMESTAMP_DIFF(dropoff_datetime,pickup_datetime,SECOND) as time_duration_in_secs,
            TIMESTAMP_DIFF(dropoff_datetime,pickup_datetime,MINUTE) as time_duration_in_mins,
            ROUND(trip_distance/TIMESTAMP_DIFF(dropoff_datetime,pickup_datetime,SECOND),2)*3600 as driving_speed_miles_per_hour,
            (CASE WHEN total_amount=0 THEN 0
            ELSE ROUND(tip_amount*100/total_amount,2) END) as tip_rate,
            EXTRACT(YEAR from pickup_datetime) as pickup_year,
            EXTRACT(MONTH from pickup_datetime) as pickup_month,
            CONCAT(CAST(EXTRACT(YEAR from pickup_datetime) as STRING),"-",CAST(EXTRACT(MONTH from pickup_datetime) AS STRING)) as pickup_yearmonth,
            EXTRACT(DATE from pickup_datetime) as pickup_date,
            FORMAT_DATE('%A',DATE(pickup_datetime)) as pickup_weekday_name,
            EXTRACT(HOUR from pickup_datetime) as pickup_hour,
            EXTRACT(YEAR from dropoff_datetime) as dropoff_year,
            EXTRACT(MONTH from dropoff_datetime) as dropoff_month,
            CONCAT(CAST(EXTRACT(YEAR from dropoff_datetime) as STRING),"-",CAST(EXTRACT(MONTH from dropoff_datetime) AS STRING)) as dropoff_yearmonth,
            EXTRACT(DATE from dropoff_datetime) as dropoff_date,
            FORMAT_DATE('%A',DATE(dropoff_datetime)) as dropoff_weekday_name,
            EXTRACT(HOUR from dropoff_datetime) as dropoff_hour
            FROM `nyc-tlc.green.trips_2015`
            /* filter by latitude & longitude that are within the correct range */
            WHERE 
                ((pickup_latitude BETWEEN -90 AND 90) AND
                (pickup_longitude BETWEEN -180 AND 180)) 
            AND
                ((dropoff_latitude BETWEEN -90 AND 90) AND
                (dropoff_longitude BETWEEN -180 AND 180))
            ) t
            /* find the boroughs and zone names for dropoff locations */
            INNER JOIN `bigquery-public-data.new_york_taxi_trips.taxi_zone_geom` tz_do ON 
            (ST_DWithin(tz_do.zone_geom,ST_GeogPoint(dropoff_longitude, dropoff_latitude), 0))
            /* find the boroughs and zone names for pickup locations */
            INNER JOIN `bigquery-public-data.new_york_taxi_trips.taxi_zone_geom` tz_pu ON 
            (ST_DWithin(tz_pu.zone_geom,ST_GeogPoint(pickup_longitude, pickup_latitude), 0))
            WHERE 
            pickup_datetime BETWEEN '2015-01-01' AND '2016-12-31' 
            AND dropoff_datetime BETWEEN '2015-01-01' AND '2016-12-31'
            AND TIMESTAMP_DIFF(dropoff_datetime,pickup_datetime,SECOND) > 0
            AND passenger_count > 0
            AND trip_distance >= 0 
            AND tip_amount >= 0 
            AND tolls_amount >= 0 
            AND mta_tax >= 0 
            AND fare_amount >= 0
            AND total_amount >= 0
            ),
            hourly as(
            #standardSQL
            select date_trunc(int, hour) DAY_Datetime,
            count(pickup_datetime) rides,
            sum(total_amount) as total_amount,
            avg(total_amount) as avg_total_amount,
            avg(time_duration_in_mins) as avg_trip_duration_mins,
            max(time_duration_in_mins) as max_time_duration_mins,
            avg(trip_distance) as avg_trip_distance,
            max(trip_distance) as max_trip_distance
            from clean,
            unnest(generate_timestamp_array(
            pickup_datetime, 
            dropoff_datetime, 
            interval 1 hour)) as int
            where pickup_datetime BETWEEN '2015-04-01' AND '2015-04-30' 
            AND dropoff_datetime BETWEEN '2015-04-01' AND '2015-04-30' 
            group by DAY_Datetime
            order by DAY_Datetime
            )

            select *,
            FROM hourly
            order by avg_trip_distance DESC, avg_trip_duration_mins DESC;
            
        
         """

## In theory the interval could be as small as 1 minute.  Doing so could in theory be more accurate, however, it may also overcount the total ammount billed and the passenger count in the group by.

    result = query_big_query(query_string=query_string_2)
    df = result.to_dataframe()
    return df

df = longest_rides_per_hour()
    


# In[210]:


df


# #### Discussion of Date Trunc Method

# I wanted to see if avg_trip_duration would correlate with avg_trip_distance.  
# 
# In this sample it does seem to. I would like to test the distributions later for correlation. 
# 
# To answer the question, 2014-04-22 at 5:00 am recorded the longest trips.  Interestingly, most of longest trips are at 5:00.  I expected the evening rush hour to record a larger number of results. As this is the green line, it would make sense that a large majority of taking the vehicle to the airport or to a determined destination as opposed to randomly hailing a yellow cab.  
# 
# Review the code below for a results below for a more succint table.  
# 

# ### The Extract Method
# 
# Extract will record the values by hour of the 24 hour clock.  It will aggregate accordinly.

# In[211]:


def longest_rides_per_hour_etracted():


    query_string_2 = """
        with clean as (      
            SELECT 
            t.*,
            FROM
            (
            SELECT *,
            TIMESTAMP_DIFF(dropoff_datetime,pickup_datetime,SECOND) as time_duration_in_secs,
            TIMESTAMP_DIFF(dropoff_datetime,pickup_datetime,MINUTE) as time_duration_in_mins,
            ROUND(trip_distance/TIMESTAMP_DIFF(dropoff_datetime,pickup_datetime,SECOND),2)*3600 as driving_speed_miles_per_hour,
            (CASE WHEN total_amount=0 THEN 0
            ELSE ROUND(tip_amount*100/total_amount,2) END) as tip_rate,
            EXTRACT(YEAR from pickup_datetime) as pickup_year,
            EXTRACT(MONTH from pickup_datetime) as pickup_month,
            CONCAT(CAST(EXTRACT(YEAR from pickup_datetime) as STRING),"-",CAST(EXTRACT(MONTH from pickup_datetime) AS STRING)) as pickup_yearmonth,
            EXTRACT(DATE from pickup_datetime) as pickup_date,
            FORMAT_DATE('%A',DATE(pickup_datetime)) as pickup_weekday_name,
            EXTRACT(HOUR from pickup_datetime) as pickup_hour,
            EXTRACT(YEAR from dropoff_datetime) as dropoff_year,
            EXTRACT(MONTH from dropoff_datetime) as dropoff_month,
            CONCAT(CAST(EXTRACT(YEAR from dropoff_datetime) as STRING),"-",CAST(EXTRACT(MONTH from dropoff_datetime) AS STRING)) as dropoff_yearmonth,
            EXTRACT(DATE from dropoff_datetime) as dropoff_date,
            FORMAT_DATE('%A',DATE(dropoff_datetime)) as dropoff_weekday_name,
            EXTRACT(HOUR from dropoff_datetime) as dropoff_hour
            FROM `nyc-tlc.green.trips_2015`
            /* filter by latitude & longitude that are within the correct range */
            WHERE 
                ((pickup_latitude BETWEEN -90 AND 90) AND
                (pickup_longitude BETWEEN -180 AND 180)) 
            AND
                ((dropoff_latitude BETWEEN -90 AND 90) AND
                (dropoff_longitude BETWEEN -180 AND 180))
            ) t
            /* find the boroughs and zone names for dropoff locations */
            INNER JOIN `bigquery-public-data.new_york_taxi_trips.taxi_zone_geom` tz_do ON 
            (ST_DWithin(tz_do.zone_geom,ST_GeogPoint(dropoff_longitude, dropoff_latitude), 0))
            /* find the boroughs and zone names for pickup locations */
            INNER JOIN `bigquery-public-data.new_york_taxi_trips.taxi_zone_geom` tz_pu ON 
            (ST_DWithin(tz_pu.zone_geom,ST_GeogPoint(pickup_longitude, pickup_latitude), 0))
            WHERE 
            pickup_datetime BETWEEN '2015-01-01' AND '2016-12-31' 
            AND dropoff_datetime BETWEEN '2015-01-01' AND '2016-12-31'
            AND TIMESTAMP_DIFF(dropoff_datetime,pickup_datetime,SECOND) > 0
            AND passenger_count > 0
            AND trip_distance >= 0 
            AND tip_amount >= 0 
            AND tolls_amount >= 0 
            AND mta_tax >= 0 
            AND fare_amount >= 0
            AND total_amount >= 0
            ),
            hourly as(
            #standardSQL
            select EXTRACT(HOUR from int) DAY_Datetime,
            count(pickup_datetime) rides,
            sum(total_amount) as total_amount,
            avg(total_amount) as avg_total_amount,
            avg(time_duration_in_mins) as avg_trip_duration_mins,
            max(time_duration_in_mins) as max_time_duration_mins,
            avg(trip_distance) as avg_trip_distance,
            max(trip_distance) as max_trip_distance
            from clean,
            unnest(generate_timestamp_array(
            pickup_datetime, 
            dropoff_datetime, 
            interval 1 hour)) as int
            where pickup_datetime BETWEEN '2015-04-01' AND '2015-04-30' 
            AND dropoff_datetime BETWEEN '2015-04-01' AND '2015-04-30' 
            group by DAY_Datetime
            order by DAY_Datetime
            )

            select *,
            FROM hourly
            order by avg_trip_distance DESC, avg_trip_duration_mins DESC;
            
        
         """

## In theory the interval could be as small as 1 minute.  Doing so could in theory be more accurate, however, it may also overcount the total ammount billed and the passenger count in the group by.

    result = query_big_query(query_string=query_string_2)
    df = result.to_dataframe()
    return df

df = longest_rides_per_hour_etracted()
    


# In[212]:


df


# #### Discussion of the Extract Method
# 
# The longest time duration is recorded at 5 am.  The distance between 5 and 6 am are marginal.  
