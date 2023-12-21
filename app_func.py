import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Connection GSheets
global conn
conn = st.connection("gsheets", type=GSheetsConnection)

def get_dataframe():
    #Lire les données existantes
    existing_data = conn.read(worksheet="articles", usecols=list(range(5)), ttl=5)
    existing_data = existing_data.dropna(how="all")

    return existing_data

def data_form(current_data):
    rayons = [
        'Fruits & Légumes',
        'Boucherie'
        'Boulangerie'
    ]
    units = [
        'Non précisé',
        'Unité(s)',
        'g', 'kg', 'Litre(s)'
    ]

    with st.form(key="data_entry"):
        article_name = st.text_input(label="Nom de l'article*")
        article_unit = st.selectbox('Unité*', options=units)
        article_rayon = st.selectbox('Rayon*', options=rayons)
        comment = st.text_area(label='Commentaire')

        submit_button = st.form_submit_button(label="Enregistrer l'article")

        if submit_button:
            if not article_name:
                st.warning("Un ou plusieurs champs obligatoires sont manquants.")
                st.stop()
            elif current_data['Article'].str.contains(article_name).any():
                st.warning('Cet article semble déjà exister.')
                st.stop()
            else:
                #Créer un df pour le nouveau produit
                new_article = pd.DataFrame(

                    [
                        {
                            "Article": article_name,
                            "Quantité": "",
                            "Unité": article_unit,
                            "Rayon": article_rayon,
                            "Commentaire": comment,
                        }
                    ]

                )

                #Ajouter le produit à la bdd existante
                updated_df = pd.concat([current_data, new_article], ignore_index=True)

                #Update le Gsheet
                conn.update(worksheet="articles", data=updated_df)
                st.success("L'article a bien été enregistré !")