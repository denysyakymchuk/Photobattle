import smtplib
import ssl
from email.message import EmailMessage


class Email:
    def __init__(self):
        self.email_sender = 'instamaninov@gmail.com'
        self.ema_password = 'bzaemtnlmmuwqpof'

    def verif(self, email_receiver, unique):
        subject = 'Verify email'
        body = 'http:127.0.0.1:8000/verification-email/' + unique
        em = EmailMessage()
        em['From'] = self.email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(self.email_sender, self.ema_password)
            smtp.sendmail(self.email_sender, email_receiver, em.as_string())

    def reset_password_u(self, email_receiver, unique):
        subject = 'Reset password'
        body = 'http:127.0.0.1:8081/reset-password/' + unique
        em = EmailMessage()

        em['From'] = self.email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(self.email_sender, self.ema_password)
            smtp.sendmail(self.email_sender, email_receiver, em.as_string())
