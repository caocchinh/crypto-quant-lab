from FormatRegulator import FormatRegulator
from GetFile import GetFile\

if __name__ == "__main__":
    path = GetFile("all","all",dropCol="blank").removeCol()
# \    # a = FormatRegulator([r"C:\Users\Chinh\Downloads\Binance_AAVEETH_d.csv"], sortType="ascending", cryptoWatch=True, dropCol=None, checkDefault=False).modifyCSV()
