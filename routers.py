import pandas as pd 

df = pd.read_excel("hibah.xlsx")
df = df.loc[:, ["AP Name", "AP MAC Address"]]

df = df.drop_duplicates()

df.to_csv("routers.csv")