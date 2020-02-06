import factory

from django.contrib.auth.models import User

from protector.models import Resource


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    username = factory.Faker("user_name")
    password = factory.PostGenerationMethodCall("set_password", "user")
    is_active = True


class ResourceFactory(factory.DjangoModelFactory):
    class Meta:
        model = Resource

    author = factory.SubFactory(UserFactory)
    url = factory.Faker("image_url")
