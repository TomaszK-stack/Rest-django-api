from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from PIL import Image as Img
from io import BytesIO
from django.core.files import File
from django.urls import reverse
from django.core.signing import Signer
from datetime import timedelta
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

class Tier(models.Model):
    name = models.CharField(max_length=50)
    original_image = models.BooleanField(default=False)
    sizes_of_thumb = models.JSONField(default={"1":"200"})
    generate_exp_links = models.BooleanField(default=False)

    def __str__(self):
        return self.name
class User(AbstractUser):

    tier = models.ForeignKey(to=Tier, on_delete=models.CASCADE, default=None, null=True)
    def save(self, *args, **kwargs):
        if self.is_staff:
            tier = Tier.objects.get_or_create(name = "Admin")[0]
            tier.save()
            self.tier = tier
        super().save(*args, **kwargs)


class Image(models.Model):
    image = models.ImageField(upload_to="static/images/")
    thumbnail = models.BooleanField(default=False)

    user = models.ForeignKey(to=User,  on_delete=models.CASCADE, default=None)
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None, *args, **kwargs):
        if not self.thumbnail:
            user = User.objects.filter(pk=self.user.pk).first()
            tier = user.tier
            for size in tier.sizes_of_thumb:
                thumbnail = self.make_thumbnail(self.image, tier.sizes_of_thumb[size])
                image = Image(image = thumbnail, thumbnail = True, user = user)
                image.save()

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
    def get_signed_image_url(self):
        signer = Signer()
        url = reverse("localhost:8000/" + self.image.url)
        return url


