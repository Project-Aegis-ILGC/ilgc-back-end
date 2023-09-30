import pandas as pd 
file_name = "hibah"
# open file and club data
with open(f"{file_name}.txt") as file:
    lines = [line.strip() for line in file.readlines() if line.strip() != ""]
new = []
for i in range(0, len(lines), 5):
    new.append(lines[i:i+5])

# creating df and dropping irrelevant rows

df = pd.DataFrame(new, columns=["Time", "Code", "Type", "Severity", "Activity"])

# REGULAR EXPRESSIONS!!
patterns = {}
patterns["236"] = {
    "user_id":r'\[([^\@]+)@',
    "global_ip":r'@([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)@',
    "user_mac":r'@([0-9A-Fa-f\:]+)\]',
    "router_name":r'AP \[([^\@]+)@',
    "router_mac": r'@([0-9A-Fa-f\:]+)\]\.'
}

patterns["205"] = {
    "user_id": r'Client \[([^\]]+)\] disconnected',
    "router_name": r'AP \[([^\@]+)@',
    "router_mac": r'@([0-9A-Fa-f\:]+)\]'
}
attrs = ["User ID", "Global IP", "User MAC Address", "AP Name", "AP MAC Address"]
df = df.loc[(df["Code"] == "236") | (df["Code"] == "205"), :]
for attr in attrs:
    df[attr] = "NA"

df.loc[df["Code"] == "236", "User ID"] = df.loc[df["Code"] == "236", "Activity"].str.extract(patterns["236"]["user_id"]).values
df.loc[df["Code"] == "236","Global IP"] = df.loc[df["Code"] == "236", "Activity"].str.extract(patterns["236"]["global_ip"]).values
df.loc[df["Code"] == "236","User MAC Address"] = df.loc[df["Code"] == "236", "Activity"].str.extract(patterns["236"]["user_mac"]).values
df.loc[df["Code"] == "236","AP Name"] = df.loc[df["Code"] == "236", "Activity"].str.extract(patterns["236"]["router_name"]).values
df.loc[df["Code"] == "236","AP MAC Address"] = df.loc[df["Code"] == "236", "Activity"].str.extract(patterns["236"]["router_mac"]).values


df.loc[df["Code"] == "205", "User ID"] = df.loc[df["Code"] == "205", "Activity"].str.extract(patterns["205"]["user_id"]).values
df.loc[df["Code"] == "205", "AP Name"] = df.loc[df["Code"] == "205", "Activity"].str.extract(patterns["205"]["router_name"]).values
df.loc[df["Code"] == "205", "AP MAC Address"] = df.loc[df["Code"] == "205", "Activity"].str.extract(patterns["205"]["router_mac"]).values

# df = df.d], axis = 1)
df = df.reset_index(drop = True)
df.to_excel(f"{file_name}.xlsx")

