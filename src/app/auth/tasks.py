from enum import StrEnum, auto
import smtplib
import ssl
from email.message import EmailMessage

from common.celery_worker import celery
from common.settings import settings


class EmailTypeEnum(StrEnum):
    VERIFICATION = auto()
    RESET_PASSWORD = auto()


def get_verification_email(
    username: str, email_address: str, token: str
) -> EmailMessage:
    msg = EmailMessage()
    msg["Subject"] = "Verification"
    msg["From"] = settings.SMTP_USER
    msg["To"] = email_address
    msg.set_content(
        f"<h1>Your verification token, {username}</h1>"
        f"<span>{token}</span>",
        subtype="html",
    )
    return msg


def get_reset_password_email(
    username: str, email_address: str, token: str
) -> EmailMessage:
    msg = EmailMessage()
    msg["Subject"] = "Reset your password"
    msg["From"] = settings.SMTP_USER
    msg["To"] = email_address
    msg.set_content(
        f"<h1>Did you forget your password, {username}?</h1>"
        f"<span>{token}</span>",
        subtype="html",
    )
    return msg


get_msg = {
    EmailTypeEnum.VERIFICATION: get_verification_email,
    EmailTypeEnum.RESET_PASSWORD: get_reset_password_email,
}


@celery.task
def send_email_task(
    email_type: EmailTypeEnum, username: str, email_address: str, token: str
) -> None:
    msg = get_msg[email_type](username, email_address, token)
    _ = ssl.SSLContext(ssl.PROTOCOL_TLS)
    server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
    server.starttls()
    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
    server.send_message(msg)
