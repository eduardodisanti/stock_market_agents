import requests
import json
import time
import pandas as pd
import matplotlib.pyplot as plt
import deepdish as dd

from apis.worldtradingdata_com import WtdsDataSource

SYMBOL = "SPCE"
PAUSE_TICKER = 60

hist = []
prs = []

ds = WtdsDataSource()

for a in range(1):
    d = ds.get_live("SPCE")
    p = float(d['data'][0]['price'])
    prs.append(p)
    hist.append(d)
    plt.plot(prs)
    print(p)
    plt.pause(PAUSE_TICKER)
    #dd.io.save(history_path, hist)
    #dd.io.save(price_path, prs)
