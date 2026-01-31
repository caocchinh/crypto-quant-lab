import pandas as pd
technologies = {
    'Courses':["Spark","PySpark","Python","pandas"],
    'Fee' :[20000,25000,22000,24000],
    'Duration':['30day','40days','35days','60days'],
    'Discount':[1000,2300,2500,2000]
              }
index_labels=['r1','r2','r3','r4']
df = pd.DataFrame(technologies,index=index_labels)
df.drop(index=df.index[-1],axis=0,inplace=True)

print(df)