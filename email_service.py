import smtplib
from email.mime.text import MIMEText

SENDER_EMAIL = "poojithasadhanala@gmail.com"
APP_PASSWORD = "pgkc bxry stil nkni"  # ⚠️ CHANGE THIS AFTER TESTING

RECEIVER_EMAILS = [
    "246n1a05h3@sriniet.edu.in",
    "poojithasadhanala@gmail.com",
    "mahithagubbala117@gmail.com"
     #you can add as many emails as you want in this list 
]

def send_email_alert(medicine_name):
    subject = "⚠️ Missed Medicine Alert"
    body = f"You missed your medicine: {medicine_name}. Please stay consistent."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = ", ".join(RECEIVER_EMAILS)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAILS, msg.as_string())

        print(f"[EMAIL SENT] {medicine_name}")

    except Exception as e:
        print("[EMAIL ERROR]:", e)
