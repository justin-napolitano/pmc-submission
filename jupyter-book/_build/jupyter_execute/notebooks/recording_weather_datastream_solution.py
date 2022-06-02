#!/usr/bin/env python
# coding: utf-8

# # Question 2b: Data Streaming Solution via BigTable
# 
# ## Question
# 
# (b) Now, assume we needed to make a similar call, but retrieving information about many locations and much more than just the temperature. Assume it will retrieve 500MB of data a day. Describe any alterations you would want to make to your code, where the code would run each day, where the data would be saved, and which database you'd prefer to store it in.
# 
#  
# 
# 

# ## My Solution
# 
# ### Data Storage
# 
# #### BigTable or Apache Hbase
# 
# Writing to a csv file at scale with asychronous calls is difficult to manage.  File corruption, migrations, and file management are problems that will manifest at scale.
# 
# A BigTable solution reduces the complexity of the data pipeline and ensures that files are never lost or mismanaged.   Instead of writing to a csv, I would prefer to write the data of each request to a big table.  
# 
# According to the workflow I would then migrate that data to a postgresql db for permanent storage.  
# 
# Typically, I would run a google cloud environment to achieve this.  
# 
# #### CSV Method
# 
# If the csv method is the only option available, I would not expose the programs to the internet to avoid asynchronous calls.  I would also limit cpu usage to 1 thread at a time, to avoid file corruption.  
# 
# I would use google cloud compute or a comparible service to run the csv solution code from my solution to 2a. It would take input from a local file containing search cities and intervals.  Each city's data will be stored on individual csv partitioned by the hour at maximum.  
# 
# That data would be store do on the storage solution of the cloud platform.
# 
# Finally, I would migrate the data to a postgresql db (open source-no licensing fees) daily with chron jobs and schema building pyspark scripts.  I could also use also write sql queries to integrate the csv's and to clean the data if the server workload is low.  
# 
# ### Searching for Many Cities
# 
# To search for many cities, I would integrate the code below into a restful framework that passes a city name to the open weather endpoint.  
# 
# It would then pass the result needed to the big-query endpoint detailed in the next section.  
# 
# Finally, I would write another set of programs to run the application.   The service would take input from whatever source the team is most comfortable editing.  For example,  a google sheet with cities and search interva.  The service would make the request via an api to the solution presented below.  
# 
# Each service would be containerized in order to scale at need.  Kubernetes clusters would be orchestrated to meet compute and request demands variable to reduce overall cost cost to the organization. At enterprise scale it would likely be more cost efficient to externalize these processes via the cloud.  Local hardware would be cost prohibitive.  
# 
# 
# ## The Code Below
# 
# The code below is written to take advantage of the bigtable/hbase method.  It will run asynchronously without corrupting csv files. It also forwards the data to a rest api that I wrote to store data on a bigtable.
# 
# For testing, I ran the code below on my local RHEL server. It has succesfully run for three days without error.   With variation to fit the needs of another rest api, the code could be put into production within a week.  
# 
# A django based web app, or preferably a go based rest api could also be produced within about two to three weeks to accomplish enterprise scale data migration. 

# ### Imports

# In[1]:


import requests, json
from pprint import pprint
from pandas import json_normalize
from flatten_json import flatten_json
from datetime import datetime
import os
from ratelimit import limits, RateLimitException, sleep_and_retry
from concurrent.futures import ThreadPoolExecutor as PoolExecutor

ONE_MINUTE = 60
MAX_CALLS_PER_MINUTE = 30


# ### Credentials

# In[2]:


def get_key(key_path):
    with open(key_path, "r") as f:
        key = f.read()
        key = key.rstrip('\n')
        pprint(key)
    return key




# ### Making the Weather Query String

# In[3]:


def make_query_string(base_url,lat,long,key):
    lat_string = "lat={}".format(lat)
    long_string = "lon={}".format(long)
    appid_string = "appid={}".format(key)
    query_string = "&".join([lat_string,long_string,appid_string])
    query_string = "?".join([base_url,query_string])
    return query_string


# ### General Request function
# 

# In[4]:


def make_request(query_string):
    response = requests.get(query_string)
    return response


# ### Parse Json into Dictionary

# In[5]:


def make_dict_from_response(response):
    try: 
        return response.json()
    except:
        raise
    


# ### Add Time Stamp for Unique ID

# In[6]:


def add_date_stamp(response_dict):
    response_dict['timestamp'] = stamp = datetime.now().strftime("%Y-%m-%d:%H:%M:%S:%f")
    pprint(stamp)
    return response_dict
    


# ### Making the Update String to Send to my REST Server
# 
# note that this function could be simplified and made dynamic, but it serves a single purpose in this instance.  

# In[7]:


def make_update_string(response_dict):
    #pprint(response_dict)

    latitude = response_dict['coord']['lat']
    longitude = response_dict['coord']['lon']
    temp = response_dict['main']['temp']
    temp_max = response_dict['main']['temp_max']
    temp_min = response_dict['main']['temp_min']
    humidity = response_dict['main']['humidity']
    pressure = response_dict['main']['pressure']
    feels_like = response_dict['main']['feels_like']
    sunrise = response_dict['sys']['sunrise']
    sunset =  response_dict['sys']['sunset']
    datetime = response_dict['timestamp']
    timezone = response_dict['timezone']
    city_name = response_dict['name']
    city_name = city_name.replace(" ", "")
    city_name = city_name.replace(",", "-")


    base_url = "http://0.0.0.0:8080/weather?"
    lat_str = "lat={}".format(str(latitude))
    long_str = "long={}".format(str(longitude))
    temp_str = "temp={}".format(str(temp))
    temp_max_str = "temp_max={}".format(str(temp_max))
    temp_min_str = "temp_min={}".format(str(temp_min))
    feels_like_str = "feels_like={}".format(str(feels_like))
    humidity_str = "humidity={}".format(str(humidity))
    pressure_str = "pressure={}".format(str(pressure))
    sunrise_str = "sunrise={}".format(str(sunrise))
    sunset_str = "sunset={}".format(str(sunset))
    datetime_str = "datetime={}".format(str(datetime))
    timezone_str = "timezone={}".format(str(timezone))
    city_name_str = "city={}".format(str(city_name))
    
    query_str = "&".join([lat_str,long_str,temp_str, temp_max_str, temp_min_str, feels_like_str, humidity_str, pressure_str,sunrise_str, sunset_str, datetime_str, timezone_str, city_name_str])
    query_str = base_url + query_str
    return query_str
    



# In[8]:


@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
def update_pipeline(count = 0):
    #outpath = os.getcwd()
    key_path = "/Users/jnapolitano/Projects/pmc-submission/jupyter-book/notebooks/weather_key.txt"
    lat = 34.047470
    long = -118.445950
    key = get_key(key_path)
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    query_string = make_query_string(base_url,lat,long,key)
    #pprint(query_string)
    response = make_request(query_string=query_string)
    response_dict = make_dict_from_response(response=response)
    response_dict = add_date_stamp(response_dict)
    update_str = make_update_string(response_dict)
    big_query_response = make_request(update_str)
    pprint(big_query_response)
    pprint(update_str)
    pprint(count)

    ## The Pool Executor is testing for thread safety.  For intance, it is running the update_pipeline 3 times at 3 different rates according
    #the limits set by the ratelimitter.   With an exposed rest api and big table it is in theory possible to query as many times as they're are cpu cores available on the machine.  
    with PoolExecutor(max_workers=3) as executor:
        for _ in executor.map(update_pipeline, range(60)):
            pass 


# ## Main Function
# 

# ```python
# def main():
#     update_pipeline()
# ```
