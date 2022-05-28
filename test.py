from google.cloud import bigquery
from pprint import pprint



def query_big_query(query_string):
    client = bigquery.Client()
    query_job = client.query(query_string
    )

    results = query_job.result()  # Waits for job to complete.
    return results

def query_passengers_by_month():
    query_string = """
        SELECT date_trunc(dropoff_datetime,MONTH) as Month,
        sum(passenger_count) as Sum_PASS,
        sum(total_amount) as TOTAL_AMOUNT_SUM
        FROM `nyc-tlc.green.trips_2015` 
        where dropoff_datetime BETWEEN '2015-02-01' AND '2015-04-30'
        GROUP BY Month;
        """

    result = query_big_query(query_string = query_string)

    df = result.to_dataframe()
    pprint(df)

def query_average_ridership_every_hour():
    #What has been the average hourly passenger count throughout the year?
    query_string = """
        SELECT EXTRACT(hour from dropoff_datetime ) as dropoff_hour,
        EXTRACT(hour from pickup_datetime) as pickup_hour,
        avg(passenger_count) as Average
        FROM `nyc-tlc.green.trips_2015` 
        where dropoff_datetime BETWEEN '2015-01-01' AND '2015-12-31' AND (dropoff_hour = pickup_hour)
        GROUP BY dropoff_hour,pickup_hour
        Order BY dropoff_hour, pickup_hour;
        """
    result = query_big_query(query_string = query_string)

    for row in result:
        print(row)


def query_average_hourly_ridership():
     #What has been the average hourly passenger count throughout the year?
    query_string = """
        SELECT EXTRACT(hour from pickup_datetime) as Hour,
        avg(passenger_count) as AVG
        FROM `nyc-tlc.green.trips_2015` 
        where dropoff_datetime BETWEEN '2015-01-01' AND '2015-12-31'
        GROUP BY Hour
        ORDER by Hour;
        """


    result = query_big_query(query_string = query_string)

    for row in result:
        print(row)


def super_tester():
    query_string = """
        SELECT

            entity.pickup_time,
        """

    result = query_big_query(query_string = query_string)

    for row in result:
        print(row)


def dif_billed_per_day():
    query_string = """
    SELECT
    pickup_datetime,
    EXTRACT(ISOYEAR FROM date) AS isoyear,
    EXTRACT(ISOWEEK FROM date) AS isoweek,
    EXTRACT(YEAR FROM date) AS year,
    EXTRACT(WEEK FROM date) AS week
    FROM UNNEST(GENERATE_DATE_ARRAY('2015-12-23', '2016-01-09')) AS date
    ORDER BY date;

    """
    




def query_longest_distance_hour_avg():
    # aggregate average length by hour
    # where month is april
    #return maximum 

    query_string = """
        with a as (
        SELECT EXTRACT(hour from pickup_datetime) as hour,
        avg(distance_between_service) as AVG_Distance
        FROM `nyc-tlc.green.trips_2015` 
        where dropoff_datetime BETWEEN '2015-04-01' AND '2015-4-30'
        GROUP BY Hour
        ORDER by AVG_Distance DESC
        )

        select * 
        from a
        """
        

    


    result = query_big_query(query_string = query_string)

    for row in result:
        print(row)


def query_longest_distance_max():
    # aggregate average length by hour
    # where month is april
    #return maximum 

    query_string = """
        with a as (
        SELECT EXTRACT(hour from pickup_datetime) as hour,
        MAX(distance_between_service) as MAX_Distance
        FROM `nyc-tlc.green.trips_2015` 
        where dropoff_datetime BETWEEN '2015-04-01' AND '2015-4-30'
        GROUP BY Hour
        ORDER by MAX_Distance DESC
        )

        select * 
        from a
        """
        

    result = query_big_query(query_string = query_string)

    for row in result:
        print(row)


def a_difficult_problem():

    query_string = """  SELECT
    MAX(overlapAtEnd)
    FROM
    (
        SELECT 
            COUNT(1) AS overlapAtEnd                        
        FROM 
            `nyc-tlc.green.trips_2015` AS t1, 
            `nyc-tlc.green.trips_2015` AS t2
        WHERE 
                t2.pickup_datetime <= t1.dropoff_datetime
            AND t2.pickup_datetime >= t1.dropoff_datetime - (SELECT MAX(dropoff_datetime - pickup_datetime) FROM `nyc-tlc.green.trips_2015`)
            AND t2.dropoff_datetime   >= t1.dropoff_datetime
        GROUP BY t1.pickup_datetime
    ) AS foo LIMIT 100

    """

    result = query_big_query(query_string = query_string)

    for row in result:
        print(row)


def another_difficult_problem():

    query_string = """
        with d AS (
            SELECT pickup_datetime as dt
            from 
            `nyc-tlc.green.trips_2015`
        )
        select
        d.dt,
        count(case when t.pickup_datetime = d.dt then 1 end) as Adds,
        count(case when d.dt > t.pickup_datetime and case when d.dt < t.dropoff_datetime as Existing,
        count(case when t.dropoff_datetime = d.dt then 1 end) as Closed
        from `nyc-tlc.green.trips_2015` t inner join Dates d on d.dt <= coalesce(t.dropoff_datetime)
        group by d.dt;
    """


        

    result = query_big_query(query_string)

    for row in result:
        print(row)


def another_another_difficult_problem():

    query_string = """
    #standardSQL
    SELECT MAX(maxOLP)
    FROM
    (
        SELECT MAX(olp) AS maxOLP
        FROM
        (
            SELECT 
                MAX(overlapAtEnd) AS maxOLP,
                EXTRACT(HOUR FROM t1.dropoff_datetime)  AS hr
            FROM
            (
                SELECT 
                    COUNT(1) AS overlapAtEnd            
                FROM 
                    nyc-tlc.green.trips_2015 AS t1, 
                    nyc-tlc.green.trips_2015 AS t2
                WHERE 
                    t1.dropoff_datetime BETWEEN t2.pickup_datetime AND t2.dropoff_datetime
                GROUP BY t1.pickup_datetime
            ) AS foo
            GROUP BY t1.pickup_datetime, EXTRACT(HOUR FROM t1.dropoff_datetime)
        ) AS foo
        GROUP BY hr
    ) AS foo2
    """


    query_2 = """
                SELECT 
                    COUNT(1) AS overlapAtEnd            
                FROM 
                    nyc-tlc.green.trips_2015 AS t1, 
                    nyc-tlc.green.trips_2015 AS t2
                WHERE 
                    t1.dropoff_datetime BETWEEN t2.pickup_datetime AND t2.dropoff_datetime
                GROUP BY t1.pickup_datetime
                limit 1
    """



    result = query_big_query(query_string=query_2)

    for row in result:
        pprint(row)


def calendar_query():
    str = """
    SELECT CAST(pickup_datetime as date) AS ForDate,
       EXTRACT(hour from pickup_datetime) AS OnHour,
       COUNT(*) AS TotalStarts,
       SUM(CASE WHEN CAST(pickup_datetime as date) <> CAST(dropoff_datetime as date) or
                     Extract(hour from pickup_datetime) <> EXTRACT(hour from dropoff_datetime)
                THEN 1
                ELSE 0
           END) as StartedButNotEndedInHour
        FROM nyc-tlc.green.trips_2015
        GROUP BY CAST(pickup_datetime as date),
       EXTRACT(hour from pickup_datetime)"""

    result = query_big_query(query_string=str)

    for row in result:
        pprint(row)


def question1_2():

    query_str=   """
        with se as (select *, pickup_datetime as time, 1 as inc from nyc-tlc.green.trips_2015
        union all
        select *, dropoff_datetime, -1 as inc from nyc-tlc.green.trips_2015
        order by time),
        se2 as (
        select time, sum(sum(inc)) over (order by time) as active_taxis, avg(passenger_count) as average_passenger_count
        from se
        group by time
        qualify row_number() over (partition by date_trunc(time, hour) order by time) = 1
        order by date_trunc(time, hour)
        )
        select date_trunc(time, hour) as time, active_taxis, average_passenger_count from se2
        order by time
    """

    result = query_big_query(query_string=query_str)

    for row in result: 
        pprint(row)


def question1_2_2():

    query_str=   """
        with se as (select *, pickup_datetime as time, 1 as inc from nyc-tlc.green.trips_2015
        union all
        select *, dropoff_datetime, -1 as inc from nyc-tlc.green.trips_2015
        order by time),
        se2 as (
        select time, sum(sum(inc)) over (order by time) as active_taxis, avg(passenger_count) as average_passenger_count
        from se
        group by time
        qualify row_number() over (partition by date_trunc(time, hour) order by time) = 1
        order by date_trunc(time, hour)
        )
        select EXTRACT(hour from time) as hour, avg(active_taxis)as average_active_taxis, avg(average_passenger_count) as average_passenger_count
        from se2
        group by hour
        order by hour;

        """    

    result = query_big_query(query_string=query_str)

    for row in result: 
        pprint(row)



def query_difference_by_day():
         #What has been the average hourly passenger count throughout the year?


    query_str=   """
        with se as (select *, pickup_datetime as time, 1 as inc from nyc-tlc.green.trips_2015
        union all
        select *, dropoff_datetime, -1 as inc from nyc-tlc.green.trips_2015
        order by time),
        se2 as (
        select time, sum(sum(inc)) over (order by time) as active_taxis, sum(sum(total_amount)) over (order by time) as total_billed
        from se
        group by time
        qualify row_number() over (partition by date_trunc(time, day) order by time) = 1
        order by date_trunc(time, day)
        ),
        se3 as (select time, active_taxis, total_billed, lag(total_billed) over (order by time) as pre_value from se2  qualify row_number() over (partition by date_trunc(time, day) order by time) = 1 order by time )
        select * from se  

        """    


    test = """
        with se as (select total_amount, pickup_datetime as time, 1 as inc from nyc-tlc.green.trips_2015
        union all
        select total_amount, dropoff_datetime, -1 as inc from nyc-tlc.green.trips_2015
        order by time),
        se2 as (
        select time, sum(sum(inc)) over (order by time) as active_taxis, sum(total_amount) as total_billed
        from se
        group by time
        qualify row_number() over (partition by date_trunc(time, day) order by time) = 1
        order by date_trunc(time, day)
        ),
        se3 as (select time, active_taxis, total_billed, lag(total_billed) over (order by time) as pre_value from se2 order by time)
        select *, total_billed - pre_value as difference from se3

    """


    result = query_big_query(query_string=test)

    for row in result: 
        pprint(row)


def longest_ride():

    test = """
        with se as (select distance_between_service, pickup_datetime as time, 1 as inc from nyc-tlc.green.trips_2015 where dropoff_datetime BETWEEN '2015-04-01' AND '2015-04-30'
        union all
        select distance_between_service, dropoff_datetime, -1 as inc from nyc-tlc.green.trips_2015 where dropoff_datetime BETWEEN '2015-04-01' AND '2015-04-30'
        order by time),
        se2 as (
        select time, sum(sum(inc)) over (order by time) as active_taxis, max(distance_between_service) as maximum
        from se
        group by time
        qualify row_number() over (partition by date_trunc(time, hour) order by time) = 1
        order by maximum DESC,date_trunc(time, hour)
        )
        select * from se2

    """

    result = query_big_query(query_string=test)

    for row in result: 
        pprint(row)


def total_passenger_total_ammount():

    test = """
        with se as (select total_amount, passenger_count, pickup_datetime as time, 1 as inc from nyc-tlc.green.trips_2015 where dropoff_datetime BETWEEN '2015-02-01' AND '2015-04-30'
        union all
        select total_amount, passenger_count, dropoff_datetime, -1 as inc from nyc-tlc.green.trips_2015 where dropoff_datetime BETWEEN '2015-02-01' AND '2015-04-30'
        order by time),
        se2 as (
        select time, sum(sum(inc)) over (order by time) as active_taxis, sum(total_amount) as amount_billed, sum(passenger_count) as passenger_count
        from se
        group by time
        qualify row_number() over (partition by date_trunc(time, month) order by time) = 1
        order by date_trunc(time, hour) DESC
        )
        select * from se2

    """

    

    result = query_big_query(query_string=test)
    df = result.to_dataframe()
    pprint(df)

def beautiful_solution():
    string = """

    #standardSQL
    WITH check_times AS (
      SELECT pickup_datetime AS TIME FROM nyc-tlc.green.trips_2015 UNION DISTINCT
      SELECT dropoff_datetime AS TIME FROM nyc-tlc.green.trips_2015 
    ),
    distinct_intervals AS (
      SELECT TIME AS pickup_datetime, LEAD(TIME) OVER(PARTITION BY TIME ORDER BY TIME) dropoff_datetime
      FROM check_times
    ), deduped_intervals AS (
      SELECT a.pickup_datetime, a.dropoff_datetime, MAX(passenger_count) passenger_count, ANY_VALUE(To_JSON_STRING(b)) event_hash
      FROM distinct_intervals a
      JOIN `nyc-tlc.green.trips_2015` b
      ON a.pickup_datetime = b.pickup_datetime
      AND a.pickup_datetime BETWEEN b.pickup_datetime AND b.dropoff_datetime 
      AND a.dropoff_datetime BETWEEN b.pickup_datetime AND b.dropoff_datetime
      GROUP BY a.pickup_datetime, a.dropoff_datetime
    ), combined_intervals AS (
      SELECT MIN(pickup_datetime) pickup_datetime, MAX(dropoff_datetime) dropoff_datetime, MAX(passenger_count) passenger_count, COUNT(DISTINCT event_hash) events
      FROM (
        SELECT *, COUNTIF(flag) OVER(PARTITION BY pickup_datetime ORDER BY pickup_datetime) grp
        FROM (
          SELECT *,
            pickup_datetime != IFNULL(LAG(dropoff_datetime) OVER(PARTITION BY pickup_datetime ORDER BY pickup_datetime), pickup_datetime) flag
          FROM deduped_intervals
        )
      )
      GROUP BY grp
    )
    SELECT *
    FROM combined_intervals
    """


    test = """
        #standardSQL
    WITH check_times AS (
    SELECT pickup_datetime AS TIME FROM `nyc-tlc.green.trips_2015` UNION DISTINCT
    SELECT dropoff_datetime AS TIME FROM `nyc-tlc.green.trips_2015` 
    ), distinct_intervals AS (
    SELECT TIME AS pickup_datetime, LEAD(TIME) OVER(PARTITION BY TIME ORDER BY TIME) dropoff_datetime
    FROM check_times
    ), deduped_intervals AS (
    SELECT a.pickup_datetime, a.dropoff_datetime, MAX(passenger_count) passenger_count 
    FROM distinct_intervals a
    JOIN `nyc-tlc.green.trips_2015` b
    ON a.pickup_datetime = b.pickup_datetime 
    AND a.pickup_datetime BETWEEN b.pickup_datetime AND b.dropoff_datetime 
    AND a.dropoff_datetime BETWEEN b.pickup_datetime AND b.dropoff_datetime
    GROUP BY a.pickup_datetime, a.dropoff_datetime
    ), combined_intervals AS (
    SELECT MIN(pickup_datetime) pickup_datetime, MAX(dropoff_datetime) dropoff_datetime, MAX(passenger_count) passenger_count 
    FROM (
        SELECT pickup_datetime, dropoff_datetime, passenger_count, COUNTIF(flag) OVER(PARTITION BY pickup_datetime ORDER BY pickup_datetime) grp
        FROM (
        SELECT pickup_datetime, dropoff_datetime, passenger_count,
            pickup_datetime != IFNULL(LAG(dropoff_datetime) OVER(PARTITION BY pickup_datetime ORDER BY pickup_datetime), pickup_datetime) flag
        FROM deduped_intervals
        )
    )
    GROUP BY grp
    )
    SELECT *
    FROM combined_intervals
    """

    tester = """
        #standardSQL
        SELECT 
        pickup_datetime,
        (SELECT COUNT(1) FROM UNNEST(ends) AS e WHERE e >= pickup_datetime) AS cnt  
        FROM (
        SELECT 
            pickup_datetime, 
            ARRAY_AGG(pickup_datetime) OVER(ORDER BY pickup_datetime) AS ends
        FROM nyc-tlc.green.trips_2015
        )
        -- ORDER BY pickup_datetime 
    """


    meek = """
    SELECT
CASE WHEN TipPercentage < 0 THEN 'No Tip'
WHEN TipPercentage BETWEEN 0 AND 5 THEN 'Less but still a Tip'
WHEN TipPercentage BETWEEN 5 AND 10 THEN 'Decent Tip'
WHEN TipPercentage > 10 THEN 'Good Tip'
ELSE 'Something different'
END AS TipRange,
Hr,
Wk,
TripMonth,
Trips,
Tips,
AverageSpeed,
AverageDistance,
TipPercentage,
Tipbin
FROM
(SELECT
EXTRACT(HOUR from pickup_datetime) As Hr,
EXTRACT(DAYOFWEEK from pickup_datetime) As Wk,
Extract (MONTH from pickup_datetime) As TripMonth,
case when tip_amount=0 then 'No Tip'
when (tip_amount > 0 and tip_amount <=5) then '0-5'
when (tip_amount > 5 and tip_amount <=10) then '5-10'
when (tip_amount > 10 and tip_amount <=20) then '10-20'
when tip_amount > 20 then '> 20'
else 'other'
end as Tipbin,
COUNT(*) Trips,
SUM(tip_amount) as Tips,
ROUND(AVG(trip_distance         /
TIMESTAMP_DIFF(dropoff_datetime,pickup_datetime,second))*3600,1) as AverageSpeed,
ROUND(AVG(trip_distance),1) as AverageDistance,
ROUND(avg((tip_amount)/(total_amount-tip_amount))*100,3) as TipPercentage
FROM `bigquery-public-data.new_york.tlc_yellow_trips_2015`
WHERE trip_distance >0
AND fare_amount/trip_distance BETWEEN 2 AND 10
AND dropoff_datetime > pickup_datetime
group by 1,2,3,tip_amount,total_amount,tipbin)
"""


    another_test = """
    SELECT 
    t.*,
    tz_pu.zone_id as pickup_zone_id,
    tz_pu.zone_name as pickup_zone_name,
    tz_pu.borough as pickup_borough,
    tz_do.zone_id as dropoff_zone_id,
    tz_do.zone_name as dropoff_zone_name,
    tz_do.borough as dropoff_borough,
    CONCAT(tz_pu.borough,"-",tz_do.borough) as route_borough,
    CONCAT(tz_pu.zone_name,"-",tz_do.zone_name) as route_zone_name
FROM
(
SELECT *,
    TIMESTAMP_DIFF(dropoff_datetime,pickup_datetime,SECOND) as time_duration_in_secs,
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
FROM `bigquery-public-data.new_york.tlc_yellow_trips_2016`
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
    pickup_datetime BETWEEN '2016-01-01' AND '2016-12-31' 
    AND dropoff_datetime BETWEEN '2016-01-01' AND '2016-12-31'
    AND TIMESTAMP_DIFF(dropoff_datetime,pickup_datetime,SECOND) > 0
    AND passenger_count > 0
    AND trip_distance >= 0 
    AND tip_amount >= 0 
    AND tolls_amount >= 0 
    AND mta_tax >= 0 
    AND fare_amount >= 0
    AND total_amount >= 0"""
    result = query_big_query(another_test)
    for r in result:
        pprint(r)


def justin():

    test = """
        with se as (select total_amount, passenger_count, pickup_datetime as time, 1 as inc from nyc-tlc.green.trips_2015 where dropoff_datetime BETWEEN '2015-02-01' AND '2015-04-30'
        union all
        select total_amount, passenger_count, dropoff_datetime, -1 as inc from nyc-tlc.green.trips_2015 where dropoff_datetime BETWEEN '2015-02-01' AND '2015-04-30'
        order by time)
        select * from se
        limit 10000
    """

    tester = """select total_amount, passenger_count, dropoff_datetime, -1 as inc from nyc-tlc.green.trips_2015 where dropoff_datetime BETWEEN '2015-02-01' AND '2015-04-30'"""


    another = """SELECT
        ROW_NUMBER () OVER (ORDER BY pickup_datetime, dropoff_datetime) AS RN,
        pickup_datetime,
        dropoff_datetime,
        MAX(dropoff_datetime) OVER (PARTITION BY pickup_datetime ORDER BY pickup_datetime, pickup_datetime ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS PreviousEndDate,
        FROM
        nyc-tlc.green.trips_2015 where dropoff_datetime BETWEEN '2015-02-01' AND '2015-04-30' LIMIT 10000"""

    another2 = """
        #standardSQL
        select timestamp_trunc(minute, hour) hour, 
        count(pickup_datetime) rides,
        avg(passenger_count) avg_passenger_count,
        avg(distance_between_service) avg_distance,
        sum(total_amount) total_amount,
        from `nyc-tlc.green.trips_2015`, 
        unnest(generate_timestamp_array(
        pickup_datetime, 
        dropoff_datetime, 
        interval 10 MINUTE)) minute
        group by hour
        order by hour
        limit 1000
         """


    query_string_2 = """
        with clean as (      
            SELECT 
            t.*,
            FROM
            (
            SELECT *,
            TIMESTAMP_DIFF(dropoff_datetime,pickup_datetime,SECOND) as time_duration_in_secs,
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
            pickup_datetime BETWEEN '2015-01-01' AND '2015-12-31' 
            AND dropoff_datetime BETWEEN '2015-01-01' AND '2015-12-31'
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
            select date_trunc(int, hour) Hour_Datetime,
            count(pickup_datetime) rides,
            sum(passenger_count) as passenger_count,
            avg(passenger_count) as avg_passenger_count,
            from clean
            CROSS JOIN unnest(generate_timestamp_array(
            pickup_datetime, 
            dropoff_datetime, 
            interval 1 hour)) as int
            group by Hour_Datetime
            order by Hour_Datetime
            
         """
    result = query_big_query(query_string_2)
    #df = result.to_dataframe()
    #pprint(df)
    for row in result:
        pprint(row)



def pretty():
    string = """SELECT pickup_datetime AS ForDate,
       DATE_TRUNC(hour from pickup_datetime) AS OnHour,
       COUNT(*) AS TotalStarts,
       SUM(CASE WHEN pickup_datetime <> dropoff_datetime or
                     DATE_TRUNC(hour from pickup_datetime) <> DATE_TRUNC(hour from dropoff_datetime)
                THEN 1
                ELSE 0
           END) as StartedButNotEndedInHour
        FROM `nyc-tlc.green.trips_2015`
        GROUP BY pickup_datetime,
            DATE_TRUNC(hour from pickup_datetime)
       """

    result = query_big_query(string)
    
    

if __name__ == "__main__":
    #query_passengers_by_month()
    #query_difference_by_day()
    #query_average_ridership_every_hour()
    #super_tester()
    #query_difference_by_day()
    #query_longest_day()
    #query_longest_hour_max()
    #a_difficult_problem()
    #another_another_difficult_problem()
    #calendar_query(#
    #question1_2()
    #question1_2_2()
    #longest_ride()
    #total_passenger_total_ammount()
    #query_passengers_by_month()
    #beautiful_solution()
    justin()
    #total_passenger_total_ammount()
    #query_passengers_by_month()
    #pretty()
    #another_another_difficult_problem()



#
#1) Use the publicly available BigQuery dataset named `nyc-tlc.green.trips_2015`, provide SQL queries to answer the following questions:
#What is the total amount and passenger counts for the months of February, March and April? !ADD total ammount
#What has been the average hourly passenger count throughout the year?  check and check Should be good
#What has been the change/delta in total amount billed over days? What we would like see is how much (positive or negative)  SHould be good !!difference we have seen, day over day, in terms of `total_amount`.
#What hour of the day has seen the longest rides in April?