import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# on rentre les renseignements pris sur le site du fournisseur
smtp_address = 'smtp.gmail.com'
smtp_port = 465

# on rentre les informations sur notre adresse e-mail
email_address = 'keracles000@gmail.com'
email_password = 'uxdrxnqvlxlhcrbv'



def envoie_mail(email_receiver, subject, contenu_mail, smtp_address=smtp_address, smtp_port=smtp_port, email_address=email_address, email_password=email_password):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = email_address
    message["To"] = email_receiver
    texte_mime = MIMEText(contenu_mail, 'plain')
    message.attach(texte_mime)


    # on crée la connexion
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_address, smtp_port, context=context) as server:
        # connexion au compte
        server.login(email_address, email_password)
        # envoi du mail
        server.sendmail(email_address, email_receiver, message.as_string())
        server.quit()


def creation_mail(findings):
    final_str = ''
    for str in findings :
        final_str = final_str + "\n" + str
    
    texte = f'''
        Hello !

        Voici les surebets trouvés : 
        {final_str}

        Vas-y régale-toi !

        Keracles,
        Un plaisir.
        '''
    return texte