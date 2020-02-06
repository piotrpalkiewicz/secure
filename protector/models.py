from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.urls import reverse

from protector.consts import GENERATED_PASSWORD_LEN


class Resource(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField(
        blank=True,
        verbose_name="URL Address",
        help_text="Type URL Address that you want to protect",
    )
    file = models.FileField(blank=True, upload_to="media/", verbose_name="File")
    protected_url = models.CharField(blank=True, max_length=120)
    password = models.CharField(blank=True, max_length=GENERATED_PASSWORD_LEN)

    def __repr__(self) -> str:
        return f"<Resource>: {self.id or 0} - {self.url or self.file}"

    def __str__(self):
        return f"{self.id or 0} - {self.url or self.file}"

    @property
    def full_protected_url(self):
        url = reverse("protector-protected_resource", args=(self.protected_url,))
        domain = Site.objects.get_current().domain
        return f"https://{domain}{url}"
