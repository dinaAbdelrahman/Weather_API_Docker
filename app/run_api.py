import requests
from requests import exceptions
import time
import pandas as pd
from pandas import DataFrame
import json
from datetime import datetime, timedelta
import ciso8601
from sql_queries import select_statment
from cursors_operations import *
from utilities import get_path


def get_json(num_days,api_key,api_url,cur,conn,staging_path):

    ### Reading the cities data from the database
    cur.execute(select_statment[0])

    #read the query output into a new dataframe
    df_cities = DataFrame(cur.fetchall())
    print("Getting cities data from datase")
    #print(df_cities.head())

    #Calculating the timestamp to use it in the API call
    l=[]
    for i in range(num_days):
        date = datetime.now() - timedelta(i+1)
        date= date.replace(minute=0, hour=0, second=0)
        date=  datetime.strftime(date, '%Y-%m-%d')
        ts = ciso8601.parse_datetime(date)
        # to get time in seconds:
        ts = time.mktime(ts.timetuple())
        l.append(ts)
        #print(date, ts,l)

    #Calculate the directory absolute path to save the files
    json_full_path=get_path(staging_path)

    for row in df_cities.values:
        #print(row)
        for ts in range(len(l)):
            #confirm all keys for API are as required
            #print(row[1],row[2],l[ts])
            print(api_url.format(row[1],row[2],l[ts],api_key).replace("'", ""))
            try:
                response = requests.get((api_url.format(row[1],row[2],int(l[ts]),api_key)).replace("'", ""), timeout=5)
                response.raise_for_status()
                # Code here will only run if the request is successful
                
                # Serializing json 
                json_object = json.dumps(json.loads(response.content))
                
                #write the output to file with timestamp to prevent overwrite
                date = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
                file_name=f"json_output_{date}.json"
                
                json_file_path_name= os.path.join(json_full_path, file_name).replace('\\','/')
                with open(json_file_path_name, "w") as outfile:
                    outfile.write(json_object)
                time.sleep(3)

            except requests.exceptions.HTTPError as errh:
                print("HTTP error has occured")
                print(errh)
            except requests.exceptions.ConnectionError as errc:
                print("Connection error has occured")
                print(errc)
            except requests.exceptions.Timeout as errt:
                print("Request has timeout")
                print(errt)
            except requests.exceptions.RequestException as err:
                print("Request has had an exception")
                print(err)
                exit



    return