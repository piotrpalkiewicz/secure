from django import forms

from protector import services
from protector.consts import GENERATED_PASSWORD_LEN
from protector.models import Resource


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = (
            "url",
            "file",
        )


class ResourcePermissionForm(forms.Form):
    password = forms.CharField(
        max_length=GENERATED_PASSWORD_LEN, label="Enter a Password"
    )

    def is_valid(self):
        if services.is_password_match(**self.data):
            return True
        self.add_error("password", "Wrong password.")
        return False
