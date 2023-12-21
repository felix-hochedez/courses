import streamlit as st
from app_func import get_rayon_data, select_rayon_form, get_dataframe

st.title('Boucherie')
current_data = get_dataframe()

boucherie_df = get_rayon_data(current_data=current_data, rayon="Boucherie")

select_rayon_form(current_data, boucherie_df)

selected_df = get_rayon_data(current_data, 'Boucherie')
selected_df = selected_df.query('Quantité > 0')
st.table(selected_df)
