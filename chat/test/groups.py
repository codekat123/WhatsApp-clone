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

CACHE_SETTINGS = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
REST_FRAMEWORK={
        'DEFAULT_THROTTLE_CLASSES': [],
        'DEFAULT_THROTTLE_RATES': {}
    }

@override_settings(DATABASES=SQLITE_DB_SETTINGS, CACHES=CACHE_SETTINGS,REST_FRAMEWORK=REST_FRAMEWORK)
class GroupAPITest(APITestCase):

    def setUp(self):
        send_otp_url = reverse("users:send-otp")
        register_url = reverse("users:register")

        send_otp_response = self.client.post(
            send_otp_url,
            {'phone_number': '01004968745'},
            format='json'
        )
        self.assertEqual(send_otp_response.status_code, status.HTTP_200_OK)

        register_response = self.client.post(
            register_url,
            {
                'session_id': send_otp_response.data['session_id'],
                'otp': '000000'
            },
            format='json'
        )
        self.assertEqual(register_response.status_code, status.HTTP_200_OK)

        self.access = register_response.data['access']

        # Create group ONCE here
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access}')
        create_url = reverse("chat:group-create")
        create_res = self.client.post(create_url)


        self.assertEqual(create_res.status_code, status.HTTP_201_CREATED)

        self.group_id = create_res.data['id']



    def test_update_group(self):
        url = reverse("chat:group-update", kwargs={"group_id": self.group_id})
        response = self.client.patch(url,{"name":"test group update"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_group(self):
        url = reverse("chat:group-delete", kwargs={"group_id":self.group_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

