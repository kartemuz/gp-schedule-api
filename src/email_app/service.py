from pydantic import EmailStr
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from src.config import settings


class EmailService:
    def send_email(email: EmailStr, subject: str, message: str) -> None:
        host = settings.email.login[settings.email.login.index('@') + 1:]

        msg = MIMEText(f'{message}', 'plain', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = settings.email.login
        msg['To'] = email

        s = smtplib.SMTP('smtp.' + f'{host}', 587, timeout=10)

        s.starttls()
        s.login(settings.email.login, settings.email.password)
        s.sendmail(msg['From'], email, msg.as_string())
        s.quit()


email_service = EmailService()
