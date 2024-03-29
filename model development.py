import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import skillsnetwork
import warnings
warnings.filterwarnings('ignore')

#This function will download the dataset into your browser 

from pyodide.http import pyfetch

async def download(url, filename):
    response = await pyfetch(url)
    if response.status == 200:
        with open(filename, "wb") as f:
            f.write(await response.bytes())

df = pd.read_csv("automobileEDA.csv", header=0)

df.head()

#loading the modules for linear regression

from sklearn.linear_model import LinearRegression

#Create the linear regression object

lm = LinearRegression()
lm

#"highway-mpg" help us predict 

X = df[['highway-mpg']]
Y = df['price']

lm.fit(X,Y)

#output a prediction

Yhat=lm.predict(X)
Yhat[0:5]   

#value of the intercept 

lm.intercept_

#value of slope

lm.coef_

#Create the linear regression 'lm1'

lm1 = LinearRegression()
lm1

#Train the model using "engine-size" as the independent variable and "price" as the dependent variable

lm1.fit(df[['engine-size']], df[['price']])
lm1

#slope 

lm1.coef_

#intercept

lm1.intercept_

#equation of the predicted line

# using X and Y  
Yhat=-7963.34 + 166.86*X

Price=-7963.34 + 166.86*df['engine-size']

#MULTIPLE REGRESSION
#develop a model using these variables as the predictor variables

Z = df[['horsepower', 'curb-weight', 'engine-size', 'highway-mpg']]

#Fit the linear model using the four above-mentioned variables

lm.fit(Z, df['price'])

lm.intercept_

lm.coef_

#Create and train a Multiple Linear Regression model "lm2" where the response variable is "price", and the predictor variable is "normalized-losses" and "highway-mpg".

lm2 = LinearRegression()
lm2.fit(df[['normalized-losses' , 'highway-mpg']],df['price'])

lm2.coef_

#Model Evaluation Using Visualization

import seaborn as sns
%matplotlib inline 

#visualize highway-mpg as potential predictor variable of price

width = 12
height = 10
plt.figure(figsize=(width, height))
sns.regplot(x="highway-mpg", y="price", data=df)
plt.ylim(0,)

#compare this plot to the regression plot of "peak-rpm

plt.figure(figsize=(width, height))
sns.regplot(x="peak-rpm", y="price", data=df)
plt.ylim(0,)

#Given the regression plots above, is "peak-rpm" or "highway-mpg" more strongly correlated with "price"

df[["peak-rpm","highway-mpg","price"]].corr()

#residual plot

width = 12
height = 10
plt.figure(figsize=(width, height))
sns.residplot(x=df['highway-mpg'],y=df['price'])
plt.show()

#look at the distribution of the fitted values that result from the model and compare it to the distribution of the actual values

Y_hat = lm.predict(Z)

plt.figure(figsize=(width, height))


ax1 = sns.distplot(df['price'], hist=False, color="r", label="Actual Value")
sns.distplot(Y_hat, hist=False, color="b", label="Fitted Values" , ax=ax1)


plt.title('Actual vs Fitted Values for Price')
plt.xlabel('Price (in dollars)')
plt.ylabel('Proportion of Cars')

plt.show()
plt.close()

#Polynomial Regression and Pipelines

def PlotPolly(model, independent_variable, dependent_variabble, Name):
    x_new = np.linspace(15, 55, 100)
    y_new = model(x_new)

    plt.plot(independent_variable, dependent_variabble, '.', x_new, y_new, '-')
    plt.title('Polynomial Fit with Matplotlib for Price ~ Length')
    ax = plt.gca()
    ax.set_facecolor((0.898, 0.898, 0.898))
    fig = plt.gcf()
    plt.xlabel(Name)
    plt.ylabel('Price of Cars')

    plt.show()
    plt.close()

x = df['highway-mpg']
y = df['price']

# Here we use a polynomial of the 3rd order (cubic) 
f = np.polyfit(x, y, 3)
p = np.poly1d(f)
print(p)

PlotPolly(p, x, y, 'highway-mpg')

np.polyfit(x, y, 3)

# Here we use a polynomial of the 11rd order (cubic) 
f1 = np.polyfit(x, y, 11)
p1 = np.poly1d(f1)
print(p1)
PlotPolly(p1,x,y, 'Highway MPG')

from sklearn.preprocessing import PolynomialFeatures

#create a PolynomialFeatures object of degree 2

pr=PolynomialFeatures(degree=2)
pr

Z_pr=pr.fit_transform(Z)

Z.shape

Z_pr.shape

#PIPELINE

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

#create the pipeline by creating a list of tuples including the name of the model or estimator and its corresponding constructor.

Input=[('scale',StandardScaler()), ('polynomial', PolynomialFeatures(include_bias=False)), ('model',LinearRegression())]

#input the list as an argument to the pipeline constructor

pipe=Pipeline(Input)
pipe

#normalize the data, perform a transform and fit the model simultaneously

Z = Z.astype(float)
pipe.fit(Z,y)

#normalize the data, perform a transform and produce a prediction simultaneously

ypipe=pipe.predict(Z)
ypipe[0:4]

#pipeline that standardizes the data, then produce a prediction using a linear regression model using the features Z and target y

Input=[('scale',StandardScaler()),('model',LinearRegression())]

pipe=Pipeline(Input)

pipe.fit(Z,y)

ypipe=pipe.predict(Z)
ypipe[0:10]


#Measures for In-Sample Evaluation

#highway_mpg_fit
lm.fit(X, Y)
# Find the R^2
print('The R-square is: ', lm.score(X, Y))

#predict the output

Yhat=lm.predict(X)
print('The output of the first four predicted value is: ', Yhat[0:4])

from sklearn.metrics import mean_squared_error

# compare the predicted results with the actual results

mse = mean_squared_error(df['price'], Yhat)
print('The mean square error of price and predicted value is: ', mse)

# fit the model 
lm.fit(Z, df['price'])
# Find the R^2
print('The R-square is: ', lm.score(Z, df['price']))

Y_predict_multifit = lm.predict(Z)

print('The mean square error of price and predicted value using multifit is: ', \
      mean_squared_error(df['price'], Y_predict_multifit))

from sklearn.metrics import r2_score 

#apply the function to get the value of R^2

r_squared = r2_score(y, p(x))
print('The R-square value is: ', r_squared)

#MSE

mean_squared_error(df['price'], p(x))

#Prediction and Decision Making

import matplotlib.pyplot as plt
import numpy as np

%matplotlib inline 

new_input=np.arange(1, 100, 1).reshape(-1, 1)

lm.fit(X, Y)
lm

yhat=lm.predict(new_input)
yhat[0:5]

plt.plot(new_input, yhat)
plt.show()