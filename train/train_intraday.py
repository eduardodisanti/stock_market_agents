import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import matplotlib.pyplot as plt
import deepdish as dd

from tensorflow.python.keras.utils import tf_utils

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

import pickle
import numpy as np

SYMBOL = "TSLA"
file_path = "../data/SPCE/intraday_20200110.json"

with open(file_path, "rb") as fb:
    jfile = pickle.load(fb)

history = jfile['intraday']

X = []
Y = []
vY = []
for date in history:
    _v = history[date]

    _open   = float(_v['open'])
    _close  = float(_v['close'])
    _high   = float(_v['high'])
    _low    = float(_v['low'])
    _volume = int(_v['volume'])

    vX = [_open, _close, _high, _low, _volume]

    X.append(vX)
    Y.append(_close)
    vY.append(_volume)

X = X[::-1]
Y = Y[::-1]
X = np.array(X)
Y = np.array(Y)
vY = np.array(vY)

X = X[1:]
Y = Y[1:]

#### SCALE DATA SET ####

scaler = MinMaxScaler()
scaler.fit(X)

dd.io.save("../data/"+SYMBOL+"/intraday_scaler.h5", scaler)

X = scaler.transform(X)

slice = int(len(X)/20)
X_train = X[0:-slice]
Y_train = Y[0:-slice]
X_test = X[-slice:]
Y_test = Y[-slice:]

X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
X_test  = np.reshape(X_test,  (X_test.shape[0],  1, X_test.shape[1]))

model = Sequential()
model.add(LSTM(24, input_shape=(1, X_train.shape[2])))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
hist = model.fit(X_train, Y_train, epochs=10, batch_size=1, verbose=1)

model.save("../data/"+SYMBOL+"/intraday_model.h5")
plt.plot(hist.history['loss']);
plt.show()

plt.plot(Y_test, "x", label="real")
pred = model.predict(X_test)
plt.plot(pred, label="pred")
plt.legend();
plt.show()
