import pandas
import plotly.express as px
import pandas as pd

year = []
No_Smoothing = []
Lowess = []

with open(r"/home/caocchinh/Downloads/Bitcoin/Plot/data.giss.nasa.gov_gistemp_graphs_graph_data_Global_Mean_Estimates_based_on_Land_and_Ocean_Data_graph.txt","r") as file:
    for line in file.readlines():
        if len(line.strip().split("     ")) == 3:
            year.append(line.strip().split("     ")[0])
            No_Smoothing.append(line.strip().split("     ")[1])
            Lowess.append(line.strip().split("     ")[2])

df = pandas.DataFrame({
    "Year": year,
    "No_Smoothing":No_Smoothing,
    "Lowess":Lowess
})

fig = px.line(df, x="Year", y="No_Smoothing", color='Lowess')
fig.show()
