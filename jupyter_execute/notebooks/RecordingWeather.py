#!/usr/bin/env python
# coding: utf-8

# # Question 2a: CSV Solution
# 

# ## The Question
# 
# 2) (a) Let's say you're tasked with using an API to record the weather. Specifically, we want to know the current temperature at our HQ in Los Angeles each day. We want it saved as a CSV file and then loaded into a database. 

# My solution to part is below.  
# 
# You'll find a program that can dynamicaly request data from the openweather api.  It will append data to a csv file per hour before creatinga new one with a name containing the hour from the datetime.  
# 
# When integrating into a db each file could be considered indendently if computing power is minimal.  They may also be aggregated via pyspark or pandas into larger csvs.  I would most likely write an automation script to download data, clean it to whatever schema is necessary for the workload, and then upload the data in batches to a database with the sqlalchemy library.  

# ## Solution A

# In[1]:


import requests, json
from pprint import pprint
from pandas import json_normalize
from flatten_json import flatten_json
from datetime import datetime
import os


# In[2]:


def get_key(key_path):
    with open(key_path, "r") as f:
        key = f.read()
        key = key.rstrip('\n')
        pprint(key)
    return key




# In[3]:


def make_query_string(base_url,lat,long,key):
    lat_string = "lat={}".format(lat)
    long_string = "lon={}".format(long)
    appid_string = "appid={}".format(key)
    query_string = "&".join([lat_string,long_string,appid_string])
    query_string = "?".join([base_url,query_string])
    return query_string



# In[4]:


def make_request(query_string):
    response = requests.get(query_string)
    return response
 


# In[5]:


def make_dict_from_response(response):
    try: 
        return response.json()
    except:
        raise
    


# In[6]:


def flatten_response(response_dict):
    try:
        return flatten_json(response_dict)
    except:
        raise


# In[7]:


def response_to_df(response_dict):
    ## write a test for levels. If dict has more than one than except
    try:
        return json_normalize(response_dict)
    except:
        raise


# In[8]:


def response_to_line(response_dict):
    for key,v in response_dict.items():
        response_dict[key] = str(v)
    value_line = [list(response_dict.values())]
    
    #pprint(keys)
    return value_line



# In[9]:


def add_date_stamp(response_dict):
    response_dict['timestamp'] = stamp = datetime.now().strftime("%Y-%m-%d:%H:%M:%S:%f")
    pprint(stamp)
    return response_dict
    


# In[10]:


def response_df_to_csv(response_df, outpath):
    outpath = outpath + os.sep + response_df['timestamp'][0][:-13] + ".csv"
    #output_path='my_csv.csv'
    response_df.to_csv(outpath, mode='a', header=not os.path.exists(outpath))
    return outpath


# In[11]:


def main():
    outpath = os.getcwd()
    key_path = "/Users/jnapolitano/Projects/pmc-submission/jupyter-book/notebooks/weather_key.txt"
    lat = 34.047470
    long = -118.445950
    key = get_key(key_path)
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    query_string = make_query_string(base_url,lat,long,key)
    pprint(query_string)
    response = make_request(query_string=query_string)
    response_dict = make_dict_from_response(response=response)
    response_dict = flatten_response(response_dict)
    response_dict = add_date_stamp(response_dict)
    response_df = response_to_df(response_dict)
    outfile = response_df_to_csv(response_df,outpath)
    
    


# In[12]:


main()


# 
