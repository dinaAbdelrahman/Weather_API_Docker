import os
import pandas as pd
import numpy as np
import psycopg2
from sql_queries import *



def insert_postgres_table(df,cur,statment):
    j=0
    for i, row in df.iterrows():
        items = list(row)
        list1 = [(None,) if str(x)=='nan' else (x,) for x in items]
        #print(list1)
        cur.execute(statment, list1)
        j=j+1
    print("Number of processed rows {}".format(j) )
    return

def Truncate_tables(cur, conn):
    
    cur.execute(Truncate_tables)
    conn.commit()



def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()

def adjust_timezone(cur, conn):
    cur.execute(timezone_adjust)
    conn.commit()