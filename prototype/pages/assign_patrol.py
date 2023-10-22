import streamlit as st 
import os
from supabase import create_client, Client
import pandas as pd 
import datetime

url: str = "https://vjreddkwmtshsjyscxti.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZqcmVkZGt3bXRzaHNqeXNjeHRpIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTc3MDk5MzQsImV4cCI6MjAxMzI4NTkzNH0.lOuhmXyLOUvI6USzNvrOB8_zYXS8CSV7EaEjA3ADNO4"
supabase: Client = create_client(url, key)

guard_names = supabase.table('guard_data').select("name").execute()
patrol_places = supabase.table('patrol_places').select("name").execute()

with st.form("assign_patrols"):
    st.subheader("Assign Patrol")
    guard_name = st.selectbox("Guard Name", [x["name"] for x in guard_names.data])
    patrol_place = st.selectbox("Patrol Place", [x["name"] for x in patrol_places.data])
    start_date = st.date_input("Start Date")
    start_time = st.time_input("Start Time", step = 3600)
    end_date = st.date_input("End Date")
    end_time = st.time_input("End Time", step = 3600)


    submit = st.form_submit_button('Submit')
if submit:
    start_time_post = datetime.datetime.combine(start_date, start_time)
    end_time_post = datetime.datetime.combine(end_date, end_time)
    data, count = supabase.table('assignments').insert({ "guard_name": guard_name, "patrol_place": patrol_place, "start_time": start_time_post.isoformat(), "end_time": end_time_post.isoformat()}).execute()

