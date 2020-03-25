import os
import pickle

from apis.worldtradingdata_com import WtdsDataSource

def load_historical_data(symbol):

    ds = WtdsDataSource()

    r = ds.get_history(symbol)

    try:
        os.mkdir("data/"+symbol)
    except:
        pass
    file_path = "data/"+symbol+"/history.pckl"
    with open(file_path, "wb") as fp:
        pickle.dump(r.json(), fp)
        fp.close()

def load_intraday_data(symbol, interval=5, timeframe=30):
    ds = WtdsDataSource()

    file_path = "data/" + symbol + "/intraday.pckl"
    r = ds.get_intraday(symbol, interval, timeframe)

    with open(file_path, "wb") as fp:
        pickle.dump(r.json(), fp)
        fp.close()
