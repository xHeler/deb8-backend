import factory
from faker import Faker
from django.contrib.auth import get_user_model

fake = Faker()

class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.LazyAttribute(lambda _: fake.user_name())
    email = factory.LazyAttribute(lambda _: fake.email())
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')
    is_active = True
    is_staff = False
    is_superuser = False
