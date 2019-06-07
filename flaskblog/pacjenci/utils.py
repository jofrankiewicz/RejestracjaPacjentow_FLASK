import os
import secrets
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail


def send_reset_email(pacjent):
    token = pacjent.get_reset_token()
    msg = Message('Zresetuj hasło',
                  sender='noreply@demo.com',
                  recipients=[pacjent.email])
    msg.body = f'''W celu zresetowania hasła, otwórz podany link:
{url_for('pacjenci.reset_token', token=token, _external=True)}

Jeśli nie chciałeś zmienić swojego hasła, zignoruj tę wiadomość.
'''
    mail.send(msg)
