import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

def send_email(recipient_email, subject, body, sender_email=email, app_password=password):
    """belirtilen email adresine posta gönderir"""
    try:
        # E-posta mesajını oluştur
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # SMTP sunucusuna bağlan
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
            print("E-posta başarıyla gönderildi!")
    except Exception as e:
        print(f"E-posta gönderiminde hata oluştu: {e}")
