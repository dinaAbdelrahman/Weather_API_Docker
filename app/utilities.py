import os
import glob
import pandas as pd
import numpy as np
import configparser
import psycopg2

def get_files(filepath):
    all_files = []
    for root, dirs, files in os.walk(filepath):
        #files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(f)
    
    return all_files



def get_path(relative_url):
    
    #Input files directory configuration

    root = os.getcwd()
    file_path = os.path.join(root, relative_url).replace('\\','/')
    return file_path

def connect_database():
    
    # connect to ookla database
    config = configparser.ConfigParser()
    #reading configuration settings
    config.read('parameters.cfg')
    
    #Database configuration
    [HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT]= config['DB'].values()  
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['DB'].values()))
    cur = conn.cursor()
    
    return cur, conn

