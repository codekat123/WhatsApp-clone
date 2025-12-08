from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.test import override_settings
from users.models import User



SQLITE_DB_SETTINGS = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

@override_settings(DATABASES=SQLITE_DB_SETTINGS)
class ChatListAPITest(APITestCase):

    def setUp(self):
        send_otp_url = reverse("users:send-otp")
        register_url = reverse("users:register")

        send_otp_response = self.client.post(send_otp_url, {
            'phone_number': '01004968745'
        }, format='json')

        self.assertEqual(send_otp_response.status_code, status.HTTP_200_OK)

        register_response = self.client.post(register_url, {
            'session_id': send_otp_response.data['session_id'],
            'otp': '000000'
        }, format='json')

        self.assertEqual(register_response.status_code, status.HTTP_200_OK)

        self.access = register_response.data['access']
        self.user =  User.objects.create_user(
            phone_number="01004968565",
            full_name="Ahmed",
            is_active=True
        )

    def _auth(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access}')

    def test_get_list_chat(self):
        self._auth()

        url = reverse("chat:chat-list")

        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK,response.status_code)
