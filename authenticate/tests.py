from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthenticateViewTests(TestCase):
    def test_login_view_authenticated_redirect(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('login'))
        self.assertRedirects(response, reverse('default'))
