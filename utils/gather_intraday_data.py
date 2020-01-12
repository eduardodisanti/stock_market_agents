import pickle

from apis.worldtradingdata_com import WtdsDataSource

SYMBOL = "SPCE"
PAUSE_TICKER = 60

hist = []
prs = []

ds = WtdsDataSource()

file_path = "data/SPCE/intraday_20200110.pckl"
r = ds.get_intraday(SYMBOL, 5, 30)

with open(file_path, "wb") as fp:
    pickle.dump(r.json(), fp)
    fp.close()
    