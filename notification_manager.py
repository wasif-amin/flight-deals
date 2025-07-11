import smtplib
import os
from dotenv import load_dotenv
class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        load_dotenv()
        self.EMAIL = os.environ.get("EMAIL")
        self.PASSWORD = os.environ.get("PASSWORD")
        self.RECIPIENT = os.environ.get("RECIPIENT")

    def send_email(self, body):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection = smtplib.SMTP("smtp.gmail.com")
            connection.starttls()
            connection.login(user=self.EMAIL, password=self.PASSWORD)
            connection.sendmail(
            from_addr=self.EMAIL,
            to_addrs=self.RECIPIENT,
            msg=body
        )



