from io import BytesIO
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
from django.core.validators import FileExtensionValidator
from .validators import validata_json_data
import os
# from django.contrib.auth.management.commands.createsuperuser import
class Tier(models.Model):
    name = models.CharField(max_length=50)
    original_image = models.BooleanField(default=False)
    sizes_of_thumb = models.JSONField(default={"1":200}, validators=[validata_json_data])
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
        else:
            self.set_password(self.password)

        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None


class Image(models.Model):
    image = models.ImageField(upload_to="static/images/",validators=[FileExtensionValidator(["jpg", "png"])])

    thumbnail = models.BooleanField(default=False)
    user = models.ForeignKey(to=User,  on_delete=models.CASCADE, default=None)
    size = models.IntegerField( default=100, null=True)
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None, *args, **kwargs):
        if not self.thumbnail:
            user = User.objects.filter(pk=self.user.pk).first()
            tier = user.tier
            for size in tier.sizes_of_thumb:
                thumbnail = self.make_thumbnail(self.image, tier.sizes_of_thumb[size])
                image = Image(image = thumbnail, thumbnail = True, user = user, size=tier.sizes_of_thumb[size])
                image.save()
            if self.user.tier.original_image:
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    # def delete(self, using=None, keep_parents=False):
    #     os.remove("static/images/" + self.image )
    #
    #     super().delete()
    def make_thumbnail(self, image, height = 200):

        img = Img.open(image)
        img = img.convert('RGB')
        width = img.width
        size = (width, int(height))
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
    def get_signed_image_url(self):
        signer = Signer()
        url = reverse("localhost:8000/" + self.image.url)
        return url


