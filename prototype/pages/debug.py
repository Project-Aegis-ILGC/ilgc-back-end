import streamlit as st 
import os

with st.form("debug_form"):
    code = st.text_input("shell commands")
    submit = st.form_submit_button()
if submit:
    print(os.system(code))