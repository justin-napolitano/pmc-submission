#!/usr/bin/env python
# coding: utf-8

# ### Import Statements

# In[1]:


from google.cloud import bigquery
from pprint import pprint
import os


# ### Utility Big Query Function

# In[2]:


def query_big_query(query_string):
    client = bigquery.Client()
    query_job = client.query(query_string)

    results = query_job.result()  # Waits for job to complete.
    return results


# In[3]:


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/jnapolitano/Projects/pmc-submission/creds.json"


# In[4]:


def marketing_query():

    query_string = """
        SELECT fullVisitorId
        ,COUNT(DISTINCT visitId) AS num_sessions
        ,SUM(totals.pageviews) AS num_pageviews
        ,SUM(totals.hits) AS num_hits
        ,SUM(totals.timeOnSite) AS total_timeonsite
        ,MAX(CASE WHEN trafficSource.medium = '(none)' THEN 1 ELSE 0 END) AS medium_direct
        ,MAX(CASE WHEN trafficSource.medium = 'organic' THEN 1 ELSE 0 END) AS medium_organic
        ,MAX(CASE WHEN trafficSource.medium = 'referral' THEN 1 ELSE 0 END) AS medium_referral
        ,MAX(CASE WHEN trafficSource.medium NOT IN ('(none)', 'organic', 'referral') THEN 1 ELSE 0 END) AS medium_other
        ,MAX(CASE WHEN device.deviceCategory = 'mobile' THEN 1 ELSE 0 END) AS device_mobile
        ,MAX(CASE WHEN device.deviceCategory = 'desktop' THEN 1 ELSE 0 END) AS device_desktop
        ,MAX(CASE WHEN device.deviceCategory = 'tablet' THEN 1 ELSE 0 END) AS device_tablet
        ,SUM(totals.transactions) AS transactions
        FROM `bigquery-public-data.google_analytics_sample.ga_sessions_2017*`
        GROUP BY fullVisitorId
         """
    result = query_big_query(query_string)
    return result.to_dataframe()

df_first_try = marketing_query()


# In[7]:


df_first_try


# In[11]:


file_name = "marketing_data.csv"
cwd = os.getcwd()

outpath = os.sep.join([cwd,file_name])

df_first_try.to_csv(outpath)


# In[ ]:





# In[ ]:




