import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email_alert(subject, body):

    sender_email = "csitnic@gmail.com"
    receiver_email = "csitnic@gmail.com"

    # 🔴 PAROLA APP (NU parola normala Gmail)
    password = "vmrf ezka prxr midh"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()

        print("Email trimis cu succes!")

    except Exception as e:
        print("Eroare trimitere email:", e)