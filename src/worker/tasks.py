import dramatiq
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


from config import settings


@dramatiq.actor
def activate_user_message(user_email, activate_token):
    # TODO: it's dummy just for test. Should be refactored.
    sender_email = 'template@fastapi.ru'

    activating_url = f'{settings.API_BASE_DOMAIN}/users/me/activate?token={activate_token}'

    message = MIMEMultipart("alternative")
    message["Subject"] = "Test subject"
    message["From"] = sender_email

    html = """\
    <html>
    <body>
        <p>Hi,<br>
        This is the test email
            <a href={activating_url}>activate</a>
        </p>
    </body>
    </html>
    """.format(activating_url=activating_url)

    part = MIMEText(html, "html")
    message.attach(part)

    server = smtplib.SMTP(settings.MAIL_HOST, settings.MAIL_PORT)

    if settings.MAIL_LOGIN and settings.MAIL_PASSWORD:
        server.login(
            settings.MAIL_LOGIN,
            settings.MAIL_PASSWORD
        )

    server.sendmail(
        sender_email, user_email, message.as_string()
    )
