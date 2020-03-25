import time

import deepdish as dd
import matplotlib.pyplot as plt
import numpy as np
from keras.models import load_model

from apis.worldtradingdata_com import WtdsDataSource

symbol = "DAL"
ds = WtdsDataSource()

high = -10e10
low  = 10e10
hist = []
prs = []
prev_val = None
difa_ant = None
HOLD = 0
BUY = -1
SELL = 1
symbols={
            HOLD:".",
            BUY :"^",
            SELL:"v"
}
actions = [symbols[HOLD]]
model = load_model("../data/"+symbol+"/_model.h5")
scaler  = dd.io.load("../data/"+symbol+"/_scaler.h5")
preds = []
sells = []
buys  = []
for a in range(100):
    d = ds.get_live("DAL")
    p = float(d['data'][0]['price'])
    prs.append(p)
    hist.append(d)
    plt.plot(prs, label="real")
    plt.plot(preds, "v", label="pred")
    plt.plot(preds, "v", c='b', label="BUY", markevery=buys)
    plt.plot(preds, "^", c='r',label="SELL", markevery=sells)
    plt.legend()
    plt.pause(0.1)
    print(d)

    _open = float(d['data'][0]['price_open'])
    _price = float(d['data'][0]['price'])
    _high = float(d['data'][0]['day_high'])
    _low = float(d['data'][0]['day_low'])
    _volume = int(d['data'][0]['volume']) / 1000000

    if prev_val == None:
        prev_val = _price

    difa = _price - prev_val

    if difa < 0:
        action = SELL
        sells.append(a)
    elif difa > 0:
        action = BUY
        action = BUY
        buys.append(a)
    else:
        action = HOLD


    if difa != difa_ant:
        difa_ant = difa

    if _low < low:
        low = _low
    if _high > high:
        high = _high
    x = np.array([[_open, _price, high, low, _volume]])
    x = scaler.transform(x)
    x = np.reshape(x, (x.shape[0], 1, x.shape[1]))

    pred = model.predict(x)
    preds.append(pred[0])

    next_action = pred[0] - _price
    print("Next", pred[0], "dif", difa, "vector", x, "act", action, "next act", next_action)
    prev_val = _price
    time.sleep(300)