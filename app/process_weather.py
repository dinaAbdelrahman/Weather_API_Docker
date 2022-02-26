import time
import pandas as pd
import os
from pandas import DataFrame
import json
import pytz
from datetime import datetime
from utilities import get_path, get_files
from cursors_operations import insert_postgres_table
from sql_queries import Insert_statment


def convert_timestamp_in_datetime_utc(timestamp_received):
    dt_naive_utc = datetime.utcfromtimestamp(timestamp_received)
    return dt_naive_utc.replace(tzinfo=pytz.utc)


def process_json_file(file,cur,conn,weather_json_full_path):

    json_file_path = os.path.join(weather_json_full_path, file).replace('\\','/')
    
    #define the dataframe to process in it the JSON content
    headers_weather=['latitude','longitude','time_stamp','date_val','month_val','day_val','temperature']
    df_weather = pd.DataFrame(columns=headers_weather)

    with open(json_file_path, 'r') as openfile:
  
        # Reading from json file
        json_object = json.load(openfile)
        lat=json_object['lat']
        lon=json_object['lon']
        for i in range(len(json_object['hourly'])):
            temp=json_object['hourly'][i]['temp']
            ts=json_object['hourly'][i]['dt']
            date=convert_timestamp_in_datetime_utc(ts)
            day=date.strftime('%Y-%m-%d')
            month=date.strftime('%Y-%m')
            df_weather=df_weather.append({'latitude':lat,
                                      'longitude':lon,
                                      'time_stamp':ts,
                                      'date_val':date,
                                      'month_val':month,
                                      'day_val':day,
                                      'temperature':temp},ignore_index=True)

    

    #Writing the dataframe into the database
    insert_postgres_table(df_weather,cur,Insert_statment[1])
    conn.commit()


    return



def process_weather_json(weather_json_path,cur,conn):
    """
    input to the function is the relative URL of the JSON files having the API output
    
    """

    #construct the files full path OS_path + relative path
    weather_json_full_path=get_path(weather_json_path)

    #construct a list of all files inside the folder
    weather_json_files_list=get_files(weather_json_full_path)

    #process json files
    for file in weather_json_files_list:
        print('JSON file {} started processing.'.format(file))
        process_json_file(file,cur,conn,weather_json_full_path)
        conn.commit()
        print('JSON file {} was processed.'.format(file))



    return