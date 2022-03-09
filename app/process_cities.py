import os
import glob
import pandas as pd
import numpy as np
import psycopg2
from geopy.geocoders import Nominatim
from utilities import get_path, get_files
from sql_queries import Insert_statment
from cursors_operations import insert_postgres_table



def process_cities(relative_url,cur,conn):
    """
    input to the function is the relative URL of the CSV file having the desired cities
    I then process the cities using geopy librabry to get their co-ordinate which will be used later in the API calls
    
    """
  
    #construct the file full path OS_path + relative path
    cities_full_path=get_path(relative_url)

    #reading the folder content, here there is only 1 file so will take the first element return by function get_files
    cities_file_name=get_files(cities_full_path)
    cities_file_path= os.path.join(cities_full_path, cities_file_name[0]).replace('\\','/')

    #reading the CSV file
    df_original_cities=pd.read_csv(cities_file_path)
    addresses=df_original_cities['City_Name'].to_list()

    #add the cities coordinates
    geolocator = Nominatim(user_agent="Dina")
    headers_cities=['city_name','latitude','longitude']
    df_cities = pd.DataFrame(columns=headers_cities)

    for address in addresses:
        location = geolocator.geocode(address)
        df_cities=df_cities.append({'city_name': address, 'latitude':location.latitude,'longitude':location.longitude},ignore_index=True)
    
    print(df_cities.head())

    #write df_cities to the database
    insert_postgres_table(df_cities,cur,Insert_statment[0])
    conn.commit()





    return
