from django.urls import path
from .views import *

urlpatterns = [
    path('image/<pk>', ImageApiView.as_view(), name = "image_view"),
    path('create/', ImageCreateView.as_view(), name = "create_view"),
]