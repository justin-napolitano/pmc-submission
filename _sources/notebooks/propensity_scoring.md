# Churn Modelling Marketing Data with Julia 

```julia
using Pkg
using DataFrames
using CSV
using Plots
using GLM
using StatsBase
using Lathe
using MLBase
using ClassImbalance
using ROCAnalysis
using PyCall
sklearn = pyimport("sklearn.metrics")
```




    PyObject <module 'sklearn.metrics' from '/Users/jnapolitano/venvs/finance/lib/python3.9/site-packages/sklearn/metrics/__init__.py'>




```julia
function load_csv() 

    df = DataFrame(CSV.File("./Churn_Modelling.csv")) 
    return df 
end
```




    load_csv (generic function with 1 method)



## Loading Data


```julia
marketing_df = load_csv()
first(marketing_df,5)
```




<table class="data-frame"><thead><tr><th></th><th>RowNumber</th><th>CustomerId</th><th>Surname</th><th>CreditScore</th><th>Geography</th><th>Gender</th><th>Age</th><th>Tenure</th></tr><tr><th></th><th>Int64</th><th>Int64</th><th>String31</th><th>Int64</th><th>String7</th><th>String7</th><th>Int64</th><th>Int64</th></tr></thead><tbody><p>5 rows × 14 columns (omitted printing of 6 columns)</p><tr><th>1</th><td>1</td><td>15634602</td><td>Hargrave</td><td>619</td><td>France</td><td>Female</td><td>42</td><td>2</td></tr><tr><th>2</th><td>2</td><td>15647311</td><td>Hill</td><td>608</td><td>Spain</td><td>Female</td><td>41</td><td>1</td></tr><tr><th>3</th><td>3</td><td>15619304</td><td>Onio</td><td>502</td><td>France</td><td>Female</td><td>42</td><td>8</td></tr><tr><th>4</th><td>4</td><td>15701354</td><td>Boni</td><td>699</td><td>France</td><td>Female</td><td>39</td><td>1</td></tr><tr><th>5</th><td>5</td><td>15737888</td><td>Mitchell</td><td>850</td><td>Spain</td><td>Female</td><td>43</td><td>2</td></tr></tbody></table>




```julia
println(size(marketing_df))
describe(marketing_df)
```

    (10000, 14)





<table class="data-frame"><thead><tr><th></th><th>variable</th><th>mean</th><th>min</th><th>median</th><th>max</th><th>nunique</th><th>nmissing</th><th>eltype</th></tr><tr><th></th><th>Symbol</th><th>Union…</th><th>Any</th><th>Union…</th><th>Any</th><th>Union…</th><th>Nothing</th><th>DataType</th></tr></thead><tbody><p>14 rows × 8 columns</p><tr><th>1</th><td>RowNumber</td><td>5000.5</td><td>1</td><td>5000.5</td><td>10000</td><td></td><td></td><td>Int64</td></tr><tr><th>2</th><td>CustomerId</td><td>1.56909e7</td><td>15565701</td><td>1.56907e7</td><td>15815690</td><td></td><td></td><td>Int64</td></tr><tr><th>3</th><td>Surname</td><td></td><td>Abazu</td><td></td><td>Zuyeva</td><td>2932</td><td></td><td>String31</td></tr><tr><th>4</th><td>CreditScore</td><td>650.529</td><td>350</td><td>652.0</td><td>850</td><td></td><td></td><td>Int64</td></tr><tr><th>5</th><td>Geography</td><td></td><td>France</td><td></td><td>Spain</td><td>3</td><td></td><td>String7</td></tr><tr><th>6</th><td>Gender</td><td></td><td>Female</td><td></td><td>Male</td><td>2</td><td></td><td>String7</td></tr><tr><th>7</th><td>Age</td><td>38.9218</td><td>18</td><td>37.0</td><td>92</td><td></td><td></td><td>Int64</td></tr><tr><th>8</th><td>Tenure</td><td>5.0128</td><td>0</td><td>5.0</td><td>10</td><td></td><td></td><td>Int64</td></tr><tr><th>9</th><td>Balance</td><td>76485.9</td><td>0.0</td><td>97198.5</td><td>2.50898e5</td><td></td><td></td><td>Float64</td></tr><tr><th>10</th><td>NumOfProducts</td><td>1.5302</td><td>1</td><td>1.0</td><td>4</td><td></td><td></td><td>Int64</td></tr><tr><th>11</th><td>HasCrCard</td><td>0.7055</td><td>0</td><td>1.0</td><td>1</td><td></td><td></td><td>Int64</td></tr><tr><th>12</th><td>IsActiveMember</td><td>0.5151</td><td>0</td><td>1.0</td><td>1</td><td></td><td></td><td>Int64</td></tr><tr><th>13</th><td>EstimatedSalary</td><td>1.0009e5</td><td>11.58</td><td>1.00194e5</td><td>1.99992e5</td><td></td><td></td><td>Float64</td></tr><tr><th>14</th><td>Exited</td><td>0.2037</td><td>0</td><td>0.0</td><td>1</td><td></td><td></td><td>Int64</td></tr></tbody></table>




```julia
# Check column names
names(marketing_df)
```




    14-element Vector{Symbol}:
     :RowNumber
     :CustomerId
     :Surname
     :CreditScore
     :Geography
     :Gender
     :Age
     :Tenure
     :Balance
     :NumOfProducts
     :HasCrCard
     :IsActiveMember
     :EstimatedSalary
     :Exited



### Check Class Imbalance



```julia
# Count the classes
countmap(marketing_df.Exited)
```




    Dict{Int64, Int64} with 2 entries:
      0 => 7963
      1 => 2037



## Data Preprocessing


### One Hot Encoding


```julia
# One hot encoding
Lathe.preprocess.OneHotEncode(marketing_df,:Geography)
Lathe.preprocess.OneHotEncode(marketing_df,:Gender)
select!(marketing_df, Not([:RowNumber, :CustomerId,:Surname,:Geography,:Gender,:Male]))

```




<table class="data-frame"><thead><tr><th></th><th>CreditScore</th><th>Age</th><th>Tenure</th><th>Balance</th><th>NumOfProducts</th><th>HasCrCard</th><th>IsActiveMember</th></tr><tr><th></th><th>Int64</th><th>Int64</th><th>Int64</th><th>Float64</th><th>Int64</th><th>Int64</th><th>Int64</th></tr></thead><tbody><p>10,000 rows × 13 columns (omitted printing of 6 columns)</p><tr><th>1</th><td>619</td><td>42</td><td>2</td><td>0.0</td><td>1</td><td>1</td><td>1</td></tr><tr><th>2</th><td>608</td><td>41</td><td>1</td><td>83807.9</td><td>1</td><td>0</td><td>1</td></tr><tr><th>3</th><td>502</td><td>42</td><td>8</td><td>1.59661e5</td><td>3</td><td>1</td><td>0</td></tr><tr><th>4</th><td>699</td><td>39</td><td>1</td><td>0.0</td><td>2</td><td>0</td><td>0</td></tr><tr><th>5</th><td>850</td><td>43</td><td>2</td><td>1.25511e5</td><td>1</td><td>1</td><td>1</td></tr><tr><th>6</th><td>645</td><td>44</td><td>8</td><td>1.13756e5</td><td>2</td><td>1</td><td>0</td></tr><tr><th>7</th><td>822</td><td>50</td><td>7</td><td>0.0</td><td>2</td><td>1</td><td>1</td></tr><tr><th>8</th><td>376</td><td>29</td><td>4</td><td>1.15047e5</td><td>4</td><td>1</td><td>0</td></tr><tr><th>9</th><td>501</td><td>44</td><td>4</td><td>1.42051e5</td><td>2</td><td>0</td><td>1</td></tr><tr><th>10</th><td>684</td><td>27</td><td>2</td><td>1.34604e5</td><td>1</td><td>1</td><td>1</td></tr><tr><th>11</th><td>528</td><td>31</td><td>6</td><td>1.02017e5</td><td>2</td><td>0</td><td>0</td></tr><tr><th>12</th><td>497</td><td>24</td><td>3</td><td>0.0</td><td>2</td><td>1</td><td>0</td></tr><tr><th>13</th><td>476</td><td>34</td><td>10</td><td>0.0</td><td>2</td><td>1</td><td>0</td></tr><tr><th>14</th><td>549</td><td>25</td><td>5</td><td>0.0</td><td>2</td><td>0</td><td>0</td></tr><tr><th>15</th><td>635</td><td>35</td><td>7</td><td>0.0</td><td>2</td><td>1</td><td>1</td></tr><tr><th>16</th><td>616</td><td>45</td><td>3</td><td>1.43129e5</td><td>2</td><td>0</td><td>1</td></tr><tr><th>17</th><td>653</td><td>58</td><td>1</td><td>1.32603e5</td><td>1</td><td>1</td><td>0</td></tr><tr><th>18</th><td>549</td><td>24</td><td>9</td><td>0.0</td><td>2</td><td>1</td><td>1</td></tr><tr><th>19</th><td>587</td><td>45</td><td>6</td><td>0.0</td><td>1</td><td>0</td><td>0</td></tr><tr><th>20</th><td>726</td><td>24</td><td>6</td><td>0.0</td><td>2</td><td>1</td><td>1</td></tr><tr><th>21</th><td>732</td><td>41</td><td>8</td><td>0.0</td><td>2</td><td>1</td><td>1</td></tr><tr><th>22</th><td>636</td><td>32</td><td>8</td><td>0.0</td><td>2</td><td>1</td><td>0</td></tr><tr><th>23</th><td>510</td><td>38</td><td>4</td><td>0.0</td><td>1</td><td>1</td><td>0</td></tr><tr><th>24</th><td>669</td><td>46</td><td>3</td><td>0.0</td><td>2</td><td>0</td><td>1</td></tr><tr><th>25</th><td>846</td><td>38</td><td>5</td><td>0.0</td><td>1</td><td>1</td><td>1</td></tr><tr><th>26</th><td>577</td><td>25</td><td>3</td><td>0.0</td><td>2</td><td>0</td><td>1</td></tr><tr><th>27</th><td>756</td><td>36</td><td>2</td><td>1.36816e5</td><td>1</td><td>1</td><td>1</td></tr><tr><th>28</th><td>571</td><td>44</td><td>9</td><td>0.0</td><td>2</td><td>0</td><td>0</td></tr><tr><th>29</th><td>574</td><td>43</td><td>3</td><td>1.41349e5</td><td>1</td><td>1</td><td>1</td></tr><tr><th>30</th><td>411</td><td>29</td><td>0</td><td>59697.2</td><td>2</td><td>1</td><td>1</td></tr><tr><th>&vellip;</th><td>&vellip;</td><td>&vellip;</td><td>&vellip;</td><td>&vellip;</td><td>&vellip;</td><td>&vellip;</td><td>&vellip;</td></tr></tbody></table>



### Split Train/and Test Data


```julia
# Train test split
using Lathe.preprocess: TrainTestSplit
train, test = TrainTestSplit(marketing_df,.75);
```

## Build Model



```julia
# Train logistic regression model
fm = @formula(Exited ~ CreditScore + Age + Tenure + Balance + NumOfProducts + HasCrCard + IsActiveMember + EstimatedSalary + Female + France + Spain)
logit = glm(fm, train, Binomial(), ProbitLink())
```




    StatsModels.TableRegressionModel{GeneralizedLinearModel{GLM.GlmResp{Vector{Float64}, Binomial{Float64}, ProbitLink}, GLM.DensePredChol{Float64, LinearAlgebra.Cholesky{Float64, Matrix{Float64}}}}, Matrix{Float64}}
    
    Exited ~ 1 + CreditScore + Age + Tenure + Balance + NumOfProducts + HasCrCard + IsActiveMember + EstimatedSalary + Female + France + Spain
    
    Coefficients:
    ───────────────────────────────────────────────────────────────────────────────────────
                            Coef.   Std. Error       z  Pr(>|z|)     Lower 95%    Upper 95%
    ───────────────────────────────────────────────────────────────────────────────────────
    (Intercept)      -1.90933      0.165007     -11.57    <1e-30  -2.23274      -1.58592
    CreditScore      -0.000321917  0.000183184   -1.76    0.0789  -0.000680951   3.71172e-5
    Age               0.040893     0.00165251    24.75    <1e-99   0.0376541     0.0441318
    Tenure           -0.008864     0.00611129    -1.45    0.1469  -0.0208419     0.0031139
    Balance           1.65933e-6   3.30286e-7     5.02    <1e-06   1.01198e-6    2.30668e-6
    NumOfProducts    -0.040173     0.0309946     -1.30    0.1949  -0.100921      0.0205753
    HasCrCard        -0.00442931   0.0386394     -0.11    0.9087  -0.0801612     0.0713026
    IsActiveMember   -0.557894     0.0365213    -15.28    <1e-51  -0.629475     -0.486314
    EstimatedSalary   2.2925e-7    3.07604e-7     0.75    0.4561  -3.73644e-7    8.32143e-7
    Female            0.301642     0.0354259      8.51    <1e-16   0.232209      0.371076
    France           -0.450226     0.0446176    -10.09    <1e-23  -0.537674     -0.362777
    Spain            -0.443184     0.051707      -8.57    <1e-16  -0.544527     -0.34184
    ───────────────────────────────────────────────────────────────────────────────────────



## Model Predictions and Evaluation


```julia
# Predict the target variable on test data 
prediction = predict(logit,test)
```




    2406-element Vector{Union{Missing, Float64}}:
     0.24401107345293602
     0.1266535868551322
     0.031721959583257124
     0.11357816519004983
     0.24824114578495612
     0.024688755265128235
     0.14209354336141483
     0.18528877855991494
     0.15470097145575007
     0.25962439112051505
     0.15117890643161475
     0.2110682947689441
     0.06358192272871947
     ⋮
     0.24899439141513482
     0.23449577199293972
     0.13610439167926225
     0.1737934374110589
     0.1341643450975004
     0.5831068095078078
     0.2950497674661655
     0.04139159536998556
     0.06795785137729822
     0.017204995327274736
     0.12888818685657766
     0.15310112069144077




```julia
# Convert probability score to class
prediction_class = [if x < 0.5 0 else 1 end for x in prediction];

prediction_df = DataFrame(y_actual = test.Exited, y_predicted = prediction_class, prob_predicted = prediction);
prediction_df.correctly_classified = prediction_df.y_actual .== prediction_df.y_predicted
```




    2406-element BitVector:
     0
     1
     1
     1
     1
     1
     1
     1
     1
     0
     1
     1
     1
     ⋮
     1
     1
     1
     1
     1
     1
     1
     1
     1
     1
     1
     1



### Prediction Accuracy


```julia
accuracy = mean(prediction_df.correctly_classified)
```




    0.8100581878636741



### Confusion Matrix


```julia
# confusion_matrix = confusmat(2,prediction_df.y_actual, prediction_df.y_predicted)
confusion_matrix = MLBase.roc(prediction_df.y_actual, prediction_df.y_predicted)
```




    ROCNums{Int64}
      p = 510
      n = 1896
      tp = 105
      tn = 1844
      fp = 52
      fn = 405




### Results

The model is estimating far to many exiting cases.  About 4 times the true value. 


```julia
fpr, tpr, thresholds = sklearn.roc_curve(prediction_df.y_actual, prediction_df.prob_predicted)
```




    ([0.0, 0.0, 0.0, 0.0005274261603375527, 0.0005274261603375527, 0.0010548523206751054, 0.0010548523206751054, 0.0015822784810126582, 0.0015822784810126582, 0.0026371308016877636  …  0.8829113924050633, 0.9066455696202531, 0.9066455696202531, 0.9193037974683544, 0.9193037974683544, 0.92457805907173, 0.92457805907173, 0.9725738396624473, 0.9725738396624473, 1.0], [0.0, 0.00196078431372549, 0.00392156862745098, 0.00392156862745098, 0.00784313725490196, 0.00784313725490196, 0.01568627450980392, 0.01568627450980392, 0.03137254901960784, 0.03137254901960784  …  0.9921568627450981, 0.9921568627450981, 0.9941176470588236, 0.9941176470588236, 0.996078431372549, 0.996078431372549, 0.9980392156862745, 0.9980392156862745, 1.0, 1.0], [1.8467335270755767, 0.8467335270755767, 0.8140811888019499, 0.8092555110984978, 0.7970873802691381, 0.79684704533007, 0.7719016175181805, 0.7709263202992206, 0.7060214606993195, 0.6994801619873218  …  0.04233143871590189, 0.03786940431261241, 0.037850945580692276, 0.035665362242897694, 0.03532968973176317, 0.03416668456674327, 0.03407543014692377, 0.020932892669754958, 0.020885871157504798, 0.00597005405256463])




```julia
# Plot ROC curve
plot(fpr, tpr)
title!("ROC curve")
```




    
![svg](propensity_scoring_files/propensity_scoring_24_0.svg)
    



## The Class Imbalance Problem



```julia
# Count the classes
countmap(marketing_df.Exited)
```




    Dict{Int64, Int64} with 2 entries:
      0 => 7963
      1 => 2037



### Smote to fix imbalance


```julia
X2, y2 =smote(marketing_df[!,[:CreditScore,:Age ,:Tenure, :Balance, :NumOfProducts, :HasCrCard, :IsActiveMember, :EstimatedSalary, :Female , :France, :Spain]], marketing_df.Exited, k = 5, pct_under = 150, pct_over = 200)
df_balanced = X2
df_balanced.Exited = y2;

df = df_balanced;

# Count the classes
countmap(df.Exited)
```




    Dict{Int64, Int64} with 2 entries:
      0 => 6111
      1 => 6111



### Retest


```julia
# Train test split
train, test = TrainTestSplit(df,.75);

# Model Building
fm = @formula(Exited ~ CreditScore + Age + Tenure + Balance + NumOfProducts + HasCrCard + IsActiveMember + EstimatedSalary + Female + France + Spain)
logit = glm(fm, train, Binomial(), ProbitLink())

# Predict the target variable on test data 
prediction = predict(logit,test)

# Convert probability score to class
prediction_class = [if x < 0.5 0 else 1 end for x in prediction];

prediction_df = DataFrame(y_actual = test.Exited, y_predicted = prediction_class, prob_predicted = prediction);
prediction_df.correctly_classified = prediction_df.y_actual .== prediction_df.y_predicted


# Accuracy Score
accuracy = mean(prediction_df.correctly_classified)
print("Accuracy of the model is : ",accuracy)

# Confusion Matrix
confusion_matrix = MLBase.roc(prediction_df.y_actual, prediction_df.y_predicted)
```

    Accuracy of the model is : 0.7169563791407019




    ROCNums{Int64}
      p = 1550
      n = 1499
      tp = 1091
      tn = 1095
      fp = 404
      fn = 459





```julia
fpr, tpr, thresholds = sklearn.roc_curve(prediction_df.y_actual, prediction_df.prob_predicted)
# Plot ROC curve

```




    ([0.0, 0.0, 0.0, 0.00066711140760507, 0.00066711140760507, 0.00133422281521014, 0.00133422281521014, 0.0020013342228152103, 0.0020013342228152103, 0.00266844563042028  …  0.9846564376250834, 0.9893262174783188, 0.9893262174783188, 0.9913275517011341, 0.9913275517011341, 0.9973315543695798, 0.9986657771847899, 0.9993328885923949, 0.9993328885923949, 1.0], [0.0, 0.0006451612903225806, 0.0025806451612903226, 0.0025806451612903226, 0.005161290322580645, 0.005161290322580645, 0.007741935483870968, 0.007741935483870968, 0.00903225806451613, 0.00903225806451613  …  0.9980645161290322, 0.9980645161290322, 0.9987096774193548, 0.9987096774193548, 0.9993548387096775, 0.9993548387096775, 0.9993548387096775, 0.9993548387096775, 1.0, 1.0], [1.9907624292252022, 0.9907624292252022, 0.983731024429679, 0.97951657298985, 0.9730082291507035, 0.9713532719467679, 0.9629327481173712, 0.9604203755106321, 0.9593444340323958, 0.9584649467140461  …  0.06923199350115271, 0.06553287523911823, 0.06469253560487893, 0.058594401854125504, 0.057872556108602216, 0.034170953161915506, 0.03357051125028141, 0.03297342671224324, 0.030937011626933943, 0.023743078872535135])




```julia
plot(fpr, tpr)
title!("ROC curve")
```




    
![svg](propensity_scoring_files/propensity_scoring_32_0.svg)
    



## Final Discussion

When accounting for class imbalance, the model accuracy is reduced to 71 percent from about 81 percent.  

While this seems counterintutive, the second model is actually a better model overall.  

The model with 81 percent accuracy is simply more accurate by chance.  The bin of exits to remains is far larger.  Thus, reported accuracy is higher. 

When the classes are normalized, we see a prediction of about 71 percent.  Confidently, I can say that this model would scale appropriately.  

The first model on the other hand would scale to about 25-30 percent accuracy. 
