# Cost of Living Projections


## Introduction

I do not like negotiating for salary. Especially, without valid projections to determine a range.  

I prepared this report to estimate a salary expectation that will maintain my current standard of living.  

I present two Monte Carlo models of Houston and NYC annual living costs.  The data is somewhat dated and --particularly in the case of houston-- are high level estimates. 

In order to produce a better report, I am currently scraping data from the internet for more accurate sample distributions.  I will be able to present that soon.

With that said, the model should not deviate by more than about 5-10 percent from what is presented in below.  


## Findings

An annual salary of $90,000 would be sufficient to qualify for rent in Houston and most likely the median level income neighbors of NYC.  

I came about this number by quantifying a confidence inverval of annual rent costs in boths cities across a normal distribution.  I then simply multiplied that number by 3 in order to meet the lease qualifications of most landlords.  


## Limitations of the Model

### Old Nyc Data

The data I am using was sourced from 2018.   I will be updating it soon.  

### Houston Data 

The houston estimate is based an estimate to stay in the property I am currently staying in.  The rent is 2400 a month.  I estimated that it could raise at maximum to about 2600 in the next year.  If I were to move similiar housing goes for around 2200 to about 2600 a month. I used these as the bounds of my estimates


## Houston Cost of Living Expenses

I intend to stay in Houston for the next year.  I would like to move to NY eventually to be nearer to a central office, but not in the near future.  


```python
lower_bound = int(2400)
upper_bound = int(2600)

median = 2500
standard_dev = 100  #file:///Users/jnapolitano/Downloads/LNG_Shipping_a_Descriptive_Analysis.pdf

cap_range = range(lower_bound, upper_bound)

rent_distribution = np.random.normal(loc=median , scale=standard_dev, size=10000)

rent_sample = choice(rent_distribution,12)
```

### Houston Monthly food costs



```python
lower_bound = int(300)
upper_bound = int(500)

median = 400
standard_dev = 50 

food_range = range(lower_bound, upper_bound)

food_distribution = np.random.normal(loc=median , scale=standard_dev, size=10000)

food_sample = choice(food_distribution, 12)
```

### Houston Insurance Costs



```python
lower_bound = int(200)
upper_bound = int(300)

median = 250
standard_dev = 25

insurance_range = range(lower_bound, upper_bound)

insurance_distribution = np.random.normal(loc=median , scale=standard_dev, size=10000)

```

#### The Houston Cost of Living DF


```python
cost_of_living_df = pd.DataFrame()
cost_of_living_df['rent']= choice(rent_distribution,12)
cost_of_living_df['food'] = choice(food_distribution, 12)
cost_of_living_df['insurance'] = choice(insurance_distribution, 12)
cost_of_living_df['monthly_cost'] = cost_of_living_df.rent + cost_of_living_df.food + cost_of_living_df.insurance
cost_of_living_df
```




<div style="overflow-x:auto;">
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>rent</th>
      <th>food</th>
      <th>insurance</th>
      <th>monthly_cost</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2472.688851</td>
      <td>334.419350</td>
      <td>231.162225</td>
      <td>3038.270426</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2399.284893</td>
      <td>444.677340</td>
      <td>248.645107</td>
      <td>3092.607340</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2684.456976</td>
      <td>430.277801</td>
      <td>252.578613</td>
      <td>3367.313390</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2478.390464</td>
      <td>360.661703</td>
      <td>291.989836</td>
      <td>3131.042002</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2513.324309</td>
      <td>429.771020</td>
      <td>252.866861</td>
      <td>3195.962190</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2501.390892</td>
      <td>413.121444</td>
      <td>243.717854</td>
      <td>3158.230190</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2554.433859</td>
      <td>363.994333</td>
      <td>226.672435</td>
      <td>3145.100627</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2530.369935</td>
      <td>299.997467</td>
      <td>239.663510</td>
      <td>3070.030911</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2635.681318</td>
      <td>394.667441</td>
      <td>241.502045</td>
      <td>3271.850803</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2596.457738</td>
      <td>513.944623</td>
      <td>229.362551</td>
      <td>3339.764912</td>
    </tr>
    <tr>
      <th>10</th>
      <td>2455.017883</td>
      <td>371.266360</td>
      <td>283.637179</td>
      <td>3109.921421</td>
    </tr>
    <tr>
      <th>11</th>
      <td>2427.449703</td>
      <td>485.960065</td>
      <td>276.488430</td>
      <td>3189.898198</td>
    </tr>
  </tbody>
</table>
</div>



## Houston Costs Per Annum Algorithm

The algorithm below calculates the annual cost of rent, food, and insurance to determine total cost per year.  Rent, food, and insurance are set by random choice based on the distributions defined in the functions above.  

I run the simulation 10,000 times which in theory corresponds to 10,000 random samples of annual costs.  The point in doing this is to create a random normal distribution to define convidence intervals of my total annual costs.  


```python

years = 10000
year_counter = 0
#carbon_total_millions_metric_tons = 300000000
#total_tons_shipped = 0
total_price = 0
cycle_price_samples = np.zeros(shape=years)
cycle_rent_samples = np.zeros(shape=years)
cycle_food_samples = np.zeros(shape=years)
cycle_insurance_samples = np.zeros(shape=years)
annual_cost = 0


for year in range(years):
    # Define a New DataFrame. It should fall out of scope with each iteration 
    cost_of_living_df = pd.DataFrame()
    #random choice of rent 
    cost_of_living_df['rent']= choice(rent_distribution,12)
    #random choice of food
    cost_of_living_df['food'] = choice(food_distribution, 12)
    #random Choice of Insurance
    cost_of_living_df['insurance'] = choice(insurance_distribution, 12)
    #Random Choice of total annual cost
    cost_of_living_df['monthly_cost'] = cost_of_living_df.rent + cost_of_living_df.food + cost_of_living_df.insurance
    # must use apply to account for multiple 0 conditions.  If i simply vectorized the function across the dataframe in a single call i would assign the the same values each day 
    #calculate cost per day for fun...
    # query all that are = o.  Summate the capacities deduct the total 
    annual_cost = cost_of_living_df['monthly_cost'].sum()
    annual_rent = cost_of_living_df.rent.sum()
    annual_food = cost_of_living_df.food.sum()
    annual_insurance = cost_of_living_df.insurance.sum()
    cycle_price_samples[year] = annual_cost
    cycle_food_samples[year] = annual_food
    cycle_insurance_samples[year] = annual_insurance
    cycle_rent_samples[year] = annual_rent
    #print(carbon_total_millions_metric_tons)
    year_counter = year_counter+1


```

### Houston Prediction Df


```python
prediction_df = pd.DataFrame()
prediction_df['rent'] = cycle_rent_samples
prediction_df['food'] = cycle_food_samples
prediction_df['insurance'] = cycle_insurance_samples
prediction_df['total'] = cycle_price_samples
```


```python
prediction_df.describe()

```




<div style="overflow-x:auto;">
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>rent</th>
      <th>food</th>
      <th>insurance</th>
      <th>total</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>10000.000000</td>
      <td>10000.000000</td>
      <td>10000.000000</td>
      <td>10000.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>30003.016272</td>
      <td>4800.864106</td>
      <td>2997.910667</td>
      <td>37801.791045</td>
    </tr>
    <tr>
      <th>std</th>
      <td>344.473477</td>
      <td>171.736899</td>
      <td>86.991071</td>
      <td>394.976839</td>
    </tr>
    <tr>
      <th>min</th>
      <td>28586.298471</td>
      <td>4159.970425</td>
      <td>2699.038887</td>
      <td>36163.596078</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>29771.562236</td>
      <td>4683.226307</td>
      <td>2940.117598</td>
      <td>37537.005225</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>30003.442289</td>
      <td>4800.664909</td>
      <td>2997.584664</td>
      <td>37797.598919</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>30234.927776</td>
      <td>4915.307716</td>
      <td>3056.853675</td>
      <td>38072.961560</td>
    </tr>
    <tr>
      <th>max</th>
      <td>31370.239418</td>
      <td>5495.020896</td>
      <td>3314.016695</td>
      <td>39469.935965</td>
    </tr>
  </tbody>
</table>
</div>



### Houston Annual Cost Histogram


```python
prediction_df.total.plot.hist(grid=True, bins=20, rwidth=0.9,
                   color='#607c8e')
plt.xlabel('Annual Total Costs Price USD')
plt.ylabel('Frequency')
plt.grid(axis='y', alpha=0.75)
```


    
![png](cost_of_living_monte_carlo_files/cost_of_living_monte_carlo_17_0.png)
    


### Houston: Calculating the Confidence Interval For Total Costs

The data is nearly normal. Greater samples sizes would produce a graph of nearly perfect normality


```python

st.norm.interval(alpha=0.90, loc=np.mean(prediction_df.total), scale=st.sem(prediction_df.total))
```




    (37795.2942543157, 37808.287836034055)



### Houston Annual Rent Histogram



```python
### Annual Cost Histogram Histogram
prediction_df.rent.plot.hist(grid=True, bins=20, rwidth=0.9,
                   color='#607c8e')
plt.title('Annual Rent Cost Distribution ')
plt.xlabel('Annual Rent Costs Price USD')
plt.ylabel('Frequency')
plt.grid(axis='y', alpha=0.75)
```


    
![png](cost_of_living_monte_carlo_files/cost_of_living_monte_carlo_21_0.png)
    


### Houston: Calculating the Confidence Interval For Annual Rent

The data is nearly normal. Greater samples sizes would produce a graph of nearly perfect normality


```python

st.norm.interval(alpha=0.95, loc=np.mean(prediction_df.rent), scale=st.sem(prediction_df.rent))
```




    (29996.264715447538, 30009.767827637417)



## New York Cost of Living Expenses

For the sake of comparison, the New York Expense distributions are calculated below.  I assume that everything but rent will be equivalent to Houston.  A more accurate model would account for insurance, food, and incidental differences.  

I am assuming the rent of a two bedroom apartment.  

The data i am using was scraped from craigslist in 2018.  I will redo it later for 2022 data to get a better model.



```python
nyc_df = pd.read_csv("/Users/jnapolitano/Projects/cost-of-living-projections/nyc-housing.csv", encoding="unicode-escape")
```


```python
#assuiming a two bedroom
nyc_df = nyc_df[nyc_df['Bedrooms']== '2br']
```


```python
nyc_df.describe()
```




<div style="overflow-x:auto;">
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Zipcode</th>
      <th>Price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>2626.000000</td>
      <td>2625.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>10845.203351</td>
      <td>2755.018286</td>
    </tr>
    <tr>
      <th>std</th>
      <td>556.758722</td>
      <td>7465.827048</td>
    </tr>
    <tr>
      <th>min</th>
      <td>10001.000000</td>
      <td>16.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>10065.000000</td>
      <td>1950.000000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>11210.000000</td>
      <td>2330.000000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>11231.000000</td>
      <td>2922.000000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>11697.000000</td>
      <td>378888.000000</td>
    </tr>
  </tbody>
</table>
</div>



The price is about 2800 with a std of 7,465.  Which is absurd.  To do a better analysis, I need to clean the data. 


```python

idx = (nyc_df.Price > 500) & (nyc_df.Price < 4500)
nyc_df = nyc_df[idx]
```


```python
nyc_df.describe()
```




<div style="overflow-x:auto;">
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Zipcode</th>
      <th>Price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>2441.000000</td>
      <td>2441.00000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>10881.331422</td>
      <td>2435.25891</td>
    </tr>
    <tr>
      <th>std</th>
      <td>541.102216</td>
      <td>728.96291</td>
    </tr>
    <tr>
      <th>min</th>
      <td>10001.000000</td>
      <td>600.00000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>10302.000000</td>
      <td>1950.00000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>11211.000000</td>
      <td>2300.00000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>11233.000000</td>
      <td>2750.00000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>11697.000000</td>
      <td>4495.00000</td>
    </tr>
  </tbody>
</table>
</div>



When accounting for outliers the data is far more managable.  I'm surprised by the mean price.  Again this data is old, but it is also does not accout for neighborhoods.  I will redo the analysis at a later data filtered by neighborhoods.

### Creating the NYC Distributions 


```python
lower_bound = int(600)
upper_bound = int(4500)

median = 2435
standard_dev = 729 

cap_range = range(lower_bound, upper_bound)

rent_distribution = np.random.normal(loc=median , scale=standard_dev, size=10000)

rent_sample = choice(rent_distribution,12)
```

### NYC Monthly food costs



```python
lower_bound = int(300)
upper_bound = int(500)

median = 400
standard_dev = 50 

food_range = range(lower_bound, upper_bound)

food_distribution = np.random.normal(loc=median , scale=standard_dev, size=10000)

food_sample = choice(food_distribution, 12)
```

### NYC Insurance Costs



```python
lower_bound = int(200)
upper_bound = int(300)

median = 250
standard_dev = 25

insurance_range = range(lower_bound, upper_bound)

insurance_distribution = np.random.normal(loc=median , scale=standard_dev, size=10000)

```

#### NYC Cost of Living Distribution


```python
cost_of_living_df = pd.DataFrame()
cost_of_living_df['rent']= choice(rent_distribution,12)
cost_of_living_df['food'] = choice(food_distribution, 12)
cost_of_living_df['insurance'] = choice(insurance_distribution, 12)
cost_of_living_df['monthly_cost'] = cost_of_living_df.rent + cost_of_living_df.food + cost_of_living_df.insurance
cost_of_living_df
```




<div style="overflow-x:auto;">
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>rent</th>
      <th>food</th>
      <th>insurance</th>
      <th>monthly_cost</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2440.594149</td>
      <td>404.104193</td>
      <td>263.802114</td>
      <td>3108.500457</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3509.157666</td>
      <td>399.234822</td>
      <td>206.641152</td>
      <td>4115.033640</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3351.649621</td>
      <td>297.314475</td>
      <td>284.177204</td>
      <td>3933.141300</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1977.607960</td>
      <td>359.872656</td>
      <td>255.831381</td>
      <td>2593.311996</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2169.224724</td>
      <td>386.271512</td>
      <td>244.469415</td>
      <td>2799.965652</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2661.843885</td>
      <td>356.660878</td>
      <td>218.425732</td>
      <td>3236.930495</td>
    </tr>
    <tr>
      <th>6</th>
      <td>3595.833071</td>
      <td>385.012912</td>
      <td>273.882653</td>
      <td>4254.728637</td>
    </tr>
    <tr>
      <th>7</th>
      <td>1765.419028</td>
      <td>404.770447</td>
      <td>236.665360</td>
      <td>2406.854835</td>
    </tr>
    <tr>
      <th>8</th>
      <td>1708.955308</td>
      <td>348.178355</td>
      <td>231.690103</td>
      <td>2288.823766</td>
    </tr>
    <tr>
      <th>9</th>
      <td>3227.258413</td>
      <td>392.787025</td>
      <td>252.315570</td>
      <td>3872.361007</td>
    </tr>
    <tr>
      <th>10</th>
      <td>1941.492537</td>
      <td>404.384587</td>
      <td>247.628257</td>
      <td>2593.505381</td>
    </tr>
    <tr>
      <th>11</th>
      <td>2081.218740</td>
      <td>416.678465</td>
      <td>213.204362</td>
      <td>2711.101567</td>
    </tr>
  </tbody>
</table>
</div>



## NYC Costs Per Annum Algorithm

The algorithm below calculates the annual cost of rent, food, and insurance to determine total cost per year.  Rent, food, and insurance are set by random choice based on the distributions defined in the functions above.  

I run the simulation 10,000 times which in theory corresponds to 10,000 random samples of annual costs.  The point in doing this is to create a random normal distribution to define convidence intervals of my total annual costs.  


```python

years = 10000
year_counter = 0
#carbon_total_millions_metric_tons = 300000000
#total_tons_shipped = 0
total_price = 0
cycle_price_samples = np.zeros(shape=years)
cycle_rent_samples = np.zeros(shape=years)
cycle_food_samples = np.zeros(shape=years)
cycle_insurance_samples = np.zeros(shape=years)
annual_cost = 0


for year in range(years):
    # Define a New DataFrame. It should fall out of scope with each iteration 
    cost_of_living_df = pd.DataFrame()
    #random choice of rent 
    cost_of_living_df['rent']= choice(rent_distribution,12)
    #random choice of food
    cost_of_living_df['food'] = choice(food_distribution, 12)
    #random Choice of Insurance
    cost_of_living_df['insurance'] = choice(insurance_distribution, 12)
    #Random Choice of total annual cost
    cost_of_living_df['monthly_cost'] = cost_of_living_df.rent + cost_of_living_df.food + cost_of_living_df.insurance
    # must use apply to account for multiple 0 conditions.  If i simply vectorized the function across the dataframe in a single call i would assign the the same values each day 
    #calculate cost per day for fun...
    # query all that are = o.  Summate the capacities deduct the total 
    annual_cost = cost_of_living_df['monthly_cost'].sum()
    annual_rent = cost_of_living_df.rent.sum()
    annual_food = cost_of_living_df.food.sum()
    annual_insurance = cost_of_living_df.insurance.sum()
    cycle_price_samples[year] = annual_cost
    cycle_food_samples[year] = annual_food
    cycle_insurance_samples[year] = annual_insurance
    cycle_rent_samples[year] = annual_rent
    #print(carbon_total_millions_metric_tons)
    year_counter = year_counter+1


```

### NYC Prediction Df


```python
prediction_df = pd.DataFrame()
prediction_df['rent'] = cycle_rent_samples
prediction_df['food'] = cycle_food_samples
prediction_df['insurance'] = cycle_insurance_samples
prediction_df['total'] = cycle_price_samples
```


```python
prediction_df.describe()

```




<div style="overflow-x:auto;">
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>rent</th>
      <th>food</th>
      <th>insurance</th>
      <th>total</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>10000.000000</td>
      <td>10000.000000</td>
      <td>10000.000000</td>
      <td>10000.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>29219.509691</td>
      <td>4797.809482</td>
      <td>3004.224643</td>
      <td>37021.543816</td>
    </tr>
    <tr>
      <th>std</th>
      <td>2532.300418</td>
      <td>172.673041</td>
      <td>87.221734</td>
      <td>2542.267617</td>
    </tr>
    <tr>
      <th>min</th>
      <td>18744.517281</td>
      <td>4116.639699</td>
      <td>2574.323735</td>
      <td>26447.949901</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>27545.387716</td>
      <td>4678.877662</td>
      <td>2945.270499</td>
      <td>35351.052672</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>29244.878069</td>
      <td>4797.251203</td>
      <td>3005.337764</td>
      <td>37034.425389</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>30915.545611</td>
      <td>4915.266687</td>
      <td>3062.210984</td>
      <td>38722.269645</td>
    </tr>
    <tr>
      <th>max</th>
      <td>38516.336096</td>
      <td>5429.519670</td>
      <td>3327.233629</td>
      <td>46383.324453</td>
    </tr>
  </tbody>
</table>
</div>



### NYC Annual Cost Histogram 


```python
prediction_df.total.plot.hist(grid=True, bins=20, rwidth=0.9,
                   color='#607c8e')
plt.xlabel('Annual Total Costs Price USD')
plt.ylabel('Frequency')
plt.grid(axis='y', alpha=0.75)
```


    
![png](cost_of_living_monte_carlo_files/cost_of_living_monte_carlo_47_0.png)
    


### NYC: Calculating the Confidence Interval For Total Costs

The data is nearly normal. Greater samples sizes would produce a graph of nearly perfect normality


```python

st.norm.interval(alpha=0.90, loc=np.mean(prediction_df.total), scale=st.sem(prediction_df.total))
```




    (36979.727235126586, 37063.36039733022)



### NYC Annual Rent Histogram



```python
### Annual Cost Histogram Histogram
prediction_df.rent.plot.hist(grid=True, bins=20, rwidth=0.9,
                   color='#607c8e')
plt.title('Annual Rent Cost Distribution ')
plt.xlabel('Annual Rent Costs Price USD')
plt.ylabel('Frequency')
plt.grid(axis='y', alpha=0.75)
```


    
![png](cost_of_living_monte_carlo_files/cost_of_living_monte_carlo_51_0.png)
    


### Calculating the Confidence Interval For Annual Rent

The data is nearly normal. Greater samples sizes would produce a graph of nearly perfect normality


```python

st.norm.interval(alpha=0.95, loc=np.mean(prediction_df.rent), scale=st.sem(prediction_df.rent))
```




    (29169.877514702926, 29269.14186706609)



## NYC Closing Remarks 

The rent distribution in NYC with 2018 data is actually nearly comparible to my houston estimate.  An annual salary of 90,000 would permit me to live at about the median level in the city.  I will be redoing this report soon as the data is old.  I am currently scraping data in houston and nyc to produce a better analysis. 

## Imports


```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st
from shapely.geometry import Point
from numpy.random import choice
import warnings

warnings.filterwarnings('ignore')

```
