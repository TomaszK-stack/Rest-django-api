# from rest_framework.test import APIRequestFactory, force_authenticate


# url = 'http://127.0.0.1:8000/api/v1/create/'
# auth_token = '507f73214411a77ceb662534e3c7b458f22bca1f'
#
# headers = {'Authorization': f'Token {auth_token}'}
# response = requests.get(url, headers=headers)
#
# print(response.json())
#
# url = 'http://127.0.0.1:8000/api/v1/create/'
# file_path = 'C:\\Users\\korni\\HexOcean\\app\\static\\images\\326811043_5719292304862868_8427228551201173610_n (1).png'
#
# with open(file_path, 'rb') as f:
#     files = {'image': f}
#     response = requests.post(url, files=files, headers={"Authorization": "Token 507f73214411a77ceb662534e3c7b458f22bca1f"})
#
# print(response.status_code)

from .views import *
from django.urls import reverse
from rest_framework.test import APITestCase



class AuthenicationTests(APITestCase):

    url = reverse("ImageApiView")
    def test_unauth_user(self):
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)