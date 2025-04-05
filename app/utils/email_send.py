"""
Common functions for sending emails
"""

import aiosmtplib
from email.mime.text import MIMEText

from app.config import settings


async def send_email(email: str | list[str], subject: str, content: str) -> bool:
    target_emails: list[str] = email if isinstance(email, list) else [email]

    msg = MIMEText(content)
    msg["Subject"] = subject
    msg["From"] = settings.email_address
    msg["To"] = ", ".join(target_emails)

    async with aiosmtplib.SMTP(
        hostname=settings.smtp_settings.smtp_host,
        port=settings.smtp_settings.smtp_port,
        use_tls=settings.smtp_settings.smtp_connection == "SSL",
        start_tls=False,
    ) as server:
        if settings.smtp_settings.smtp_connection == "TLS":
            await server.starttls()
        await server.login(settings.email_address, settings.email_password)
        await server.sendmail(settings.email_address, target_emails, msg.as_string())
        return True


async def send_activation_email(target_email: str, activation_link: str):
    return await send_email(
        target_email,
        "Activate your account",
        f"Welcome to {settings.project_name}!\n"
        f"Click the link to activate your account: {activation_link}",
    )
