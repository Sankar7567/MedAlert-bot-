import smtplib
from email.mime.text import MIMEText

SENDER_EMAIL = "poojithasadhanala@gmail.com"
APP_PASSWORD = "pgkc bxry stil nkni" # Use an app password for Gmail
RECEIVER_EMAIL = "246n1a05h3@sriniet.edu.in"

def send_email_alert(medicine_name):
    subject = "⚠️ Missed Medicine Alert"
    body = f"You missed your medicine: {medicine_name}. Please stay consistent."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

        print("Email alert sent!")

    except Exception as e:
        print("Email failed:", e)
