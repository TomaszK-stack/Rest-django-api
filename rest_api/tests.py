from rest_framework.authtoken.models import Token
from .views import *
from django.urls import reverse
from rest_framework.test import APITestCase
# from django.test import TestCase
from .models import User, Tier
from io import BytesIO
from PIL import Image
from django.core.files.temp import NamedTemporaryFile
class ImageViewCreateTestCase(APITestCase):

    def setUp(self) -> None:

        tier = Tier.objects.create(name="test", original_image=True, sizes_of_thumb={"1": 200, "2": 500})
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

    def test_file_is_accepted(self):
        self.client.force_authenticate(self.user)

        image = Image.new('RGB', (100, 100))

        tmp_file = NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)

        create_response = self.client.post(self.create_url, {'image': tmp_file}, format='multipart')
        list_response = self.client.get(self.list_images_url)

        self.assertEqual(201, create_response.status_code)
        self.assertEqual(200, list_response.status_code)
        self.assertEqual(3, len(list_response.json()))

    def test_upload_invalid_image(self):
        self.client.force_authenticate(self.user)

        image = Image.new('RGB', (100, 100))

        tmp_file = NamedTemporaryFile(suffix='.jpeg')
        image.save(tmp_file)
        tmp_file.seek(0)

        create_response = self.client.post(self.create_url, {'image': tmp_file}, format='multipart')
        self.assertEqual(400, create_response.status_code)

class ExpiringLinkTestCase(APITestCase):

    def setUp(self) -> None:
        self.exp_link_url = reverse("rest_api:generate_exp_links")
        self.allowed_tier = Tier.objects.create(name="test", original_image=True, sizes_of_thumb={"1": 200, "2": 500}, generate_exp_links = True)
        self.unallowed_tier = Tier.objects.create(name="test", original_image=True, sizes_of_thumb={"1": 200, "2": 500}, generate_exp_links = False)
        self.allowed_user = User.objects.create_user(username="allowed", password="allowed", tier = self.allowed_tier)
        self.unallowed_user = User.objects.create_user(username="unallowed", password="unallowed", tier = self.unallowed_tier)

        image = Image.new('RGB', (100, 100))

        self.tmp_file = NamedTemporaryFile(suffix='.jpg')
        image.save(self.tmp_file)
        self.tmp_file.seek(0)
    def test_getting_exp_link(self):
        self.client.force_authenticate(self.allowed_user)
        self.client.post(reverse("rest_api:create_view"),{'image': self.tmp_file}, format='multipart' )
        image_response = self.client.get(reverse("rest_api:image_view"))
        image_link = image_response.json()[0]["image"]

        exp_link_response = self.client.post(self.exp_link_url, {"link": image_link, "time": 312})
        self.assertEqual(200, exp_link_response.status_code)

    def test_getting_exp_link_without_access(self):
        self.client.force_authenticate(self.unallowed_user)
        self.client.post(reverse("rest_api:create_view"), {'image': self.tmp_file}, format='multipart')
        image_response = self.client.get(reverse("rest_api:image_view"))
        image_link = image_response.json()[0]["image"]

        exp_link_response = self.client.post(self.exp_link_url, {"link": image_link, "time": 312})
        self.assertEqual(403, exp_link_response.status_code)