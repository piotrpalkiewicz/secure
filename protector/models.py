from django.db import models


class Resource(models.Model):
    url = models.URLField(blank=True, verbose_name="URL Address")
    file = models.FileField(blank=True, upload_to='media/', verbose_name="File")

    def __repr__(self) -> str:
        return f"<Resource>: {self.id or 0} - {self.url or self.file}"

    def __str__(self):
        return f"{self.id or 0} - {self.url or self.file}"
