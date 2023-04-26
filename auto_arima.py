# -*- coding: utf-8 -*-
"""auto_arima.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Q1JQkbfxo4lAROGBbu8tHT3q9EYNpKI4
"""

import pandas as pd
import numpy as np

df = pd.read_csv("AAP_data.csv", index_col=['date'], parse_dates=['date'], dayfirst=True)
df.head()

import matplotlib
from matplotlib import pyplot as plt

df['close'].plot()

from statsmodels. tsa.stattools import adfuller
adfuller(df['close'])

df_close = df['close'] 
df_close_diff = df_close.diff(periods=1).dropna()

adfuller(df_close_diff)

df_close_diff.plot()

df_close_diff = df_close_diff.resample('M').mean()
df_close_diff.plot()

!pip install pmdarima

from pmdarima.arima import ADFTest
adf_test = ADFTest(alpha=0.05)
adf_test.should_diff(df_close_diff)

train_size = int(len(df_close_diff) * 0.90)
train, test = df_close_diff[0:train_size], df_close_diff[train_size:]

from pmdarima.arima import auto_arima
df_close_diff_fit = auto_arima(train, start_p=0, d=1, start_q=0,
                         max_p=5, max_d=5, max_q=5, start_P=0,
                         D=1, start_Q=0, max_P=5, max_D=5,
                         max_Q=5, m=12, seasonal=True,
                         supress_warnings=True, stepwise = True,
                         random_state=20, n_fits = 50 )

df_close_diff_fit.summary()

prediction = df_close_diff_fit.predict(n_periods=22)
prediction

y = df['close']
y_pred = prediction

d = y - y_pred
mse_f = np.mean(d**2)
mae_f = np.mean(abs(d))
print("MAE:",mae_f)
print("MSE:", mse_f)