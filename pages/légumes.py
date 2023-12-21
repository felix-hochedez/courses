import streamlit as st
from app_func import get_rayon_data, get_dataframe, select_rayon_form

st.title('Fruits & Légume')
current_data = get_dataframe()
legume_df = get_rayon_data(current_data=current_data, rayon="Fruits & Légumes")

select_rayon_form(current_data, legume_df)

selected_df = get_rayon_data(current_data, 'Fruits & Légumes')
selected_df = selected_df.query('Quantité > 0')
st.table(selected_df)