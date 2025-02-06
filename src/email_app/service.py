from pydantic import EmailStr
from src.config import settings
from src.email_app.exc import EmailException

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from ssl import create_default_context


class EmailService:
    def send_email(self, email_: EmailStr, subject: str, message: str) -> None:
        # host = 'smtp.' + \
        #     settings.email.login[settings.email.login.index('@') + 1:]

        # Создаем сообщение
        msg = MIMEMultipart()
        msg["From"] = settings.email.login
        msg["To"] = email_
        msg["Subject"] = subject

        # Добавляем тело письма
        msg.attach(MIMEText(message, "plain"))

        # Создаем SSL контекст для безопасного соединения
        context = create_default_context()

        try:
            # Подключаемся к SMTP серверу с шифрованием
            with smtplib.SMTP_SSL(
                settings.email.smpt_host, settings.email.smtp_port, context=context
            ) as server:
                server.login(settings.email.login, settings.email.password)
                server.sendmail(settings.email.login, email_, msg.as_string())
        except Exception as e:
            raise EmailException(f"Ошибка при отправке письма на почту {email_}: {e}")


email_service = EmailService()
