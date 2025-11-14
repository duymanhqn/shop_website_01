import smtplib
from threading import Thread
from email.mime.text import MIMEText

SENDER_EMAIL = "doanthanhtuyen0330@gmail.com"
SENDER_APP_PASSWORD = "qykm zzuf lofo aumf"

def _send(email, otp):
    msg = MIMEText(f"OTP của bạn: {otp}\nHiệu lực 5 phút.", "plain", "utf-8")
    msg["Subject"] = "Xác nhận OTP"
    msg["From"] = SENDER_EMAIL
    msg["To"] = email

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
    server.send_message(msg)
    server.quit()

def send_otp_email(email, otp):
    Thread(target=_send, args=(email, otp)).start()
