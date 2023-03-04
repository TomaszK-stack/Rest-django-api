from rest_framework import serializers
from .models import Image
from django.core.validators import FileExtensionValidator
class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(validators=[FileExtensionValidator(["jpg", "png"])])
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())


    class Meta:
        model = Image
        fields = ('image', "user", "size")
        read_only_fields = ("size",)
    def create(self, validated_data):
        return Image.objects.create(**validated_data)
