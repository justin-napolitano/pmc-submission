#!/usr/bin/env python
# coding: utf-8

# # Restful Api to Upload Data to a BigTable Instance

# ```Python
# from flask import Flask, request, make_response, jsonify
# import pandas as pd
# import gcsfs
# from google.cloud import bigquery
# from google.oauth2 import service_account
# import pandas_gbq
# import os
# app = Flask(__name__)
# app.config["DEBUG"] = True #If the code is malformed, there will be an error shown when visit app
# @app.route("/weather", methods=["GET"])
# def weather_table_update():
#     
#     latitude = request.args.get('lat', None)
#     longitude = request.args.get('long', None)
#     temp = request.args.get('temp')
#     temp_max = request.args.get('temp_max')
#     temp_min = request.args.get('temp_min')
#     feels_like = request.args.get("feels_like")
#     humidity = request.args.get("humidity")
#     pressure = request.args.get("pressure")
#     sunrise = request.args.get('sunrise', None)
#     sunset = request.args.get('sunset', None)
#     datetime = request.args.get('datetime',None)
#     timezone = request.args.get('timezone',None)
#     city_name = request.args.get('city',None)
# 
#     
# 
# 
#     input_table = {'datetime':[datetime],'timezone': [timezone], 'city_name': [city_name], 'latitude':[latitude], 'longitude': [longitude], "temp": [temp],"feels_like": [feels_like],"temp_max": [temp_max], "temp_min": [temp_min], "humidity": [humidity], "pressure":[pressure], 'sunrise': [sunrise], 'sunset': [sunset]}
#     input_table = pd.DataFrame(input_table)
#     #input_table["datetime"]= input_table["date_time"].map(strdate_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S'))
#     input_table["datetime"] = pd.to_datetime(input_table['datetime'], format="%Y-%m-%d %H:%M:%S:%f")
#     input_table['latitude'] = pd.to_numeric(input_table['latitude'])
#     input_table['longitude'] = pd.to_numeric(input_table['longitude'])
#     input_table['temp'] = pd.to_numeric(input_table['temp'])
#     input_table['temp_max'] = pd.to_numeric(input_table['temp_max'])
#     input_table['temp_min'] = pd.to_numeric(input_table['temp_min'])
#     input_table['humidity'] = pd.to_numeric(input_table['humidity'])
#     input_table['feels_like'] = pd.to_numeric(input_table['feels_like'])
#     input_table['pressure'] = pd.to_numeric(input_table['pressure'])
#     input_table['sunset'] = pd.to_numeric(input_table['sunset'])
#     input_table['sunrise'] = pd.to_numeric(input_table['sunrise'])
#     input_table['timezone'] = pd.to_numeric(input_table['timezone'])
#     #input_table["book_author"]= input_table["book_author"].map(str)
#     
#     #Push table to Google Big Query
#     client = bigquery.Client()
#     project_id = 'pmc-submission-api'
#     table_id = 'Weather.weather_test_api'
#     pandas_gbq.to_gbq(input_table, table_id, project_id=project_id, if_exists='append')
#     
#     return "Table weather_test_api has been Updated"
# ```
