import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import matplotlib.pyplot as plt
import deepdish as dd
from sklearn.linear_model import LinearRegression
from collections import deque

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

import pickle
import numpy as np

SYMBOL   = "DAL"
PATIENCE = 10
MIN_VAR  = 2

file_path = "../data/"+SYMBOL+"/history.pckl"

with open(file_path, "rb") as fb:
    jfile = pickle.load(fb)

history = jfile['history']

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
vY = vY[1:]

#### SCALE DATA SET ####
scaler = MinMaxScaler()
scaler.fit(X)

dd.io.save("../data/"+SYMBOL+"/" + "_scaler.h5", scaler)

X = scaler.transform(X)

slice = int(len(X)/20)
X_train = X[0:-slice]
Y_train = Y[0:-slice]
X_test = X[-slice:]
Y_test = Y[-slice:]
vY_train = vY[0:-slice]
vY_test  = vY[-slice:]

X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
X_test  = np.reshape(X_test,  (X_test.shape[0],  1, X_test.shape[1]))

#### TRAIN NEXT PRICE ####
model = Sequential()
model.add(LSTM(48, input_shape=(1, X_train.shape[2])))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
i = 0
trained = False
last_err = 1e10

#PATIENCE = int(len(X)*0.01) + 10
#err_hist = deque(maxlen=PATIENCE)
PATIENCE = 5
notimp = 0

while not trained:
    i+=1
    plt.clf()
    hist = model.fit(X_train, Y_train, epochs=1, batch_size=1, verbose=2)
    pred = model.predict(X_test)
    plt.title(SYMBOL)
    plt.plot(Y_test, "x", label="real")
    plt.plot(pred, label="pred")
    plt.legend();
    plt.pause(0.1)
    err = mean_squared_error(Y_test, pred)

    if err >= last_err:
        notimp += 1
    else:
        model.save("../data/" + SYMBOL + "/" + "_model.h5")
        plt.savefig("../data/" + SYMBOL + "/trainfig.png")

    trained =  err > last_err and notimp >= PATIENCE

    last_err = err
    print("EPOCH", i,"MSE", err, "NOT_IMPROVING", notimp, "PATIENCE", PATIENCE)
    if trained:
        break

model.save("../data/"+SYMBOL+"/" + "_model.h5")
plt.savefig("../data/"+SYMBOL+"/trainfig.png")
plt.title("Loss")
model.save("../data/"+SYMBOL+"/" + "_model.h5")
plt.plot(hist.history['loss'], label="train");
plt.legend()

pred = model.predict(X_test)
plt.plot(Y_test, "x", label="real")
plt.plot(pred, label="pred")
plt.legend();
plt.show()

#### try to predict the trade volume ####
X_train, X_test, y_train, vy_test = train_test_split(X, vY, test_size=0.20, random_state=44)

lr = LinearRegression().fit(X_train, y_train)
c = lr.coef_
print(lr.coef_, lr.intercept_)
print(lr.coef_[-1])

pred = lr.predict(X_test)
plt.plot(vy_test, "x", label="real")
plt.plot(pred, label="pred")
plt.legend();
plt.show()
