from .. config import settings
import yagmail


def reset_password_email(temporary_password: str, email: str):
    try:
        yag = yagmail.SMTP(settings.YAGMAIL_USERNAME, settings.YAGMAIL_PASSWORD)
        content = temporary_password
        yag.send(to=email, subject='DB_MATERIAL', contents=content)

        return True

    except Exception as error:
        return False
