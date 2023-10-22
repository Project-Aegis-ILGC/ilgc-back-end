import pandas as pd 

df = pd.read_excel("hibah.xlsx")

print(df.loc[:, ["Time", "Type", "AP Name", "AP MAC Address"]])

new_data  = {"Start Time" : [], "End Time": [], "AP Name" : [], "AP MAC Address" : []}

nrows = df.shape[0]
if df.loc[nrows - 1, "Type"] == "Client connection timed out":
    df = df.loc[:nrows - 1, :]
nrows = df.shape[0]
start_time = df.loc[nrows - 1, "Time"]
end_time =  None
curr_ap_mac = df.loc[nrows - 1, "AP MAC Address"] 
curr_ap_name = df.loc[nrows  - 1, "AP Name"]

for i in range(nrows - 1, -1, -1):
    tmp = df.loc[i, "AP MAC Address"]
    if curr_ap_mac != tmp: # AP change
        new_data["Start Time"].append(start_time)
        new_data["End Time"].append(df.loc[i, "Time"])
        new_data["AP MAC Address"].append(curr_ap_mac)
        new_data["AP Name"].append(curr_ap_name)
        start_time = df.loc[i, "Time"]
        curr_ap_mac = tmp
        curr_ap_name = df.loc[i, "AP Name"]
    if df.loc[i, "Type"] == "Client connection timed out":
        new_data["Start Time"].append(start_time)
        new_data["End Time"].append(df.loc[i, "Time"])
        new_data["AP Name"].append(df.loc[i, "AP Name"])
        new_data["AP MAC Address"].append(df.loc[i, "AP MAC Address"])
        start_time = df.loc[i - 1, "Time"]
        curr_ap_mac = df.loc[i - 1, "AP MAC Address"]
        curr_ap_name = df.loc[i - 1, "AP Name"]
        i -= 1 
        continue
for i in new_data:
    new_data[i].reverse()
new_df = pd.DataFrame(new_data)
new_df.to_excel("HIABH HAS BEEN REVISED.xlsx")
print(new_df)
        



