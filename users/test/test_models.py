from django.test import TestCase
from django.db.utils import IntegrityError
from ..models import User


class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')


    def test_username_label(self):
        field_label = self.user._meta.get_field("username").verbose_name
        self.assertEqual(field_label, "username")

    def test_username_max_length(self):
        max_length = self.user._meta.get_field("username").max_length
        self.assertEqual(max_length, 50)

    def test_email_label(self):
        field_label = self.user._meta.get_field("email").verbose_name
        self.assertEqual(field_label, "email")

    def test_first_name_max_length(self):
        max_length = self.user._meta.get_field("first_name").max_length
        self.assertEqual(max_length, 50)

