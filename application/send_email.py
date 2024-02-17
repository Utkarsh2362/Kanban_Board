import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import *
import os

SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "kanban_app@email.com"
SENDER_PASSWORD = ""



def send_email(to_mail, subject, msg, attachment=None):
    email = MIMEMultipart()
    email["From"] = SENDER_ADDRESS
    email["Subject"] = subject
    email["To"] = to_mail

    email.attach(MIMEText(msg, "html"))

    if attachment is not None:
        with open(attachment, "rb") as attachment_file:
            # adding file as an output stream
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment_file.read())
            encode_base64(part)

        part.add_header("Content-Disposition", f"attachment; filename={attachment[len('static/export_download/'):]}")
        email.attach(part)

    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(email)
    s.quit()
    if attachment is not None:
        os.remove(attachment)

    return True