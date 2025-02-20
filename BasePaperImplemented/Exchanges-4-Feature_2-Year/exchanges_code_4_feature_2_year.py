# -*- coding: utf-8 -*-
"""Exchanges-Code_4-Feature_2-Year.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ezaK8R0C3yswtUibnCoiVQUaB3uB8pxs
"""

from google.colab import drive
# Mount Google Drive to access files
drive.mount('/content/drive')

"""# Bitcoin price Prediction using LSTM

![](https://media0.giphy.com/media/f67U9Xc53i4ViUs5T2/giphy.gif?cid=ecf05e47h4dpv8s5ppc6omcbb5uzwprey8y97x3fy8qk8dk8&rid=giphy.gif&ct=g)

# [](http://) Table of Content
<hr style='height:2px'>

## 1. What is LSTM?
## 2. Importing Library
## 3. Loading Dataset
## 4. EDA
## 5. Biulding Model
## 6. Prediction
## 7. Evaluation
## 8. Conclusion
<hr style='height:2px'>

# 1. What is LSTM ?

* ###  Long short-term memory is an artificial recurrent neural network architecture used in the field of deep learning. Unlike standard feedforward neural networks, LSTM has feedback connections. It can process not only single data points, but also entire sequences of data.

* ### Long Short-Term Memory (LSTM) networks are a type of recurrent neural network capable of learning order dependence in sequence prediction problems. This is a behavior required in complex problem domains like machine translation, speech recognition, and more. LSTMs are a complex area of deep learning.

* ### LSTMs are often referred to as fancy RNNs. Vanilla RNNs do not have a cell state. They only have hidden states and those hidden states serve as the memory for RNNs. Meanwhile, LSTM has both cell states and a hidden states.

# 2. Importing Library
"""

# First we will import the necessary Library
import os
import pandas as pd
import numpy as np
import math
import datetime as dt
from IPython.display import display
# For Evalution we will use these library
from sklearn.metrics import mean_squared_error, mean_absolute_error, explained_variance_score, r2_score, mean_absolute_percentage_error
from sklearn.metrics import mean_poisson_deviance, mean_gamma_deviance, accuracy_score
from sklearn.preprocessing import MinMaxScaler
# For model building we will use these library
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.layers import LSTM
# For PLotting we will use these library
import matplotlib.pyplot as plt
from itertools import cycle
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

"""# 3. Loading Dataset

#  [We can use this link to download bitcoin dataset from yahoo finance](https://finance.yahoo.com/quote/BTC-USD/history?p=BTC-USD)
"""

# Load our dataset
# Note it should be in same dir
maindf=pd.read_csv('/content/drive/MyDrive/Fyp_Data/BTC-USD-Exchanges.csv')

print('Total number of days present in the dataset: ',maindf.shape[0])
print('Total number of fields present in the dataset: ',maindf.shape[1])

maindf.shape

maindf.head()

maindf.tail()

maindf.info()

maindf.describe()

"""# Checking for Null Values"""

print('Null Values:',maindf.isnull().values.sum())

print('NA values:',maindf.isnull().values.any())

# If dataset had null values we can use this code to drop all the null values present in the dataset

# maindf=maindf.dropna()
# print('Null Values:',maindf.isnull().values.sum())
# print('NA values:',maindf.isnull().values.any())

# Final shape of the dataset after dealing with null values

maindf.shape

"""# 4. EDA(Exploratory Data Analysis)"""

# Printing the start date and end date of the dataset
sd = maindf.iloc[0, 0]
ed = maindf.iloc[-1, 0]

print('Starting Date:', sd)
print('Ending Date:', ed)

"""#### StockPrice Analysis from Start

# Analysis of Year 2021
"""

maindf['Date'] = pd.to_datetime(maindf['Date'], format='%Y-%m-%d')

y_2021 = maindf.loc[(maindf['Date'] >= '2021-01-01')
                     & (maindf['Date'] < '2021-12-31')]

y_2021.drop(y_2021[['Adj Close','Volume']],axis=1)

monthvise= y_2021.groupby(y_2021['Date'].dt.strftime('%B'))[['Open','Close']].mean()
new_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
             'September', 'October', 'November', 'December']
monthvise = monthvise.reindex(new_order, axis=0)
monthvise

"""#### Since we had data till 24-08-2021 in Months after August its showing NaN"""

fig = go.Figure()

fig.add_trace(go.Bar(
    x=monthvise.index,
    y=monthvise['Open'],
    name='Stock Open Price',
    marker_color='crimson'
))
fig.add_trace(go.Bar(
    x=monthvise.index,
    y=monthvise['Close'],
    name='Stock Close Price',
    marker_color='lightsalmon'
))

fig.update_layout(barmode='group', xaxis_tickangle=-45,
                  title='Monthwise comparision between Stock open and close price')
fig.show()

y_2021.groupby(y_2021['Date'].dt.strftime('%B'))['Low'].min()
monthvise_high = y_2021.groupby(maindf['Date'].dt.strftime('%B'))['High'].max()
monthvise_high = monthvise_high.reindex(new_order, axis=0)

monthvise_low = y_2021.groupby(y_2021['Date'].dt.strftime('%B'))['Low'].min()
monthvise_low = monthvise_low.reindex(new_order, axis=0)

fig = go.Figure()
fig.add_trace(go.Bar(
    x=monthvise_high.index,
    y=monthvise_high,
    name='Stock high Price',
    marker_color='rgb(0, 153, 204)'
))
fig.add_trace(go.Bar(
    x=monthvise_low.index,
    y=monthvise_low,
    name='Stock low Price',
    marker_color='rgb(255, 128, 0)'
))

fig.update_layout(barmode='group',
                  title=' Monthwise High and Low stock price')
fig.show()

names = cycle(['Stock Open Price','Stock Close Price','Stock High Price','Stock Low Price'])

fig = px.line(y_2021, x=y_2021.Date, y=[y_2021['Open'], y_2021['Close'],
                                          y_2021['High'], y_2021['Low']],
             labels={'Date': 'Date','value':'Stock value'})
fig.update_layout(title_text='Stock analysis chart', font_size=15, font_color='black',legend_title_text='Stock Parameters')
fig.for_each_trace(lambda t:  t.update(name = next(names)))
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False)

fig.show()

"""# Analysis of Year 2022"""

maindf['Date'] = pd.to_datetime(maindf['Date'], format='%Y-%m-%d')

y_2022 = maindf.loc[(maindf['Date'] >= '2022-01-01')
                     & (maindf['Date'] < '2022-12-31')]

monthvise= y_2022.groupby(y_2022['Date'].dt.strftime('%B'))[['Open','Close']].mean()
new_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
             'September', 'October', 'November', 'December']
monthvise = monthvise.reindex(new_order, axis=0)
monthvise

fig = go.Figure()

fig.add_trace(go.Bar(
    x=monthvise.index,
    y=monthvise['Open'],
    name='Stock Open Price',
    marker_color='crimson'
))
fig.add_trace(go.Bar(
    x=monthvise.index,
    y=monthvise['Close'],
    name='Stock Close Price',
    marker_color='lightsalmon'
))

fig.update_layout(barmode='group', xaxis_tickangle=-45,
                  title='Monthwise comparision between Stock open and close price')
fig.show()

y_2022.groupby(y_2022['Date'].dt.strftime('%B'))['Low'].min()
monthvise_high = y_2022.groupby(maindf['Date'].dt.strftime('%B'))['High'].max()
monthvise_high = monthvise_high.reindex(new_order, axis=0)

monthvise_low = y_2022.groupby(y_2022['Date'].dt.strftime('%B'))['Low'].min()
monthvise_low = monthvise_low.reindex(new_order, axis=0)

fig = go.Figure()
fig.add_trace(go.Bar(
    x=monthvise_high.index,
    y=monthvise_high,
    name='Stock high Price',
    marker_color='rgb(0, 153, 204)'
))
fig.add_trace(go.Bar(
    x=monthvise_low.index,
    y=monthvise_low,
    name='Stock low Price',
    marker_color='rgb(255, 128, 0)'
))

fig.update_layout(barmode='group',
                  title=' Monthwise High and Low stock price')
fig.show()

names = cycle(['Stock Open Price','Stock Close Price','Stock High Price','Stock Low Price'])

fig = px.line(y_2022, x=y_2022.Date, y=[y_2022['Open'], y_2022['Close'],
                                          y_2022['High'], y_2022['Low']],
             labels={'Date': 'Date','value':'Stock value'})
fig.update_layout(title_text='Stock analysis chart', font_size=15, font_color='black',legend_title_text='Stock Parameters')
fig.for_each_trace(lambda t:  t.update(name = next(names)))
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False)

fig.show()

"""# Overall Analysis from 2014-2022"""

maindf['Date'] = pd.to_datetime(maindf['Date'], format='%Y-%m-%d')

y_overall = maindf.loc[(maindf['Date'] >= '2014-09-17')
                     & (maindf['Date'] <= '2022-02-19')]

y_overall.drop(y_overall[['Adj Close','Volume']],axis=1)

monthvise= y_overall.groupby(y_overall['Date'].dt.strftime('%B'))[['Open','Close']].mean()
new_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
             'September', 'October', 'November', 'December']
monthvise = monthvise.reindex(new_order, axis=0)
monthvise

names = cycle(['Stock Open Price','Stock Close Price','Stock High Price','Stock Low Price'])

fig = px.line(y_overall, x=y_overall.Date, y=[y_overall['Open'], y_overall['Close'],
                                          y_overall['High'], y_overall['Low']],
             labels={'Date': 'Date','value':'Stock value'})
fig.update_layout(title_text='Stock analysis chart', font_size=15, font_color='black',legend_title_text='Stock Parameters')
fig.for_each_trace(lambda t:  t.update(name = next(names)))
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False)

fig.show()

"""# 5. Building LSTM Model

* ## First Step is Preparing Data for Training and Testing

* ## Here we are just considering 1 year data for training data

* ## Since Bitcoin price has drastically flucated from 200 dollar in year 2014 to 15000 dollar in year 2018 to 3000 dollar in year 2019(theses values are apporx) so we will just consider 1 Year to avoid this type of flucation in the data.

* ## As we want to predict Close Price of the Bitcoin so we are just Considering Close and Date
"""

# Taking required features and target
closedf = maindf[['Date', 'Open', 'High', 'Low', 'Adj Close', 'Volume', 'Close']]

# Preserve the 'Date' column for future use
date_column = closedf['Date'].reset_index(drop=True)

print("Shape of close dataframe:", closedf.shape)

fig = px.line(closedf, x=closedf.Date, y=closedf.Close,labels={'date':'Date','close':'Close Stock'})
fig.update_traces(marker_line_width=2, opacity=0.8, marker_line_color='orange')
fig.update_layout(title_text='Whole period of timeframe of Bitcoin close price 2014-2022', plot_bgcolor='white',
                  font_size=15, font_color='black')
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False)
fig.show()

"""### Now we will Take data of just 1 Year"""

# Filter data for the specified period
# Filter data for the specified period from 2022-10-08 to 2024-10-08
closedf = closedf[(maindf['Date'] > '2022-10-07') & (maindf['Date'] <= '2024-10-08')]
date_column = date_column[(maindf['Date'] > '2022-10-07') & (maindf['Date'] <= '2024-10-08')].reset_index(drop=True)


print("Total data for prediction: ", closedf.shape[0])

# After filtering the data but before deleting the 'Date' column
closedf = maindf[['Date', 'Open', 'High', 'Low', 'Adj Close', 'Volume', 'Close']]
closedf = closedf[(maindf['Date'] > '2022-10-07') & (maindf['Date'] <= '2024-10-08')].reset_index(drop=True)
date_column = closedf['Date']
print("Total data for prediction: ", closedf.shape[0])
# Preserve the original 'Date' and 'Close' columns for plotting
close_stock = closedf[['Date', 'Close']].copy()

closedf

fig = px.line(closedf, x=closedf.Date, y=closedf.Close,labels={'date':'Date','close':'Close Stock'})
fig.update_traces(marker_line_width=2, opacity=0.8, marker_line_color='orange')
fig.update_layout(title_text='Considered period to predict Bitcoin close price',
                  plot_bgcolor='white', font_size=15, font_color='black')
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False)
fig.show()

"""* ### Normalizing Data
- Normalization is a technique often applied as part of data preparation for machine learning. The goal of normalization is to change the values of numeric columns in the dataset to use a common scale, without distorting differences in the ranges of values or losing information.
- MinMaxScaler. For each value in a feature, MinMaxScaler subtracts the minimum value in the feature and then divides by the range. The range is the difference between the original maximum and original minimum. MinMaxScaler preserves the shape of the original distribution.
"""

# Remove the 'Date' column for scaling
del closedf['Date']
# Normalize the data (excluding the Date column)
scaler = MinMaxScaler(feature_range=(0, 1))
closedf = scaler.fit_transform(np.array(closedf))
print("Shape of normalized data:", closedf.shape)

"""* ### Slicing data into Training set and Testing set"""

# We keep the training set as 60% and 40% testing set
training_size = int(len(closedf) * 0.60)
test_size = len(closedf) - training_size
train_data, test_data = closedf[0:training_size, :], closedf[training_size:len(closedf), :]
print("train_data: ", train_data.shape)
print("test_data: ", test_data.shape)

# Extract training and testing dates using the preserved 'Date' column
training_dates = date_column[:training_size].reset_index(drop=True)
testing_dates = date_column[training_size:].reset_index(drop=True)

# Display start and end dates for training and testing
print(f"Training data time frame: Start: {training_dates.iloc[0]}, End: {training_dates.iloc[-1]}")
print(f"Testing data time frame: Start: {testing_dates.iloc[0]}, End: {testing_dates.iloc[-1]}")

"""* ### Now we Transform the Close price based on Time-series-analysis forecasting requirement , Here we will take 15   """

def create_dataset(dataset, time_step=1):
    dataX, dataY = [], []
    for i in range(len(dataset) - time_step - 1):

        a = dataset[i:(i + time_step), :-1]
        dataX.append(a)

        # Output: Next Close value (target)
        dataY.append(dataset[i + time_step, -1])
    return np.array(dataX), np.array(dataY)

# Generate training and testing datasets using create_dataset
time_step = 15  # Define the time step for sequence length
X_train, y_train = create_dataset(train_data, time_step)
X_test, y_test = create_dataset(test_data, time_step)

print("Generated datasets:")
print("X_train: ", X_train.shape)
print("y_train: ", y_train.shape)
print("X_test: ", X_test.shape)
print("y_test", y_test.shape)

# Reshape input to be [samples, time steps, features]
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], X_train.shape[2])
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], X_test.shape[2])

print("After reshaping:")
print("X_train: ", X_train.shape)
print("X_test: ", X_test.shape)

"""* # Actuall Model Building"""

# Define the LSTM model
model = Sequential()

# LSTM layer with input shape (time steps, features)
model.add(LSTM(10, input_shape=(X_train.shape[1], X_train.shape[2]), activation="relu"))

# Dense output layer to predict one value (Next Close)
model.add(Dense(1))

# Compile the model
model.compile(loss="mean_squared_error", optimizer="adam")

history = model.fit(X_train,y_train,validation_data=(X_test,y_test),epochs=200,batch_size=32,verbose=1)

from tensorflow.keras.models import load_model
# Define the save path
save_path = '/content/drive/MyDrive/Fyp_Model/Exchange-4-feature_Lstm_Model_2-YEAR.keras'

# Save the trained model
model.save(save_path)
print(f"Model saved successfully at: {save_path}")

loaded_model = load_model(save_path)
print("Model loaded successfully.")
# If continuing training, recompile the optimizer
loaded_model.compile(optimizer='adam', loss='mean_squared_error')
print("Optimizer reset successfully.")

"""- ### Plotting Loss vs Validation loss"""

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(len(loss))

plt.plot(epochs, loss, 'r', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.legend(loc=0)
plt.figure()


plt.show()

### Lets Do the prediction and check performance metrics
train_predict=model.predict(X_train)
test_predict=model.predict(X_test)
train_predict.shape, test_predict.shape

"""- # Model Evaluation"""

# Inverse transform the predictions to their original scale

# For train predictions
print("Before inverse transform - Train predict shape:", train_predict.shape)
train_predict = scaler.inverse_transform(np.hstack((np.zeros((train_predict.shape[0], closedf.shape[1] - 1)), train_predict)))
print("After inverse transform - Train predict shape:", train_predict.shape)

# For test predictions
print("Before inverse transform - Test predict shape:", test_predict.shape)
test_predict = scaler.inverse_transform(np.hstack((np.zeros((test_predict.shape[0], closedf.shape[1] - 1)), test_predict)))
print("After inverse transform - Test predict shape:", test_predict.shape)

# Inverse transform the actual values for comparison

# For train actual values
print("Before inverse transform - Original y_train shape:", y_train.shape)
original_ytrain = scaler.inverse_transform(np.hstack((np.zeros((y_train.shape[0], closedf.shape[1] - 1)), y_train.reshape(-1, 1))))
print("After inverse transform - Original y_train shape:", original_ytrain.shape)

# For test actual values
print("Before inverse transform - Original y_test shape:", y_test.shape)
original_ytest = scaler.inverse_transform(np.hstack((np.zeros((y_test.shape[0], closedf.shape[1] - 1)), y_test.reshape(-1, 1))))
print("After inverse transform - Original y_test shape:", original_ytest.shape)

# Extract the 'Close' values (last column) from the inverse transformed data
train_predicted_close = train_predict[:, -1]  # Extract last column
test_predicted_close = test_predict[:, -1]    # Extract last column

original_ytrain_close = original_ytrain[:, -1]  # Extract last column
original_ytest_close = original_ytest[:, -1]    # Extract last column

# Print shapes for verification
print("Train predicted close shape:", train_predicted_close.shape)
print("Test predicted close shape:", test_predicted_close.shape)
print("Original y_train close shape:", original_ytrain_close.shape)
print("Original y_test close shape:", original_ytest_close.shape)

print("---------------------------------------------------------")
# Create a DataFrame to compare predicted and actual values for the test set
comparison_table = pd.DataFrame({
    'Date': testing_dates[-len(test_predicted_close):].reset_index(drop=True),
    'Predicted Close': test_predicted_close,
    'Actual Close': original_ytest_close
})

# Compute the absolute difference between predicted and actual values
comparison_table['Difference'] = abs(comparison_table['Predicted Close'] - comparison_table['Actual Close'])

# Calculate the average difference
average_difference = comparison_table['Difference'].mean()

# Display the updated DataFrame in tabular format
display(comparison_table.head())
print("--------------------------------------------------------")
# Print the average difference
print(f"\nAverage Difference: {average_difference:.2f}")

"""- ## Evaluation metrices RMSE, MSE , MAE , R square , Variance Regression Score
- ## Regression Loss Mean Gamma deviance regression loss (MGD) and Mean Poisson deviance regression loss (MPD)
"""

# Evaluation metrics RMSE, MAE, MAPE
print("-------------------------------------------------------------------------------------")
print("Our Code :: ")
print("4 Feature ( Open,High,Low,Adj-Close,Volume ) ")
print("2 Year Training Period ")
print("Train and Test on Exchanges Data ")

print("-------------------------------------------------------------------------------------")
# For train data
print("Train data RMSE: ", math.sqrt(mean_squared_error(original_ytrain, train_predict)))
print("Train data MSE: ", mean_squared_error(original_ytrain, train_predict))
print("Train data MAE: ", mean_absolute_error(original_ytrain, train_predict))
print("Train data MAPE: % ", mean_absolute_percentage_error(original_ytrain, train_predict) * 100)
print("Train data R2: ", r2_score(original_ytrain, train_predict))
print("Train data explained variance regression score:",explained_variance_score(original_ytrain, train_predict))
#print("Train data MGD: ", mean_gamma_deviance(original_ytrain, train_predict))
#print("Train data MPD: ", mean_poisson_deviance(original_ytrain, train_predict))
print("-------------------------------------------------------------------------------------")
# For test data
print("Test data RMSE: ", math.sqrt(mean_squared_error(original_ytest, test_predict)))
print("Test data MSE: ", mean_squared_error(original_ytest, test_predict))
print("Test data MAE: ", mean_absolute_error(original_ytest, test_predict))
print("Test data MAPE: % ", mean_absolute_percentage_error(original_ytest, test_predict) * 100)
print("Test data R2: ", r2_score(original_ytest, test_predict))
print("Test data explained variance regression score:",explained_variance_score(original_ytest, test_predict))
#print("Test data MGD: ", mean_gamma_deviance(original_ytest, test_predict))
#print("Test data MPD: ", mean_poisson_deviance(original_ytest, test_predict))
print("-------------------------------------------------------------------------------------")

"""- # Comparision of original Bitcoin close price and predicted close price"""

# Shift train predictions for plotting
look_back = time_step
trainPredictPlot = np.empty((len(close_stock), 1))
trainPredictPlot[:, :] = np.nan
trainPredictPlot[look_back:len(train_predicted_close)+look_back, 0] = train_predicted_close
print("Train predicted data: ", trainPredictPlot.shape)

# Shift test predictions for plotting
testPredictPlot = np.empty((len(close_stock), 1))
testPredictPlot[:, :] = np.nan
testPredictPlot[len(train_predicted_close)+(look_back*2)+1:len(close_stock)-1, 0] = test_predicted_close
print("Test predicted data: ", testPredictPlot.shape)

# Prepare the DataFrame for plotting
plotdf = pd.DataFrame({
    'Date': close_stock['Date'],
    'Original Close': close_stock['Close'],
    'Train Predicted Close': trainPredictPlot.flatten(),
    'Test Predicted Close': testPredictPlot.flatten()
})

# Plotting
names = cycle(['Original Close Price', 'Train Predicted Close Price', 'Test Predicted Close Price'])

fig = px.line(
    plotdf,
    x='Date',
    y=['Original Close', 'Train Predicted Close', 'Test Predicted Close'],
    labels={'value': 'Stock Price', 'Date': 'Date'}
)
fig.update_layout(
    title_text='Comparison between Original Close Price vs Predicted Close Price',
    plot_bgcolor='white',
    font_size=15,
    font_color='black',
    legend_title_text='Close Price'
)
fig.for_each_trace(lambda t: t.update(name=next(names)))

fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False)
fig.show()