import streamlit as st
from utils import utils

st.title("Credit risk modelling app")

st.write("## Parameters")
col1, col_spanned = st.columns([1, 3])

with col1:
    population_sample = st.number_input("Population", min_value=100, max_value=10000, value=1000, step=10)
    dti_ratio = st.number_input("DTI", min_value=0.0, max_value=1.0, value=0.3, step=0.01)
    late_payments = st.number_input("Late payments", min_value=0, max_value=12, value=1, step=1)
    job_years = st.number_input("Job years", min_value=0, max_value=25, value=6, step=1)

viz = utils.calculations(population_sample, dti_ratio, late_payments, job_years)
with col_spanned:
    st.pyplot(viz)

