from datetime import timedelta

from django.db.models import F
from django.utils import timezone

from protector.models import Resource


def django_doctor_check():
    queryset = Resource.objects.all()
    if queryset:
        return 1
    return 0

def is_password_match(*, protected_url, password):
    try:
        Resource.objects.get(protected_url=protected_url, password=password)
    except Resource.DoesNotExist:
        return False
    return True


def is_valid_link(created_at):
    return created_at + timedelta(days=1) > timezone.now().date()


def increment_resource_visits(resource):
    resource.visits = F("visits") + 1
    resource.save()
