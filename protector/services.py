import secrets

from django.urls import reverse


def generate_protected_url():
    url_hash = secrets.token_urlsafe()
    return reverse("protector-resource_protected", args=(url_hash,))
