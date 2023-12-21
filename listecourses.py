import streamlit as st
from app_func import get_dataframe, data_form

st.title('Liste de courses')

current_data = get_dataframe()

st.dataframe(current_data)

data_form(current_data)