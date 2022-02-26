import os
import glob
import pandas as pd
import numpy as np
from pandas import DataFrame
import psycopg2
from sql_queries import *
from utilities import *
import configparser
from cursors_operations import *
from run_api import get_json
from process_weather import process_weather_json



def process_dataset(dataset_relative_url,cur,conn,statment):

    ### Reading the cities data from the database
    cur.execute(select_statment[statment])

    df_dataset = DataFrame(cur.fetchall())
    print(df_dataset.head())
    filepath = get_path(dataset_relative_url)
    file_name=os.path.join(filepath, 'output.csv').replace('\\','/')
    df_dataset.to_csv(file_name)


    return

