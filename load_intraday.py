from gather_history_data import load_historical_data, load_intraday_data

SYMBOLS = ['FCAU', 'JNJ', 'SPCE', 'TLRD']
for symbol in SYMBOLS:
    print("Loading", symbol)
    load_intraday_data(symbol, interval=15)
