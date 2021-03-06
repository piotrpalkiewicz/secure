from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from protector import utils
from protector.consts import GENERATED_PASSWORD_LEN
from protector.managers import ResourceManager
from protector.utils import get_resource_file_path


class Resource(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField(
        blank=True,
        verbose_name="URL Address",
        help_text="Type URL Address that you want to protect",
    )
    file = models.FileField(
        blank=True, upload_to=get_resource_file_path, verbose_name="File"
    )
    protected_url = models.CharField(blank=True, max_length=120)
    password = models.CharField(blank=True, max_length=GENERATED_PASSWORD_LEN)
    visits = models.PositiveIntegerField(default=0, verbose_name="Visits")
    created_at = models.DateField(auto_now_add=True)

    objects = ResourceManager()

    class Meta:
        verbose_name = "Resource"
        verbose_name_plural = "Resources"

    def __repr__(self) -> str:
        return f"<Resource>: {self.id or 0} - {self.url or self.file}"

    def __str__(self):
        return f"{self.url or self.file}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.protected_url = utils.generate_protected_url()
            self.password = utils.generate_password()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.url and self.file:
            raise ValidationError(
                "You can protect only one source at time - URL or File."
            )
        if not self.url and not self.file:
            raise ValidationError(
                "Upload File or type URL Address you want to protect."
            )

    @property
    def full_protected_url(self):
        url = reverse("protector-protected_resource", args=(self.protected_url,))
        domain = Site.objects.get_current().domain
        return f"https://{domain}{url}"

    @property
    def final_resource_url(self):
        if self.url:
            return self.url
        return reverse("protector-download", args=(self.protected_url,))
