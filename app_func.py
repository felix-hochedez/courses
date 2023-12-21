import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Connection GSheets
global conn, rayons, units
conn = st.connection("gsheets", type=GSheetsConnection)

rayons = [
        'Fruits & Légumes',
        'Boucherie',
        'Boulangerie'
    ]
units = [
    'Non précisé',
    'Unité(s)',
    'g', 'kg', 'Litre(s)'
]

def get_dataframe():
    #Lire les données existantes
    existing_data = conn.read(worksheet="articles", usecols=list(range(5)), ttl=5)
    existing_data = existing_data.dropna(how="all")

    return existing_data

def data_form(current_data):

    actions = st.selectbox("Choisir une action:",
                           [
                               "Ajouter un article",
                               "Modifier un article",
                               'Supprimer un article',
                               'Voir tous les articles'
                           ]
    )

    if actions == 'Ajouter un article':
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
                                "Quantité": 0,
                                "Unité": article_unit,
                                "Rayon": article_rayon,
                                "Commentaire": comment,
                            }
                        ]

                    )

                    #Ajouter le produit à la bdd existante
                    updated_df = pd.concat([current_data, new_article], ignore_index=True)
                    updated_df = updated_df.sort_values('Article')

                    #Update le Gsheet
                    conn.update(worksheet="articles", data=updated_df)
                    st.success("L'article a bien été enregistré !")

    elif actions == "Modifier un article":

        to_update = st.selectbox("Selectionner l'article à modifier:",
                                 options=current_data['Article'].tolist())
        item_data = current_data[current_data['Article'] == to_update].iloc[0]

        with st.form(key='update_form'):
            article_name = st.text_input(label="Nom de l'article*", value=item_data['Article'])
            article_unit = st.selectbox('Unité*', options=units, index=units.index(item_data['Unité']))
            article_rayon = st.selectbox('Rayon*', options=rayons, index=rayons.index(item_data['Rayon']))
            comment = st.text_area(label='Commentaire', value=item_data['Commentaire'])

            update_button = st.form_submit_button(label = 'Enregistrer les modifications.')
            if update_button:
                if not article_name:
                    st.warning("Un ou plusieurs champs obligatoires sont manquants.")

                else:
                    current_data.drop(current_data[current_data['Article']==item_data['Article']].index,
                                      inplace=True)

                    #Check le commentaire
                    if comment=='nan':
                        comment_value = ""
                    else:
                        comment_value = comment

                    #Chek la quantité
                    if item_data['Quantité']=="":
                        quantity_value = ""
                    else:
                        quantity_value = item_data['Quantité']

                    updated_article = pd.DataFrame(

                        [
                            {
                                "Article": article_name,
                                "Quantité": quantity_value,
                                "Unité": article_unit,
                                "Rayon": article_rayon,
                                "Commentaire": comment_value,
                            }
                        ]

                    )

                    updated_df = pd.concat([current_data, updated_article], ignore_index=True)
                    updated_df = updated_df.sort_values('Article')

                    conn.update(worksheet='articles', data=updated_df)
                    st.success("L'article a bien été modifié.")

    elif actions == 'Voir tous les articles':
        display_df = current_data.loc[:, ['Article', 'Unité', 'Rayon', 'Commentaire']]
        st.dataframe(display_df)

    elif actions == 'Supprimer un article':
        to_delete = st.selectbox("Selectionner l'arcticle à supprimer", options=current_data['Article'].tolist())

        if st.button('Supprimer'):
            current_data.drop(
                current_data[current_data["Article"]== to_delete].index,
                inplace=True
            )
            conn.update(worksheet='articles', data=current_data)
            st.success("L'article a bien été supprimé.")

def get_rayon_data(current_data, rayon):
    rayon_df = current_data.loc[current_data['Rayon']==rayon]
    rayon_df = rayon_df.dropna(how="all")

    return rayon_df

def select_rayon_form(current_data, rayon_data):

    actions = st.selectbox("Choisir une action:",
                           [
                               "Ajouter un article à la liste",
                               'Retirer un article de la liste',
                           ]
                           )

    if actions == "Ajouter un article à la liste":

        selected = st.selectbox("Selectionner l'article", options=rayon_data['Article'].tolist())
        item_data = rayon_data[rayon_data['Article'] == selected].iloc[0]

        with st.form(key='rayon_form'):
            st.write(f'Article: {selected}')
            quantity = st.number_input('Quantité', min_value=0, step=1, value=int(item_data['Quantité']))
            st.write(f'Untité: {item_data["Unité"]}')
            comment = st.text_area(label='Commentaire', value=item_data['Commentaire'])

            add_button = st.form_submit_button(label="Ajouter l'article.")
            if add_button:
                if quantity <= 0:
                    st.warning("La quantité est invalide.")
                    st.stop()

                else:
                    current_data.drop(current_data[current_data['Article'] == item_data['Article']].index,
                                      inplace=True)
                    if comment == 'nan':
                        comment_value = ""
                    else:
                        comment_value = comment

                    updated_article = pd.DataFrame(

                        [
                            {
                                "Article": item_data['Article'],
                                "Quantité": quantity,
                                "Unité": item_data['Unité'],
                                "Rayon": item_data['Rayon'],
                                "Commentaire": comment_value,
                            }
                        ]

                    )

                    updated_df = pd.concat([current_data, updated_article], ignore_index=True)
                    updated_df = updated_df.sort_values('Article')

                    conn.update(worksheet='articles', data=updated_df)
                    st.success("L'article a bien été ajouté à la liste.")

    elif actions == 'Retirer un article de la liste':

        selected = st.selectbox("Selectionner l'article à supprimer", options=rayon_data['Article'].tolist())
        item_data = rayon_data[rayon_data['Article'] == selected].iloc[0]

        add_button = st.button(label="Supprimer l'article.")
        if add_button:
            current_data.drop(current_data[current_data['Article'] == item_data['Article']].index,
                              inplace=True)
            if item_data['Commentaire'] == 'nan':
                comment_value = ""
            else:
                comment_value = item_data['Commentaire']

            updated_article = pd.DataFrame(

                [
                    {
                        "Article": item_data['Article'],
                        "Quantité": 0,
                        "Unité": item_data['Unité'],
                        "Rayon": item_data['Rayon'],
                        "Commentaire": comment_value,
                    }
                ]

            )

            updated_df = pd.concat([current_data, updated_article], ignore_index=True)
            updated_df = updated_df.sort_values('Article')

            conn.update(worksheet='articles', data=updated_df)
            st.success("L'article a bien été retiré à la liste.")


