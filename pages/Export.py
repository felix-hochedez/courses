import streamlit as st
from app_func import get_rayon_data, get_dataframe, select_rayon_form, rayons, item_listing
from export_func import email_export, list_to_export
from Paramètres import date_courses

st.write(f'# Aperçu et Export')

st.write(f'## Aperçu de la liste complète:')
current_data = get_dataframe()

actual_list = current_data.query('Quantité > 0')

for cat in rayons:
    rayon_df = actual_list.loc[actual_list['Rayon'] == cat]
    rayon_df['Commentaire'] = rayon_df['Commentaire'].astype(str).replace('nan', "")

    if rayon_df.shape[0] != 0:
        st.write(f'#### {cat}:')

    item_listing(rayon_df)

st.markdown('<hr style="size: 3">', unsafe_allow_html=True)

st.write(f'## Commentaire global (facultatif):')
comment_global = st.text_area('Rédiger un commentaire général sur la liste:')

st.markdown('<hr style="size: 3">', unsafe_allow_html=True)
st.write(f'## Export:')

formated_date = date_courses.strftime('%d/%m/%Y')
mail_object = f'{formated_date} - Liste de courses.'
receiver = st.selectbox('Entrer le destinataire:', ["Félix", "F.H", "AS.H"])
email_receiver = st.text_input("Ou taper l'adresse manuellement (laisser vide sinon):", value="")
email_body = list_to_export(actual_list)
mdp = st.text_input("Rentrer le mot de passe pour envoyer:", value="", type="password")

if email_receiver != "":
    actual_receiver = email_receiver
else:
    actual_receiver = receiver

if st.button('Envoyer'):
    if mdp == st.secrets['creds']['mdp']:
        email_export(email_body, actual_receiver, mail_object, comment_global, formated_date)
    else:
        st.warning("Mot de passe incorrect.")
        st.stop()