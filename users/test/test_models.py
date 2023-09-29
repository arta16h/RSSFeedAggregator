from django.test import TestCase
from django.db.utils import IntegrityError
from ..models import User


class UserModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
