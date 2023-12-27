import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
from app_func import rayons

approved_receivers = ["F.H", "AS.H", "Félix"]

def email_export(liste_to_export, receiver, objet, comm, date):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = st.secrets["creds"]["sender"]
    smtp_password = st.secrets["creds"]["pwd"]

    # Informations sur l'email
    from_address = st.secrets["creds"]["sender"]
    if receiver in approved_receivers:
        if receiver == "F.H":
            to_address = st.secrets["creds"]["fh"]
        elif receiver == "AS.H":
            to_address = st.secrets["creds"]["as"]
        elif receiver == "Félix":
            to_address = st.secrets["creds"]["felix"]
    else:
        to_address = receiver
    subject = objet

    # Liste d'objets à inclure dans le corps du message
    ma_liste = liste_to_export

    # Créer l'objet MIMEMultipart
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject

    # Ajouter chaque item de la liste comme une nouvelle ligne dans le corps du message
    message_body = f"Date : {date}\n"

    if comm != "":
        message_body += f"\nCommentaire : {comm}\n"

    message_body += liste_to_export

    message_body += "\n\nFin de la liste."

    # Ajouter le corps du message à l'objet MIMEMultipart
    msg.attach(MIMEText(message_body, 'plain'))

    # Configurer la connexion SMTP
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        st.success(f"La liste a bien été envoyé à : {receiver}")

def list_to_export(actual_list):
    list_message = ""

    for cat in rayons:
        list_message += f"\n{cat.upper()} :\n"
        rayon_df = actual_list.loc[actual_list['Rayon'] == cat]
        rayon_df['Commentaire'] = rayon_df['Commentaire'].astype(str).replace('nan', "")

        for i, row in rayon_df.iterrows():
            # Créer la phrase
            phrase = f"{row['Article']}: {row['Quantité']} {row['Unité']}. "

            if rayon_df.loc[i, 'Commentaire'] != '':
                phrase += f"({rayon_df.loc[i, 'Commentaire']})"

            # Afficher la phrase
            list_message += "      "+phrase+"\n"
    return list_message