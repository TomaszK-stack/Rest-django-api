from django.db import models

from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.


class User(AbstractUser):
    TIERS = (
        ("Basic","Basic"),
        ("Premium","Premium"),
        ("Enterprise","Enterprise")
    )
    tier = models.CharField(max_length= 120, choices=TIERS)

class Image(models.Model):
    image = models.ImageField(upload_to="static/images/")
    user_id = models.ForeignKey(to=User,  on_delete=models.CASCADE, default=None)
    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = User.objects.filter(pk=user_id)
