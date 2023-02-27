from django.test import TestCase
import pytest
from django.urls import reverse
from rest_framework import status

import os
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
settings.configure()
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestProductAPI:

    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def product(self, product_factory):
        return product_factory()
    def test(self, api_client):
        url = reverse("")
        response = api_client.get(url)
        print(response)

