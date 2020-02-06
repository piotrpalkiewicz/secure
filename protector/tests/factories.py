import factory
from django.contrib.auth.models import User


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    email = "user@example.com"
    username = "user"
    password = factory.PostGenerationMethodCall("set_password", "user")
    is_active = True
