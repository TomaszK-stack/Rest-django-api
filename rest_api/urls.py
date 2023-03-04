from django.urls import path
from .views import *
from rest_framework.authtoken import views

app_name = "rest_api"

urlpatterns = [
    path('images/', ImageApiView.as_view(), name = "image_view"),
    path('create/', ImageCreateView.as_view(), name = "create_view"),
    path('explinks/', generate_exp_links, name = "generate_exp_links" ),
    path('auth/', views.obtain_auth_token, name = "get_auth_token" ),
    path('image/<str:signature>', get_image, name="image"),
]