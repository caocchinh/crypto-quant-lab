from GetFile import GetFile
import plotly.graph_objects as go

symbol = "LTCUSDT"
year = 2023
ltcusdt = GetFile([symbol], [year]).getColumn(["Open", "High", "Low", "Close", "Volume"], merge=False)[f"{symbol}_{year}"]

fig = go.Figure(data=[go.Candlestick(x=ltcusdt.index,  open=ltcusdt["Open"],
                high=ltcusdt["High"],
                low=ltcusdt["Low"],
                close=ltcusdt["Close"])])
fig.update_layout(xaxis_rangeslider_visible=False)
fig.write_html("file.html")
