import streamlit as st
from utils import utils

st.title("Credit risk modelling app")

st.write("## Parameters")
col1, col2, col3 = st.columns(3)

dti_ratio = col1.number_input("DTI", min_value=0.0, max_value=1.0, value=0.0, step=0.01)
late_payments = col1.number_input("Late payments", min_value=0, max_value=12, value=0, step=1)
job_years = col1.number_input("Job years", min_value=0, max_value=25, value=0, step=1)

