import os
import secrets
import string
import uuid

from protector.consts import GENERATED_PASSWORD_LEN


def generate_protected_url():
    return secrets.token_urlsafe()


def generate_password():
    password_characters = string.ascii_letters + string.digits
    return "".join(
        secrets.choice(password_characters) for i in range(GENERATED_PASSWORD_LEN)
    )


def path_and_rename(prefix, filename):
    ext = filename.split(".")[-1]
    filename = "{}.{}".format(uuid.uuid4().hex, ext)
    return os.path.join(prefix, filename)


def get_resource_file_path(instance, filename):
    return path_and_rename("resource/", filename)
