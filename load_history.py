from gather_history_data import load_historical_data


SYMBOLS = ['DAL','KO','FCAU']
for symbol in SYMBOLS:
    print("Loading", symbol)
    load_historical_data(symbol)