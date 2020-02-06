from django.shortcuts import get_object_or_404

from protector.models import Resource


def is_password_match(*, protected_url, password):
    try:
        Resource.objects.get(protected_url=protected_url, password=password)
    except Resource.DoesNotExist:
        return False
    return True
