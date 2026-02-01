from datetime import datetime, timedelta

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates
from GetFile import GetFile

plt.style.use('mpl15')

# dates = [
#     datetime(2019, 5, 24),
#     datetime(2019, 5, 25),
#     datetime(2019, 5, 26),
#     datetime(2019, 5, 27),
#     datetime(2019, 5, 28),
#     datetime(2019, 5, 29),
#     datetime(2019, 5, 30)
# ]
#
# y = [0, 1, 3, 4, 6, 5, 7]
#
# plt.plot_date(dates,y,linestyle="solid")
# plt.gcf().autofmt_xdate()
# date_format = mpl_dates.DateFormatter("%b, %d, %Y")
# plt.gca().xaxis.set_major_formatter(date_format)

ethereum = GetFile(["ETHUSDT"],[2021]).getColumn(["Close"],merge=False)["ETHUSDT_2021"]
ethereum.index = pd.to_datetime(ethereum.index)
price_date = ethereum.index
price_close = ethereum

plt.plot_date(price_date,price_close,linestyle="solid",marker=None)
plt.gcf().autofmt_xdate()

plt.title('Ethereum Prices')
plt.xlabel('Date')
plt.ylabel('Closing Price')

plt.tight_layout()

plt.show()