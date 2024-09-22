from pydantic import EmailStr
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from src.config import settings


class EmailService:
    def send_email(self, email_: EmailStr, subject: str, message: str) -> None:
        # host = 'smtp.' + \
        #     settings.email.login[settings.email.login.index('@') + 1:]
        host = 'smtp.gmail.com'

        msg = MIMEText(f'{message}', 'plain', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = settings.email.login
        msg['To'] = email_

        s = smtplib.SMTP_SSL(host=host, port=465, timeout=10)

        # s.starttls()
        s.login(settings.email.login, settings.email.password)
        s.auth_plain()

        s.sendmail(msg['From'], settings.email.login, msg.as_string())
        s.quit()


email_service = EmailService()
