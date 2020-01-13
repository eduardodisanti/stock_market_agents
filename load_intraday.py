from gather_history_data import load_historical_data, load_intraday_data

SYMBOLS = ['JNJ']
for symbol in SYMBOLS:
    print("Loading", symbol)
    load_intraday_data(symbol)
