# import smtplib
# from threading import Thread
# from email.mime.text import MIMEText

# SENDER_EMAIL = "doanthanhtuyen0330@gmail.com"
# SENDER_APP_PASSWORD = "qykm zzuf lofo aumf"

# def _send(email, otp):
#     msg = MIMEText(f"OTP của bạn: {otp}\nHiệu lực 5 phút.", "plain", "utf-8")
#     msg["Subject"] = "Xác nhận OTP"
#     msg["From"] = SENDER_EMAIL
#     msg["To"] = email

#     server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
#     server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
#     server.send_message(msg)
#     server.quit()

# def send_otp_email(email, otp):
#     Thread(target=_send, args=(email, otp)).start()
# from threading import Thread


import os
from dotenv import load_dotenv
import resend
from threading import Thread

# Load ENV
load_dotenv()

# Lấy API KEY
resend.api_key = os.getenv("RESEND_API_KEY")

def _send(email, otp):
    params = {
        "from": "OTP Service <no-reply@mhtmh.id.vn>",
        "to": [email],
        "subject": "Mã OTP Xác Nhận",
        "text": f"OTP của bạn là: {otp}\nOTP có hiệu lực trong 5 phút.",
    }

    try:
        resend.Emails.send(params)
        print("Đã gửi OTP đến:", email)
    except Exception as e:
        print("Lỗi gửi email Resend:", e)


def send_otp_email(email, otp):
    Thread(target=_send, args=(email, otp)).start()
