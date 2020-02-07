from django.conf import settings

import file_utils
from protector.models import Resource


def is_password_match(*, protected_url, password):
    try:
        Resource.objects.get(protected_url=protected_url, password=password)
    except Resource.DoesNotExist:
        return False
    return True


def get_file(filename):
    return file_utils.file_service.get_file_url(filename)
