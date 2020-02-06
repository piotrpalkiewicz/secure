import secrets
import string

from protector.consts import GENERATED_PASSWORD_LEN


def generate_protected_url():
    return secrets.token_urlsafe()


def generate_password():
    password_characters = string.ascii_letters + string.digits
    return "".join(
        secrets.choice(password_characters) for i in range(GENERATED_PASSWORD_LEN)
    )
