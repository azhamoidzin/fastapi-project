"""
Common functions for sending emails
"""

import smtplib
from email.mime.text import MIMEText

from app.config import settings


def send_email(email: str | list[str], subject: str, content: str) -> bool:
    target_emails: list[str] = email if isinstance(email, list) else [email]

    msg = MIMEText(content)
    msg["Subject"] = subject
    msg["From"] = settings.email_address
    msg["To"] = ", ".join(target_emails)

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        server.starttls()
        server.login(settings.email_address, settings.email_password)
        server.sendmail(settings.email_address, target_emails, msg.as_string())
        return True


def send_activation_email(target_email: str, activation_link: str):
    return send_email(
        target_email,
        "Activate your account",
        f"Welcome to {settings.project_name}!\n"
        f"Click the link to activate your account: {activation_link}",
    )
