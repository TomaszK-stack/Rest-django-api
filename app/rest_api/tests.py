from rest_framework.authtoken.models import Token
from .views import *
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import User, Tier


class ImageViewCreateTestCase(APITestCase):

    def setUp(self) -> None:

        tier = Tier.objects.create(name="test", original_image=True, sizes_of_thumb={"1": 200, "2": 500})
        self.image_path = "static/test_image/"
        self.create_url = reverse("rest_api:create_view")
        self.list_images_url = reverse("rest_api:image_view")
        self.user = User.objects.create_user(username="test", password="test", tier = tier)
        self.token = Token.objects.create(user=self.user)
        self.token.save()
    def test_get_list_images_without_auth(self):
        response = self.client.get(self.list_images_url)
        self.assertEqual(401, response.status_code)


    def test_get_list_after_auth(self):
        response = self.client.get(self.list_images_url, HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEqual(200, response.status_code)


    def test_getting_images_after_upload(self):
        with open(self.image_path + "test1.png", "rb" ) as image:
            files = {"image": image}
            create_response = self.client.post(self.create_url,HTTP_AUTHORIZATION='Token ' + self.token.key, body = files)
            print(create_response)
            self.assertEqual(200, create_response.status_code)
        list_response = self.client.get(self.list_images_url, HTTP_AUTHORIZATION='Token ' + self.token.key)
        print(list_response)
