#!/usr/bin/env python
# coding: utf-8

# # New York City Taxi Fare Data Exploration
# 
# ## Reading Data and First Impressions
# 

# In[1]:


# load some default Python modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('seaborn-whitegrid')
from google.cloud import bigquery
from pprint import pprint
import os
import folium
import geopandas
from datetime import date, datetime
import contextily as cx
import matplotlib.pyplot as plt


# In[2]:


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] ="/Users/jnapolitano/.creds/creds.json"


# ## Querying the Green Cab Data Set.
# 
# The queries below clean the data and prepare it for analysis. 

# ### SQL Import Functions

# In[3]:


def query_big_query(query_string):
    client = bigquery.Client()
    query_job = client.query(query_string)

    results = query_job.result()  # Waits for job to complete.
    return results


# In[4]:


def clean_up_data():

  query_string = """
      SELECT 
      t.*,
      FROM
      (
      SELECT *,
      TIMESTAMP_DIFF(dropoff_datetime,pickup_datetime,SECOND) as time_duration_in_secs,
      TIMESTAMP_DIFF(dropoff_datetime,pickup_datetime,MINUTE) as time_duration_in_mins,
      ROUND(trip_distance/TIMESTAMP_DIFF(dropoff_datetime,pickup_datetime,SECOND),2)*3600 as driving_speed_miles_per_hour,
      (CASE WHEN total_amount=0 THEN 0
      ELSE ROUND(tip_amount*100/total_amount,2) END) as tip_rate,
      EXTRACT(YEAR from pickup_datetime) as pickup_year,
      EXTRACT(MONTH from pickup_datetime) as pickup_month,
      CONCAT(CAST(EXTRACT(YEAR from pickup_datetime) as STRING),"-",CAST(EXTRACT(MONTH from pickup_datetime) AS STRING)) as pickup_yearmonth,
      EXTRACT(DATE from pickup_datetime) as pickup_date,
      FORMAT_DATE('%A',DATE(pickup_datetime)) as pickup_weekday_name,
      EXTRACT(HOUR from pickup_datetime) as pickup_hour,
      EXTRACT(YEAR from dropoff_datetime) as dropoff_year,
      EXTRACT(MONTH from dropoff_datetime) as dropoff_month,
      CONCAT(CAST(EXTRACT(YEAR from dropoff_datetime) as STRING),"-",CAST(EXTRACT(MONTH from dropoff_datetime) AS STRING)) as dropoff_yearmonth,
      EXTRACT(DATE from dropoff_datetime) as dropoff_date,
      FORMAT_DATE('%A',DATE(dropoff_datetime)) as dropoff_weekday_name,
      EXTRACT(HOUR from dropoff_datetime) as dropoff_hour
      FROM `nyc-tlc.green.trips_2015`
      /* filter by latitude & longitude that are within the correct range */
      WHERE 
          ((pickup_latitude BETWEEN -90 AND 90) AND
            (pickup_longitude BETWEEN -180 AND 180)) 
            AND
              ((dropoff_latitude BETWEEN -90 AND 90) AND
              (dropoff_longitude BETWEEN -180 AND 180))
      ) t
      WHERE 
      pickup_datetime BETWEEN '2015-01-01' AND '2016-12-31' 
      AND dropoff_datetime BETWEEN '2015-01-01' AND '2016-12-31'
      AND TIMESTAMP_DIFF(dropoff_datetime,pickup_datetime,SECOND) > 0
      AND passenger_count > 0
      AND trip_distance >= 0 
      AND tip_amount >= 0 
      AND tolls_amount >= 0 
      AND mta_tax >= 0 
      AND fare_amount >= 0
      AND total_amount >= 0
      order by pickup_date DESC
      limit 1000000
      """


  result = query_big_query(query_string)
      
  return result.to_dataframe()

clean_df = clean_up_data()


# In[5]:


# read data in pandas dataframe


# list first few rows (datapoints)
clean_df.head()


# In[6]:


# check datatypes
clean_df.dtypes


# In[7]:


# check statistics of the features
clean_df.describe()


# Checking for negative values and anything else I missed from the initial sql clean:

# In[8]:


print('Old size: %d' % len(clean_df))
clean_df = clean_df[clean_df.fare_amount>=0]
print('New size: %d' % len(clean_df))


# No negative values reported.

# In[9]:


# plot histogram of fare
clean_df[clean_df.fare_amount<100].fare_amount.hist(bins=100, figsize=(14,3))
plt.xlabel('fare $USD')
plt.title('Histogram');


# In the histogram of the `fare_amount` there are some small spikes between \$40 and \$55. This could indicate some fixed fare price (e.g. to/from airport). This will be explored further.
# 
# Also the graph is unusually not biased towards the right.  The minimum rate must reduce the possibility of a normal distribution.  

# ## Remove missing data
# 
# Always check to see if there is missing data. As this dataset is huge, removing datapoints with missing data probably has no effect on the models beings trained.

# In[10]:


print(clean_df.isnull().sum())


# The only data points with null are thee ehail_fees.  It is negative a cross every data point.  I'l just drop the column

# In[11]:


print('Old size: %d' % (clean_df.size))
clean_df= clean_df.loc[:, clean_df.columns != "ehail_fee"]
print('New size: %d' % (clean_df.size))


# ## Location data
# 
# As we're dealing with location data, I want to plot the coordinates on a map. This gives a better view of the data. For this, I use the following website:
# 
# 
# New York city coordinates are (https://www.travelmath.com/cities/New+York,+NY):
# 
# - longitude = -74.0063889
# - lattitude = 40.7141667
# 
# I define a bounding box of interest by [long_min, long_max, latt_min, latt_max] using the minimum and maximum coordinates from the testset. 
# 

# In[12]:


# minimum and maximum longitude test set
min(clean_df.pickup_longitude.min(), clean_df.dropoff_longitude.min()), \
max(clean_df.pickup_longitude.max(), clean_df.dropoff_longitude.max())


# In[13]:


# minimum and maximum latitude test
min(clean_df.pickup_latitude.min(), clean_df.dropoff_latitude.min()), \
max(clean_df.pickup_latitude.max(), clean_df.dropoff_latitude.max())


# In[14]:


# this function will also be used with the test set below
def select_within_boundingbox(df, BB):
    return (df.pickup_longitude >= BB[0]) & (df.pickup_longitude <= BB[1]) & \
           (df.pickup_latitude >= BB[2]) & (df.pickup_latitude <= BB[3]) & \
           (df.dropoff_longitude >= BB[0]) & (df.dropoff_longitude <= BB[1]) & \
           (df.dropoff_latitude >= BB[2]) & (df.dropoff_latitude <= BB[3])
            
# load image of NYC map
BB = (-74.5, -72.8, 40.5, 41.8)
#nyc_map = plt.imread('https://aiblog.nl/download/nyc_-74.5_-72.8_40.5_41.8.png')

# load extra image to zoom in on NYC
BB_zoom = (-74.3, -73.7, 40.5, 40.9)
#nyc_map_zoom = plt.imread('https://aiblog.nl/download/nyc_-74.3_-73.7_40.5_40.9.png')


# In[15]:


print('Old size: %d' % len(clean_df))
clean_df = clean_df[select_within_boundingbox(clean_df, BB)]
print('New size: %d' % len(clean_df))


# ### Adding a Geometry column to the table

# In[16]:


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


# In[17]:


gdf = geopandas.GeoDataFrame(
    clean_df, geometry=geopandas.points_from_xy(clean_df.pickup_longitude, clean_df.pickup_latitude))


# When using interactie maps, all of the columns within a df must be json seriable to interact with apis.  The code below serializes all of the date columns for plottin.  

# In[18]:


gdf.pickup_datetime = gdf.pickup_datetime.map(json_serial)
gdf.dropoff_datetime = gdf.dropoff_datetime.map(json_serial)
gdf.dropoff_date =  gdf.dropoff_date.map(json_serial)
gdf.pickup_date = gdf.pickup_date.map(json_serial)


# In[19]:


gdf.dtypes


# ### Checking Coordinate System

# In[20]:


#gdf = EPSG:3857
gdf.crs = "EPSG:4236"
gdf = gdf.to_crs(epsg=3857)


# In[21]:


ax = gdf.plot(figsize=(10, 10), alpha=0.5, edgecolor='k', markersize = .01)
cx.add_basemap(ax,)


# 
# ### Datapoint density per sq mile
# 
# 
# A scatterplot of the pickup and dropoff locations gives a quick impression of the density. However, it is more accurate to count the number of datapoints per area to visualize the density. The code below counts pickup and dropoff datapoints per sq miles. This gives a better view on the 'hot spots'.

# In[22]:


# For this plot and further analysis, we need a function to calculate the distance in miles between locations in lon,lat coordinates.
# This function is based on https://stackoverflow.com/questions/27928/
# calculate-distance-between-two-latitude-longitude-points-haversine-formula 
# return distance in miles
def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295 # Pi/180
    a = 0.5 - np.cos((lat2 - lat1) * p)/2 + np.cos(lat1 * p) * np.cos(lat2 * p) * (1 - np.cos((lon2 - lon1) * p)) / 2
    return 0.6213712 * 12742 * np.arcsin(np.sqrt(a)) # 2*R*asin...

# First calculate two arrays with datapoint density per sq mile
n_lon, n_lat = 200, 200 # number of grid bins per longitude, latitude dimension
density_pickup, density_dropoff = np.zeros((n_lat, n_lon)), np.zeros((n_lat, n_lon)) # prepare arrays

# To calculate the number of datapoints in a grid area, the numpy.digitize() function is used. 
# This function needs an array with the (location) bins for counting the number of datapoints
# per bin.
bins_lon = np.zeros(n_lon+1) # bin
bins_lat = np.zeros(n_lat+1) # bin
delta_lon = (BB[1]-BB[0]) / n_lon # bin longutide width
delta_lat = (BB[3]-BB[2]) / n_lat # bin latitude height
bin_width_miles = distance(BB[2], BB[1], BB[2], BB[0]) / n_lon # bin width in miles
bin_height_miles = distance(BB[3], BB[0], BB[2], BB[0]) / n_lat # bin height in miles
for i in range(n_lon+1):
    bins_lon[i] = BB[0] + i * delta_lon
for j in range(n_lat+1):
    bins_lat[j] = BB[2] + j * delta_lat
    
# Digitize per longitude, latitude dimension
inds_pickup_lon = np.digitize(clean_df.pickup_longitude, bins_lon)
inds_pickup_lat = np.digitize(clean_df.pickup_latitude, bins_lat)
inds_dropoff_lon = np.digitize(clean_df.dropoff_longitude, bins_lon)
inds_dropoff_lat = np.digitize(clean_df.dropoff_latitude, bins_lat)

# Count per grid bin
# note: as the density_pickup will be displayed as image, the first index is the y-direction, 
#       the second index is the x-direction. Also, the y-direction needs to be reversed for
#       properly displaying (therefore the (n_lat-j) term)
dxdy = bin_width_miles * bin_height_miles
for i in range(n_lon):
    for j in range(n_lat):
        density_pickup[j, i] = np.sum((inds_pickup_lon==i+1) & (inds_pickup_lat==(n_lat-j))) / dxdy
        density_dropoff[j, i] = np.sum((inds_dropoff_lon==i+1) & (inds_dropoff_lat==(n_lat-j))) / dxdy


# In[23]:


# Plot the density arrays
fig, axs = plt.subplots(2, 1, figsize=(18, 24))
#axs[0].imshow(nyc_map, zorder=0, extent=BB);
im = axs[0].imshow(np.log1p(density_pickup), zorder=1, extent=BB, alpha=0.6, cmap='plasma')
axs[0].set_title('Pickup density [datapoints per sq mile]')
cbar = fig.colorbar(im, ax=axs[0])
cbar.set_label('log(1 + #datapoints per sq mile)', rotation=270)
cx.add_basemap(axs[0],crs=4236)

#axs[1].imshow(nyc_map, zorder=0, extent=BB);
im = axs[1].imshow(np.log1p(density_dropoff), zorder=1, extent=BB, alpha=0.6, cmap='plasma')
cx.add_basemap(axs[1],crs=4236)
axs[1].set_title('Dropoff density [datapoints per sq mile]')
cbar = fig.colorbar(im, ax=axs[1])
cbar.set_label('log(1 + #datapoints per sq mile)', rotation=270)


# These plots clearly show that the dropoff datapoints concentrate around Manhatten and the three airports (JFK, EWS, LGR).
# 
# Pickup locations are typically in the boroughs.

# ## Pickup traffic density
# 

# In[24]:


# add time information
labels = {'monday' : 0, 'tuesday' : 1, 'wednesday' : 2, 'thursday' : 3, 'friday' : 4, 'saturday' : 5, 'sunday' : 6}
gdf['pickup_weekday_name_test'] = gdf["pickup_weekday_name"]
gdf.pickup_weekday_name = gdf['pickup_weekday_name'].apply(str.lower)
gdf.dropoff_weekday_name = gdf['dropoff_weekday_name'].apply(str.lower)

gdf['pickup_codes'] = gdf.pickup_weekday_name.map(labels)
gdf['dropoff_codes'] = gdf.dropoff_weekday_name.map(labels)


# In[25]:


# some constants needed to calculate pickup traffic density
n_hours = 24
n_weekdays = 7
n_years = 7
n_bins_lon = 30
n_bins_lat = 30


BB_traffic = (-74.5, -72.8, 40.5, 41.8)

# define function to calculate pickup traffic density
def calculate_trafic_density(df):
    traffic = np.zeros((n_years, n_weekdays, n_hours, n_bins_lat, n_bins_lon))
    
    # To calculate the number of datapoints in a grid area, the numpy.digitize() function is used. 
    # This function needs an array with the (location) bins for counting the number of datapoints
    # per bin.
    bins_lon = np.zeros(n_bins_lon+1) # bin
    bins_lat = np.zeros(n_bins_lat+1) # bin
    
    delta_lon = (BB_traffic[1]-BB_traffic[0]) / n_bins_lon # bin longutide width
    delta_lat = (BB_traffic[3]-BB_traffic[2]) / n_bins_lat # bin latitude height
    
    for i in range(n_bins_lon+1):
        bins_lon[i] = BB_traffic[0] + i * delta_lon
    for j in range(n_bins_lat+1):
        bins_lat[j] = BB_traffic[2] + j * delta_lat
    
    # Count per grid bin
    # note: as the density_pickup will be displayed as image, the first index is the y-direction, 
    #       the second index is the x-direction. Also, the y-direction needs to be reversed for
    #       properly displaying (therefore the (n_lat-j) term)
    for y in range(n_years):
        for d in range(n_weekdays):
            for h in range(n_hours):
                idx = (pd.to_numeric(df.pickup_year)==(2009+y)) & (df.pickup_codes==d) & (pd.to_numeric(df.pickup_hour)==h)

                # Digitize per longitude, latitude dimension
                inds_pickup_lon = np.digitize(df[idx].pickup_longitude, bins_lon)
                inds_pickup_lat = np.digitize(df[idx].pickup_latitude, bins_lat)

                for i in range(n_bins_lon):
                    for j in range(n_bins_lat):
                        traffic[y, d, h, j, i] = traffic[y, d, h, j, i] + \
                                                 np.sum((inds_pickup_lon==i+1) & (inds_pickup_lat==j+1))
    
    return traffic 

# define function to plot pickup traffic density
def plot_traffic(traffic, y, d):
    days = {'monday' : 0, 'tuesday' : 1, 'wednesday' : 2, 'thursday' : 3, 'friday' : 4, 'saturday' : 5, 'sunday' : 6}
    fig, axs = plt.subplots(3,8,figsize=(18,7))
    axs = axs.ravel()
    for h in range(24):
        axs[h].imshow(traffic[y-2009,days[d],h,::-1,:], zorder=1, cmap='coolwarm', clim=(0, traffic.max()))
        axs[h].get_xaxis().set_visible(False)
        axs[h].get_yaxis().set_visible(False)
        axs[h].set_title('h={}'.format(h))
        #cx.add_basemap(axs[h],crs=4236)
        
    fig.suptitle("Pickup traffic density, year={}, day={} (max_pickups={})".format(y, d, traffic.max()))


# Now, let's calculate the density and visualize the plots. 
# 
# NOTE: the quality of the plots depends on the number of datapoints used. This dataset used around a million datapoints.

# In[26]:


traffic = calculate_trafic_density(gdf)


# In[27]:


plot_traffic(traffic, 2015, 'monday')
plot_traffic(traffic, 2015, 'friday')
plot_traffic(traffic, 2015, 'sunday')


# ## Distance and time visualisations
# 
# Before building a model I want to test some basic 'intuition':
# 
# - The longer the distance between pickup and dropoff location, the higher the fare.
# - Some trips, like to/from an airport, are fixed fee. 
# - Fare at night is different from day time.
# 
# So, let's check.

# ### The longer the distance between pickup and dropoff location, the higher the fare
# 
# To visualize the distance - fare relation we need to calculate the distance of a trip first. 

# In[28]:


# add new column to dataframe with distance in miles
gdf.trip_distance.hist(bins=50, figsize=(12,4))
plt.xlabel('distance miles')
plt.title('Histogram ride distances in miles')
gdf.trip_distance.describe()


# It seems that most rides are just short rides, with a small peak at ~3 miles.
# Let's also see the influence of `passenger_count`.

# In[29]:


gdf.groupby(['passenger_count','trip_distance', 'fare_amount']).mean()


# Instead of looking to the `fare_amount` using the 'fare per mile' also provides some insights.

# In[30]:


print("Average $USD/Mile : {:0.2f}".format(gdf.fare_amount.sum()/gdf.trip_distance.sum()))


# In[31]:


# scatter plot distance - fare
fig, axs = plt.subplots(1, 2, figsize=(16,6))
axs[0].scatter(gdf.trip_distance, gdf.fare_amount, alpha=0.2)
axs[0].set_xlabel('distance mile')
axs[0].set_ylabel('fare $USD')
axs[0].set_title('All data')

# zoom in on part of data
idx = (gdf.trip_distance < 15) & (gdf.fare_amount < 100)
axs[1].scatter(gdf[idx].trip_distance, gdf[idx].fare_amount, alpha=0.2)
axs[1].set_xlabel('distance mile')
axs[1].set_ylabel('fare $USD')
axs[1].set_title('Zoom in on distance < 15 mile, fare < $100');


# From this plot we notice:
# 
# - There are trips with zero distance but with a non-zero fare. Could this be trips from and to the same location?  They may also be due to cabbies not reporting distance but reporting a fare.  
# - There are some trips with >25 miles travel distance but low fare. 
# - The horizontal lines in the right plot might indicate again the fixed fare trips/
# - Overall there seems to be a (linear) relation between distance and fare with an average rate of +/- 100/20 = 4 \$USD/mile.
# 

# In[32]:


# remove datapoints with distance <0.05 milesf
idx = (gdf.trip_distance >= 0.05)
print('Old size: %d' % len(gdf))
gdf = gdf[idx]
print('New size: %d' % len(gdf))


# ## Some trips, like to/from an airport, are fixed fee
# 
# Another way to explore this data is to check trips to/from well known places. E.g. a trip to JFK airport. Depending on the distance, a trip to an airport is often a fixed price. Let's see.

# In[33]:


# JFK airport coordinates, see https://www.travelmath.com/airport/JFK
jfk = (-73.7822222222, 40.6441666667)
nyc = (-74.0063889, 40.7141667)

def plot_location_fare(loc, name, range=1.5):
    # select all datapoints with dropoff location within range of airport
    fig, axs = plt.subplots(1, 2, figsize=(14, 5))
    idx = (distance(gdf.pickup_latitude, gdf.pickup_longitude, loc[1], loc[0]) < range)
    gdf[idx].fare_amount.hist(bins=100, ax=axs[0])
    axs[0].set_xlabel('fare $USD')
    axs[0].set_title('Histogram pickup location within {} miles of {}'.format(range, name))

    idx = (distance(gdf.dropoff_latitude, gdf.dropoff_longitude, loc[1], loc[0]) < range)
    gdf[idx].fare_amount.hist(bins=100, ax=axs[1])
    axs[1].set_xlabel('fare $USD')
    axs[1].set_title('Histogram dropoff location within {} miles of {}'.format(range, name))
    
plot_location_fare(jfk, 'JFK Airport')


# The majority of rides seem to be going to the airport in this set.  The price is probably fxed around 55-60 dollars.  The price from the airport to manhattan is probably around 25-27 dollars.  

# In[34]:


ewr = (-74.175, 40.69) # Newark Liberty International Airport, see https://www.travelmath.com/airport/EWR
lgr = (-73.87, 40.77) # LaGuardia Airport, see https://www.travelmath.com/airport/LGA
plot_location_fare(ewr, 'Newark Airport')
plot_location_fare(lgr, 'LaGuardia Airport')


# Trips from newark are rare.  Trips to newark are occasional.  Laguardia pickpus and dropoff rates are nearly identical.  Interestingly there are more dropoffs to the airport.  The rate is fairly normal with shifting fares it seems according to distance.

# ## Fare Per Mile

# In[35]:


# Lambda ensure that memory issues do not arise from improperly copying. It takes forever though.  I could probaly vectorize the function. 

gdf['fare_per_mile'] = gdf.apply(lambda x: x.fare_amount/x.trip_distance, axis = 1)
gdf.fare_per_mile.describe()


# In[36]:


idx = (gdf.trip_distance < 3) & (gdf.fare_amount < 100)
plt.scatter(gdf[idx].trip_distance, gdf[idx].fare_per_mile)
plt.xlabel('distance mile')
plt.ylabel('fare per distance mile')

# theta here is estimated by hand
theta = (16, 4.0)
x = np.linspace(0.1, 3, 50)
plt.plot(x, theta[0]/x + theta[1], '--', c='r', lw=2);


# There is a large spread at low distances. Probably due to slow traffic.  There is also some values reported as high as 1400.  I assume this is due to cabbies padding and cleaning their earnings.

# Let's continue with the time vs fare per distance analysis. Next we use a pandas pivot table to calculate a summary and to plot them.

# In[37]:


# display pivot table
gdf.pivot_table('fare_per_mile', index='pickup_hour', columns='pickup_year').plot(figsize=(14,6))
plt.ylabel('Fare $USD / mile')


# It can be clearly seen that the fare $USD/mile varies over the hour. 

# A more in-depth analysis of the fare / time dependency is illustrated below. Here, I calculate per year and per hour the fare and do a linear regression.

# In[38]:


from sklearn.linear_model import LinearRegression

# plot all years
for year in gdf.pickup_year.unique():
    # create figure
    fig, axs = plt.subplots(4, 6, figsize=(18, 10))
    axs = axs.ravel()
    
    # plot for all hours
    for h in range(24):
        idx = (gdf.trip_distance < 15) & (gdf.fare_amount < 100) & (gdf.pickup_hour == h) & \
              (gdf.pickup_year == year)
        axs[h].scatter(gdf[idx].pickup_hour, gdf[idx].fare_amount, alpha=0.2, s=1)
        axs[h].set_xlabel('distance miles')
        axs[h].set_ylabel('fare $USD')
        axs[h].set_xlim((0, 15))
        axs[h].set_ylim((0, 70))

        model = LinearRegression(fit_intercept=False)
        x, y = gdf[idx].trip_distance.values.reshape(-1,1), gdf[idx].fare_amount.values.reshape(-1,1)
        X = np.concatenate((np.ones(x.shape), x), axis=1)
        model.fit(X, y)
        xx = np.linspace(0.1, 25, 100)
        axs[h].plot(xx, model.coef_[0][0] + xx * model.coef_[0][1], '--', c='r', lw=2)
        axs[h].set_title('hour = {}, theta=({:0.2f},{:0.2f})'.format(h, model.coef_[0][0], model.coef_[0][1]))

    plt.suptitle("Year = {}".format(year))
    plt.tight_layout(rect=[0, 0, 1, 0.95])


# ## Fare varies with pickup location
# 
# To visualize whether the fare per km varies with the location the distance to the center of New York is calculated. 

# In[39]:


# add new column to dataframe with distance in mile
gdf['distance_to_center'] = distance(nyc[1], nyc[0], gdf.pickup_latitude, gdf.pickup_longitude)


# Plotting the distance to NYC center vs distance of the trip vs the fare amount gives some insight in this complex relation. 

# In[40]:


fig, axs = plt.subplots(1, 2, figsize=(16,6))
im = axs[0].scatter(gdf.distance_to_center, gdf.trip_distance, c=np.clip(gdf.fare_amount, 0, 100), 
                     cmap='viridis', alpha=1.0, s=1)
axs[0].set_xlabel('pickup distance from NYC center')
axs[0].set_ylabel('distance miles')
axs[0].set_title('All data')
cbar = fig.colorbar(im, ax=axs[0])
cbar.ax.set_ylabel('fare_amount', rotation=270)

idx = (gdf.distance_to_center < 15) & (gdf.trip_distance < 35)
im = axs[1].scatter(gdf[idx].distance_to_center, gdf[idx].trip_distance, 
                     c=np.clip(gdf[idx].fare_amount, 0, 100), cmap='viridis', alpha=1.0, s=1)
axs[1].set_xlabel('pickup distance from NYC center')
axs[1].set_ylabel('distance miles')
axs[1].set_title('Zoom in')
cbar = fig.colorbar(im, ax=axs[1])
cbar.ax.set_ylabel('fare_amount', rotation=270);


# There are a lot of 'green' dots, which is about \$50 to \$60 fare amount near 13 miles distance of NYC center of distrance of trip. This could be due to trips from/to JFK airport. Let's remove them to see what we're left with.

# In[41]:


gdf['pickup_distance_to_jfk'] = distance(jfk[1], jfk[0], gdf.pickup_latitude, gdf.pickup_longitude)
gdf['dropoff_distance_to_jfk'] = distance(jfk[1], jfk[0], gdf.dropoff_latitude, gdf.dropoff_longitude)


# In[42]:


# remove all to/from JFK trips
idx = ~((gdf.pickup_distance_to_jfk < 1) | (gdf.dropoff_distance_to_jfk < 1))

fig, axs = plt.subplots(1, 2, figsize=(16,6))
im = axs[0].scatter(gdf[idx].distance_to_center, gdf[idx].trip_distance, 
                    c=np.clip(gdf[idx].fare_amount, 0, 100), 
                     cmap='viridis', alpha=1.0, s=1)
axs[0].set_xlabel('pickup distance from NYC center')
axs[0].set_ylabel('distance miles')
axs[0].set_title('All data')
cbar = fig.colorbar(im, ax=axs[0])
cbar.ax.set_ylabel('fare_amount', rotation=270)

idx1 = idx & (gdf.distance_to_center < 15) & (gdf.trip_distance < 35)
im = axs[1].scatter(gdf[idx1].distance_to_center, gdf[idx1].trip_distance, 
                     c=np.clip(gdf[idx1].fare_amount, 0, 100), cmap='viridis', alpha=1.0, s=1)
axs[1].set_xlabel('pickup distance from NYC center')
axs[1].set_ylabel('distance miles')
axs[1].set_title('Zoom in')
cbar = fig.colorbar(im, ax=axs[1])
cbar.ax.set_ylabel('fare_amount', rotation=270)


# Now there are some 'yellow' dots (fare amount > \$80) left. To understand these datapoints we plot them on the map.

# In[43]:


# Pickup_locations
idx = (gdf.fare_amount>80) & (gdf.trip_distance<35) 
gdf[idx]
ax = gdf.plot(figsize=(10, 10), alpha=0.5, edgecolor='k', markersize = .01)
cx.add_basemap(ax)


# There are a surpsing numbder of data points.  
# I'll remove all of the airports just to see what is left.
# 

# In[44]:


gdf['pickup_distance_to_ewr'] = distance(ewr[1], ewr[0], gdf.pickup_latitude, gdf.pickup_longitude)
gdf['dropoff_distance_to_ewr'] = distance(ewr[1], ewr[0],gdf.dropoff_latitude,gdf.dropoff_longitude)
gdf['pickup_distance_to_lgr'] = distance(lgr[1], lgr[0], gdf.pickup_latitude, gdf.pickup_longitude)
gdf['dropoff_distance_to_lgr'] = distance(lgr[1], lgr[0],gdf.dropoff_latitude,gdf.dropoff_longitude)


# In[45]:


# remove all to/from airport trips
idx = ~((gdf.pickup_distance_to_jfk < 1) | (gdf.dropoff_distance_to_jfk < 1) |
        (gdf.pickup_distance_to_ewr < 1) | (gdf.dropoff_distance_to_ewr < 1) |
        (gdf.pickup_distance_to_lgr < 1) | (gdf.dropoff_distance_to_lgr < 1))

fig, axs = plt.subplots(1, 2, figsize=(16,6))
im = axs[0].scatter(gdf[idx].distance_to_center, gdf[idx].trip_distance, 
                    c=np.clip(gdf[idx].fare_amount, 0, 100), 
                     cmap='viridis', alpha=1.0, s=1)
axs[0].set_xlabel('pickup distance from NYC center')
axs[0].set_ylabel('distance miles')
axs[0].set_title('All data')
cbar = fig.colorbar(im, ax=axs[0])
cbar.ax.set_ylabel('fare_amount', rotation=270)

idx1 = idx & (gdf.distance_to_center < 15) & (gdf.trip_distance < 35)
im = axs[1].scatter(gdf[idx1].distance_to_center, gdf[idx1].trip_distance, 
                     c=np.clip(gdf[idx1].fare_amount, 0, 100), cmap='viridis', alpha=1.0, s=1)
axs[1].set_xlabel('pickup distance from NYC center')
axs[1].set_ylabel('distance miles')
axs[1].set_title('Zoom in')
cbar = fig.colorbar(im, ax=axs[1])
cbar.ax.set_ylabel('fare_amount', rotation=270)


# In[46]:


idx = idx = ~((gdf.pickup_distance_to_jfk < 1) | (gdf.dropoff_distance_to_jfk < 1) |
        (gdf.pickup_distance_to_ewr < 1) | (gdf.dropoff_distance_to_ewr < 1) |
        (gdf.pickup_distance_to_lgr < 1) | (gdf.dropoff_distance_to_lgr < 1))
gdf[idx]
ax = gdf.plot(figsize=(10, 10), alpha=0.5, edgecolor='k', markersize = .01)
cx.add_basemap(ax)


# In[47]:


idx = ~((gdf.pickup_distance_to_jfk < 1) | (gdf.dropoff_distance_to_jfk < 1) |
        (gdf.pickup_distance_to_ewr < 1) | (gdf.dropoff_distance_to_ewr < 1) |
        (gdf.pickup_distance_to_lgr < 1) | (gdf.dropoff_distance_to_lgr < 1))
gdf[idx]


# Removing the to/from airport trips doesn't really change the outcome of the data.  The number of to and from trips within the set are marginal.

# ## Final Thoughts
# 
# Very few of these cabs operatine in Manhattan. I was confused by this. I found that most green cabs operate in the boroughs.  The few number of these going to the center, accounted for such high rates as this is not their typical range of operation. 
# 
