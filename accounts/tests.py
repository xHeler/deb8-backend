from django.test import TestCase
from .factories import CustomUserFactory

class CustomUserTests(TestCase):
    def test_create_user(self):
        user = CustomUserFactory()
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin_user = CustomUserFactory(is_superuser=True, is_staff=True)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)
