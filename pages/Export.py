import streamlit as st
from app_func import get_rayon_data, get_dataframe, select_rayon_form, rayons, item_listing

st.write(f'# Aperçu et Export')

st.write(f'## Commentaire global (facultatif):')
comment_global = st.text_area('Rédiger un commentaire général sur la liste:')

st.markdown('<hr style="size: 3">', unsafe_allow_html=True)

st.write(f'## Aperçu de la liste complète:')
current_data = get_dataframe()

actual_list = current_data.query('Quantité > 0')

for cat in rayons:
    rayon_df = actual_list.loc[actual_list['Rayon'] == cat]
    rayon_df['Commentaire'] = rayon_df['Commentaire'].astype(str).replace('nan', "")

    if rayon_df.shape[0] != 0:
        st.write(f'#### {cat}:')

    item_listing(rayon_df)