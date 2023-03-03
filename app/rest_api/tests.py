


from .views import *
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import User, Tier

class AuthenicationTests(APITestCase):

    url = reverse("image_view")
    url_2 = reverse("create_view")
    file_path = "static/test_image/test1.png"
    auth_token = '507f73214411a77ceb662534e3c7b458f22bca1f'

    @classmethod
    def setUpTestData(cls):
        tier = Tier(name="Basic", original_image=True, sizes_of_thumb={"2": "200"})
        tier.save()
        cls.test_user = User(username = "testuser", password = "test", tier = tier)
        cls.test_user.save()
        
    def test_unauth_user(self):
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)

    def test_adding_image_without_auth_token(self):
        with open(self.file_path, "rb") as f:
            print(f)
            files = {"image":f}
            response = self.client.post(self.url_2, files=files)
        self.assertEqual(400, response.status_code)


    def test_get_image_after_add(self):
        headers = {'Authorization': f'Token {self.auth_token}'}

        with open(self.file_path, "rb") as f:
            files = {"image":f}
            response = self.client.post(self.url_2, files=files, headers = headers)
            response_2 = self.client.post(self.url, headers= headers)
            print(response)


