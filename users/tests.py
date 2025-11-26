from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.test import override_settings

SQLITE_DB_SETTINGS = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

CACHE_SETTINGS = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}


@override_settings(DATABASES=SQLITE_DB_SETTINGS, CACHES=CACHE_SETTINGS)
class UserAuthAPITest(APITestCase):
    
    def setUp(self):
        from django.core.cache import cache
        cache.clear()


    def send_otp(self):
        url = reverse("users:send-otp")
        payload = {"phone_number": "01004968745"}
        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("session_id", response.data)
        return response.data["session_id"]

    def test_send_otp(self):
        session_id = self.send_otp()
        self.assertTrue(len(session_id) > 5)

    def _auth(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access}') 

    def test_verify_correct_otp(self):
        session_id = self.send_otp()

        url = reverse("users:register")

        payload = {
            "session_id": session_id,
            "otp": "000000"  # fixed OTP
        }

        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIn("user", response.data)
        self.assertEqual(response.data["user"]["phone_number"], "+201004968745")

    def test_verify_wrong_otp(self):
        session_id = self.send_otp()

        url = reverse("users:register")

        payload = {
            "session_id": session_id,
            "otp": "999999"  # wrong
        }

        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_too_many_attempts(self):
        session_id = self.send_otp()
        url = reverse("users:register")

        for _ in range(5):  
            payload = {"session_id": session_id, "otp": "345434"}
            response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_profile_update(self):
        self._auth()
        url = reverse("users:profile-update")
        
        response = self.client.patch(
            url,
            {"about":"I'm cool, no one knows that 😎"},
            format="json"
        )
        self.assertEqual(response.status,status.HTTP_200_OK)
