from django import forms
from django.core.exceptions import ValidationError

from protector.models import Resource


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ("url", "file",)

    def clean(self) -> None:
        cleaned_data = super().clean()
        url = cleaned_data.get("url")
        file = self.files.get("file")

        if url and file:
            raise ValidationError("You can protect only one source at time - URL or File.")
        if not url and not file:
            raise ValidationError("Upload File or type URL Address you want protect.")
