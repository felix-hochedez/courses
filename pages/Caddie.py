import streamlit as st
from app_func import get_rayon_data, get_dataframe, select_rayon_form, rayons, item_listing

st.write(f'# Caddie')

st.write(f'### Sélectionner la catégorie de produit:')
rayon_choice = st.selectbox('', options=rayons)

st.markdown('<hr style="size: 3">', unsafe_allow_html=True)
st.write(f'### Ajouter/Supprimer des articles du caddie:')

current_data = get_dataframe()
current_data['Commentaire'] = current_data['Commentaire'].astype(str).replace('nan', '')
rayon_df = get_rayon_data(current_data=current_data, rayon=rayon_choice)

select_rayon_form(current_data, rayon_choice)

st.markdown('<hr style="size: 3">', unsafe_allow_html=True)
st.write(f'### Aperçu de la sélection:')

selected_df = get_rayon_data(current_data, rayon_choice)
selected_df = selected_df.query('Quantité > 0')

if selected_df.shape[0]!=0:
    item_listing(selected_df)
else:
    st.warning('Cette catégorie ne contient actuellement aucun article')
