import smtplib
import os
from email.message import EmailMessage
import json


def notification(message):
    try:
        message = json.loads(message)
        mp3_fid = message["mp3_fid"]
        sender_address = os.environ.get("GMAIL_ADDRESS")
        sender_password = os.environ.get("GMAIL_PASSWORD")
        receiver_address = message["username"]

        msg = EmailMessage()
        msg.set_content(f"mp3 file ready: {mp3_fid} is now ready")
        msg["Subject"] = "mp3 file ready"
        msg["From"] = sender_address
        msg["To"] = receiver_address

        session = smtplib.SMTP("smtp.office365.com", port=587)
        session.starttls()

        session.login(sender_address, sender_password)
        session.send_message(msg, sender_address, receiver_address)
        session.quit()

        print("email sent")
    except Exception as err:
        print("email error: ", err)
        return err
