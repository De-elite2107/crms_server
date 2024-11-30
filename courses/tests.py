# tests.py
from django.test import TestCase
from .models import User
from rest_framework.authtoken.models import Token

class LogoutAPITest(TestCase):
    def setUp(self):
        # Create a test user and an auth token for them
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)

    def test_logout(self):
        # Ensure the token exists before logging out
        self.assertIsNotNone(Token.objects.filter(user=self.user).first())

        # Call the logout API with correct authorization header
        response = self.client.post('/api/logout/', **{
            'HTTP_AUTHORIZATION': f'Token {self.token.key}'
        })

        # Check if logout was successful (status code 200)
        self.assertEqual(response.status_code, 200)

        # Check that the token has been deleted
        with self.assertRaises(Token.DoesNotExist):
            Token.objects.get(key=self.token.key)

    def tearDown(self):
        # Clean up after tests (optional)
        self.user.delete()
