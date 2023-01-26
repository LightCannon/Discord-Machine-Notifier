import smtplib
import ssl 
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime
import time


def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset

class EmailSender():
    def __init__(self):
        self.s = None
        
    def init_email_client(self):
        # context=ssl.SSLContext(ssl.PROTOCOL_TLS)

        self.s = smtplib.SMTP(host=os.getenv('EMAIL_HOST'),
                              port=int(os.getenv('EMAIL_PORT')))
        self.s.ehlo()
        self.s.starttls()
        self.s.ehlo()
        self.s.login(user=os.getenv('EMAIL_SENDER'), 
                     password=os.getenv('EMAIL_PASSWORD'))

    def send_notification_msg(self, message):
        try:
            self.init_email_client()
            msg = MIMEText(message, 'html')
            msg['Subject'] = f'Important Message From {message.split()[0]}'
            msg['From'] = os.getenv('EMAIL_SENDER')
            msg['To'] = os.getenv('EMAIL_RECEIVER')
            print(message)
            self.s.sendmail(os.getenv('EMAIL_SENDER'), os.getenv('EMAIL_RECEIVER'), msg.as_string())
            self.s.quit()

        except smtplib.SMTPServerDisconnected as e:
            self.s.quit()
