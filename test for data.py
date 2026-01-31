import pandas as pd
file = pd.read_csv(r"C:\Users\Chinh\Downloads\Binance_ALGOUSDT_2023_minute.csv",index_col=0)
print(file.info())
file.index = pd.to_datetime(file.index)
file.to_csv(r"C:\Users\Chinh\Downloads\Binance_ALGOUSDT_2023_minute.csv")