import streamlit as st 
import os
from supabase import create_client, Client
import pandas as pd 
import datetime
import json


def generate_time_buckets(df):

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
    new_data["Start Time"] = pd.to_datetime(new_data["Start Time"])
    new_data["End Time"] = pd.to_datetime(new_data["End Time"])
    return new_df



url: str = "https://vjreddkwmtshsjyscxti.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZqcmVkZGt3bXRzaHNqeXNjeHRpIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTc3MDk5MzQsImV4cCI6MjAxMzI4NTkzNH0.lOuhmXyLOUvI6USzNvrOB8_zYXS8CSV7EaEjA3ADNO4"
supabase: Client = create_client(url, key)
date_format = "%Y/%m/%d %H:%M:%S"


patrol_status = supabase.table('assignments').select("*").execute() # fetch all data 
patrol_df = pd.DataFrame(patrol_status.data) # make df

routers_data = supabase.table('routers').select("*").execute()
routers_df = pd.DataFrame(routers_data.data)

patrol_places_data = supabase.table('patrol_places').select("*").execute()
patrol_places_df = pd.DataFrame(patrol_places_data.data)
if patrol_df.shape[0] > 0:
    unpatrolled = patrol_df.loc[patrol_df["completed"] == False] # wanna verify their patrols

    all_guards_data = supabase.table('guard_data').select("*").execute()  # want everyone's phone numbers for finding xlsx
    guards_df = pd.DataFrame(all_guards_data.data)

    for i in range(patrol_df.shape[0]):
        patrol = patrol_df.loc[i, :]
        
        phone_number = guards_df.loc[guards_df["name"] == patrol["guard_name"], "phone_number"].iloc[0]

        wifi_data = pd.read_excel(f".\prototype\data\{phone_number}.xlsx")
        wifi_data = generate_time_buckets(wifi_data)
        wifi_data.to_excel("check.xlsx")
        wifi_data["Start Time"] = wifi_data["Start Time"].apply(lambda x: (datetime.datetime.strptime(x, date_format) + datetime.timedelta(seconds=19800)).timestamp())
        wifi_data["End Time"] = wifi_data["End Time"].apply(lambda x: (datetime.datetime.strptime(x, date_format) + datetime.timedelta(seconds=19800)).timestamp())
        patrol_start_time = datetime.datetime.fromisoformat(patrol_df.loc[patrol_df["id"] == patrol["id"], "start_time"].iloc[0])
        patrol_start_time = datetime.datetime.timestamp(patrol_start_time)
        
        
        patrol_end_time = datetime.datetime.fromisoformat(patrol_df.loc[patrol_df["id"] == patrol["id"], "end_time"].iloc[0])
        patrol_end_time = datetime.datetime.timestamp(patrol_end_time)
        patrol_place_name = patrol_df.loc[patrol_df["id"] == patrol["id"], "patrol_place"].iloc[0]
        router_names_at_patrol_place = patrol_places_df.loc[patrol_places_df["name"] == patrol_place_name, "router_names"].iloc[0]

        router_macs = routers_df.loc[routers_df["name"].isin(router_names_at_patrol_place) , "mac_address"]

        # filter according to location and time
        relevant_loc_time = wifi_data.loc[(wifi_data["Start Time"] >= patrol_start_time)  & (wifi_data["Start Time"] <= patrol_end_time) & (wifi_data["AP MAC Address"].isin(router_macs)), :]


        print(relevant_loc_time)
        if relevant_loc_time.shape[0] > 0:
            supabase.table('assignments').update({"completed": True}).eq("id", patrol["id"]).execute()

    # print(unpatrolled_guards)

patrol_status = supabase.table('assignments').select("*").execute()
patrol_status_df = pd.DataFrame(patrol_status.data).drop(["id"], axis = 1)
print(patrol_status_df)
patrol_status_df.loc[:, "start_time"] = patrol_status_df.loc[: , "start_time"].apply(lambda x : datetime.datetime.fromisoformat(x).strftime('%B %d, %Y, %H:%M'))
patrol_status_df.loc[:, "end_time"] = patrol_status_df.loc[:, "end_time"].apply(lambda x : datetime.datetime.fromisoformat(x).strftime('%B %d, %Y, %H:%M'))
patrol_status_df.loc[:, "created_at"] = patrol_status_df.loc[:, "created_at"].apply(lambda x : datetime.datetime.fromisoformat(x).strftime('%B %d, %Y, %H:%M'))

st.table(patrol_status_df)
