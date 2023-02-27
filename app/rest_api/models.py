from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from PIL import Image as Img
from io import BytesIO
from django.core.files import File
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
    image_th_200 = models.ImageField(upload_to="static/thumbnail_200", blank=True)
    image_th_400 = models.ImageField(upload_to="static/thumbnail_400", blank=True)

    user_id = models.ForeignKey(to=User,  on_delete=models.CASCADE, default=None)
    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None, *args, **kwargs):
        user = User.objects.filter(pk=self.user_id.pk).first()
        self.image_th_200 = self.make_thumbnail(self.image)

        if user.tier == "Enterprise" or user.tier == "Premium":
            self.image_th_400 = self.make_thumbnail(self.image, 400)


        if  user.tier == "BASIC":
            self.image = None


        super().save(*args, **kwargs)

    def make_thumbnail(self, image, height = 200):

        img = Img.open(image)
        img = img.convert('RGB')
        width = img.width
        size = (width, height)
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        thumbnail = File(thumb_io, name=image.name)

        return thumbnail

