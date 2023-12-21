import streamlit as st
from app_func import get_dataframe, data_form
from datetime import datetime, timedelta

st.title('Liste de courses')

st.write(f"## Ajout d'article au magasin:")

current_data = get_dataframe()
current_data['Commentaire'] = current_data['Commentaire'].astype(str).replace('nan', '')

data_form(current_data)

st.markdown('<hr style="size: 3">', unsafe_allow_html=True)

st.write(f"## Date de course:")

today = datetime.today()

# Définir la date par défaut sur le prochain samedi
next_saturday = today + timedelta(days=5 - today.weekday())

# Afficher le sélecteur de date
date = st.date_input("Sélectionnez une date", value=next_saturday)