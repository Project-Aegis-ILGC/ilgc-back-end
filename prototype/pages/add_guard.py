import streamlit as st 
import os
from supabase import create_client, Client
import pandas as pd 


# connecting with the database 

url: str = "https://vjreddkwmtshsjyscxti.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZqcmVkZGt3bXRzaHNqeXNjeHRpIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTc3MDk5MzQsImV4cCI6MjAxMzI4NTkzNH0.lOuhmXyLOUvI6USzNvrOB8_zYXS8CSV7EaEjA3ADNO4"
supabase: Client = create_client(url, key)

# user auth

supabase.auth.sign_in_with_password({"email": "shubhamjjj5@gmail.com", "password": "5MVDf!4SB2PfCV_"})


with st.form("Add Guard Data"):
   st.subheader("Add Guard Data")
   name = st.text_input("Guard Name")
   phone_number = st.text_input("Guard Phone Number")
   mac_address = st.text_input("Mac Address")
   submit = st.form_submit_button('Submit')

if submit:
   data, count = supabase.table('guard_data').upsert({ "name": name, "phone_number": phone_number, "mac_address": mac_address}).execute()


response = supabase.table('guard_data').select("name,phone_number,mac_address").execute()
table_data = response.data

st.subheader("Guards Data")
st.table(table_data)
