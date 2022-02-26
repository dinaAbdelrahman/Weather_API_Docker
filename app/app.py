import os
import glob
import pandas as pd
import numpy as np
import psycopg2
from sql_queries import *
from utilities import *
from process_cities import process_cities
import configparser
from cursors_operations import *
from run_api import get_json
from process_weather import process_weather_json
from process_dataset import process_dataset

config = configparser.ConfigParser()
config.read('parameters.cfg')

def main():
    """
    This program query and process the data from the Openweather through API:
    https://openweathermap.org/
    The developement was done using Python and processed data was stored in Postgres DB called weather_processing

    Dynamic configurations:
    1. user can add all required cities in the CSV file cities found in location_data folder
    2. user can query history data up to 5 days

    The following workflow explains the program running:
    Part1: the database connection is establised and all tables are created
    Part2: Process the cities and write their coordinate in the database
    Part3: Run the API to get the weather JSON files
    Part4: Contruct the required 2 datasets
    """

    
    ##### Part1 ######

    #connect to PostgresDB
    cur, conn = connect_database()

    #Adjust the database timezone
    adjust_timezone(cur, conn)

    #Option to reset database & drop SQL tables for each new run
    drop_tables(cur, conn)

    #Create all the required SQL tables
    create_tables(cur, conn)

    #Option to reset data: truncate SQL tables (clear only data but keep tables definition)
    #Need to comment drop & create functions before the truncate run
    #Truncate_tables(cur, conn)

    
    ##### Part2 ######

    ## Process the cities and write their coordinate in the database
    cities_relative_url=config['data_path']['location_path']
    process_cities(cities_relative_url,cur,conn)

    
    ##### Part3 ######

    ## Run the API to get the weather JSON files
    num_days=int(config['api']['number_of_days'])
    api_key=config['api']['key_password']
    api_url=config['api']['endpoint']
    staging_path=config['data_path']['staging_path']
    get_json(num_days,api_key,api_url,cur,conn,staging_path)
    

    ##### Part4 ######

    ## Read the JSON files and process it to prepare to be inserted in the database
    json_relative_path=config['data_path']['staging_path']
    process_weather_json(json_relative_path,cur,conn)


    #### Part 5 #####

    ##Contruct the required 2 datasets

    #first Dataset
    dataset1_relative_url=config['data_path']['dataset1_path']
    statment=1
    process_dataset(dataset1_relative_url,cur,conn,statment)

    #Second Dataset
    dataset2_relative_url=config['data_path']['dataset2_path']
    statment=2
    process_dataset(dataset2_relative_url,cur,conn,statment)




if __name__ == "__main__":
    main()