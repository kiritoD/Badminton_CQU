import smtplib
from email.header import Header
from email.mime.text import MIMEText


def send_email(
    email_smtp_server: str,
    email_smtp_username: str,
    email_smtp_password: str,
    email_smtp_port: int,
    recipient: str,
    subject: str,
    body: str,
):
    """
    Send an email using the specified SMTP server.
    """
    FROM = email_smtp_username
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    me = f"Badminton <{email_smtp_username}>"
    message = MIMEText(body, "plain", "utf-8")
    message["Subject"] = Header(subject, "utf-8")

    message["From"] = me
    message["To"] = f"<{recipient}>"
    # message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    # """ % (
    #     FROM,
    #     ", ".join(TO),
    #     SUBJECT,
    #     TEXT,
    # )

    print(1)
    server = smtplib.SMTP(email_smtp_server, email_smtp_port)
    print(2)
    server.ehlo()
    print(3)
    server.starttls()
    print(1)
    server.login(email_smtp_username, email_smtp_password)
    print(2)
    server.sendmail(FROM, TO, message.as_string())
    print(3)
    server.close()
    return True


import base64

send_email(
    "smtp.qq.com",
    "1169394593@qq.com",
    "folkkxguhohgbaca",
    587,
    "18323224032@163.com",
    "test",
    "hello world\n djw ---------你好-+\n|".encode("utf-8"),
)
