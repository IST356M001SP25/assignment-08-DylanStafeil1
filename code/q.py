import streamlit as st
import pandas as pd

df = pd.read_csv('cache/final_cuse_parking_violations.csv')
st.dataframe(df)