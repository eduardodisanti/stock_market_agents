import pickle

from apis.worldtradingdata_com import WtdsDataSource

SYMBOL = "AMZN"
PAUSE_TICKER = 60

hist = []
prs = []

ds = WtdsDataSource()

r = ds.get_history(SYMBOL)

file_path = "data/"+SYMBOL+"/history.pckl"
with open(file_path, "wb") as fp:
    pickle.dump(r.json(), fp)
    fp.close()
