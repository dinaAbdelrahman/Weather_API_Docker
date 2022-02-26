timezone_adjust="""
ALTER DATABASE weather_processing SET timezone TO 'Europe/London';
"""

# DROP TABLES

cities_table_drop = "Drop table IF EXISTS cities"
weather_table_drop = "Drop table IF EXISTS weather"


# CREATE TABLES

cities_table_create = """
CREATE TABLE IF NOT EXISTS cities
(
city_name varchar,
latitude float,
longitude float
);
ALTER TABLE cities
   ADD CONSTRAINT city_key PRIMARY KEY (city_name);
"""

weather_table_create = """
CREATE TABLE IF NOT EXISTS weather
(
latitude float,
longitude float,
time_stamp bigint,
date_val timestamp, 
month_val varchar,
day_val varchar,
temperature float
);
ALTER TABLE weather
   ADD CONSTRAINT weather_key PRIMARY KEY (latitude, longitude, time_stamp);
"""



# INSERT RECORDS

#cities table 3 fields: 3 fields inputs on the fly
cities_table_insert = """
INSERT INTO cities
(
city_name,
latitude,
longitude
) 
VALUES(%s,%s,%s) ON CONFLICT (city_name) DO NOTHING
"""


#weather table 7 fields: 7 fields inputs on the fly
weather_table_insert ="""
INSERT INTO weather
(
latitude,
longitude,
time_stamp,
date_val, 
month_val,
day_val,
temperature
) 
VALUES(%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (latitude, longitude, time_stamp) DO NOTHING
"""

# Select Statment

Cities_select ="""
select * from cities
"""

dataset1_select_query ="""
WITH T1 AS
				( SELECT LATITUDE,
						LONGITUDE,
						MONTH_VAL,
						MAX(TEMPERATURE) AS MAX_TEMP
					FROM WEATHER
					GROUP BY LATITUDE,
						LONGITUDE,
						MONTH_VAL)
SELECT T1.LATITUDE,
	T1.LONGITUDE,
	W.DATE_VAL,
	W.MONTH_VAL,
	W.TEMPERATURE
FROM T1
LEFT JOIN WEATHER W ON W.LATITUDE = T1.LATITUDE
AND W.LATITUDE = T1.LATITUDE
AND W.TEMPERATURE = T1.MAX_TEMP
"""

dataset2_select_query ="""
WITH T1 AS
				(SELECT DAY_VAL,
						ROUND(AVG(TEMPERATURE)::numeric,2) AVG_TEMP,
						MIN(TEMPERATURE) MIN_TEMP,
						MAX(TEMPERATURE) MAX_TEMP
					FROM WEATHER
					GROUP BY DAY_VAL)
SELECT DISTINCT T1.DAY_VAL,
	T1.AVG_TEMP,
	T1.MIN_TEMP,
	W1.LAT1 LAT_MIN_TEMP,
	W1.LONG1 LONG_MIN_TEMP,
	W2.LAT2 LAT_MAX_TEMP,
	W2.LONG2 LONG_MAX_TEMP
FROM T1
LEFT JOIN
				(SELECT DISTINCT DAY_VAL,
						TEMPERATURE AS TE1,
						LATITUDE AS LAT1,
						LONGITUDE AS LONG1
					FROM WEATHER) W1 ON T1.DAY_VAL = W1.DAY_VAL
AND T1.MIN_TEMP = W1.TE1
LEFT JOIN
				(SELECT DISTINCT DAY_VAL,
						TEMPERATURE AS TE2,
						LATITUDE AS LAT2,
						LONGITUDE AS LONG2
					FROM WEATHER) W2 ON T1.DAY_VAL = W1.DAY_VAL
AND T1.MAX_TEMP = W2.TE2
ORDER BY DAY_VAL
"""


# QUERY LISTS
create_table_queries = [
    cities_table_create,
    weather_table_create
]

drop_table_queries = [
    cities_table_drop,
    weather_table_drop
]

Truncate_tables  = """
Truncate table cities;
"""

Insert_statment=[
    cities_table_insert,
    weather_table_insert
]

select_statment=[
    Cities_select,
    dataset1_select_query,
    dataset2_select_query
]